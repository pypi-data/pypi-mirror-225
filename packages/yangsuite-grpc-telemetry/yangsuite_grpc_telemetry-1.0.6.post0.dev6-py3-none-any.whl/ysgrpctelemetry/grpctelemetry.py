# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
"""Python backend logic for yangsuite-grpc-telemetry.

Nothing in this file should use any Django APIs.
"""
import os
import json
from datetime import datetime
from concurrent import futures
from collections import deque
from urllib.parse import urlparse
from elasticsearch import Elasticsearch
import grpc

from ysdevices import YSDeviceProfile
from .generated import (
    add_gRPCMdtDialoutServicer_to_server,
    gRPCMdtDialoutServicer,
    Telemetry,
)

from yangsuite import get_logger
from yangsuite.paths import get_path

log = get_logger(__name__)

DOCKER_RUN = os.getenv('DOCKER_RUN', False)
GRPC_PRIMARY_IP_ADDRESS = os.getenv('GRPC_PRIMARY_IP_ADDRESS')


class YSGrpcMdtDialoutServicer(gRPCMdtDialoutServicer):
    """Concrete subclass of :class:`gRPCMdtDialoutServicer` stub."""

    def __init__(self, output_format="compact", out_queue=deque()):
        """Create an instance designed to handle inbound telemetry messages.

        Args:
          output_format (str): One of:

            - 'raw' (string representation provided by grpcio)
            - 'compact' (custom string representation, less verbose)
        """
        super(YSGrpcMdtDialoutServicer, self).__init__()
        self.output_format = output_format
        self.stdout_queue = out_queue

    def walk_fields(self, fields, pfx="", msg_fields=[]):

        if pfx == '/content':
            pfx = ''
        elif pfx == '/keys':
            pfx = ''

        for field in fields:
            if field.fields:
                self.walk_fields(
                    field.fields, pfx + '/' + field.name,
                    msg_fields
                )
            else:
                value = None
                if field.HasField('bytes_value'):
                    value = field.bytes_value
                elif field.HasField('string_value'):
                    value = field.string_value
                if field.HasField('bool_value'):
                    value = field.bool_value
                elif field.HasField('sint32_value'):
                    value = field.sint32_value
                elif field.HasField('sint64_value'):
                    value = field.sint64_value
                elif field.HasField('uint32_value'):
                    value = field.uint32_value
                elif field.HasField('uint64_value'):
                    value = field.uint64_value
                elif field.HasField('double_value'):
                    value = field.double_value
                elif field.HasField('float_value'):
                    value = field.float_value

                if value is None:
                    continue

                msg_fields.append({
                    'child_path': pfx + '/',
                    'name': field.name,
                    'value': value
                })

        return msg_fields

    def MdtDialout(self, request_iterator, context):
        """Handle an inbound telemetry message from the device."""
        for request in request_iterator:
            t = Telemetry()
            t.ParseFromString(request.data)
            if self.output_format == 'raw':
                self.stdout_queue.append({'raw': str(t)})
            elif self.output_format == 'compact':
                for gpb in t.data_gpbkv:
                    dt = datetime.fromtimestamp(gpb.timestamp / 1e3)
                    msg = {
                        'timestamp': dt.strftime('%Y %b %d %H:%M:%S:%f'),
                        'subscription': t.subscription_id_str,
                        'node': t.node_id_str,
                        'subscribe_path': '/' + t.encoding_path,
                        'fields': self.walk_fields(gpb.fields, "", [])
                    }
                    self.stdout_queue.append(msg)


class YSGrpcTelemetryServer(object):
    """Class providing feature logic for yangsuite-grpc-telemetry.

    .. seealso:: https://github.com/grpc/grpc/blob/v1.13.x/examples/python/route_guide/route_guide_server.py
    """   # noqa: E501

    _ONE_DAY_IN_SECONDS = 60 * 60 * 24

    servers = {}
    stdout_queue = deque()
    out_uri = ''
    out_file = ''

    @classmethod
    def serve(cls, address=None, port="5678", user=None, device=None):
        """Run the server indefinitely."""
        if address is None:
            address = GRPC_PRIMARY_IP_ADDRESS
        if port in cls.servers:
            log.warning("Tried to start server on port %s, already running!",
                        port)
            return False, 'Server already running on port {0}'.format(port)
        tls = False
        # Create gRPC server instance
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        if device:
            try:
                device_path = get_path('user_devices_dir', user=user)
            except ValueError:
                return (
                    False,
                    'Device {0} has no certificates uploaded.'.format(device)
                )
            tls = True
            dev_profile = YSDeviceProfile.get(device)
            ser_cert_name = dev_profile.base.servercert
            ser_cert_file = os.path.join(device_path, device, ser_cert_name)
            ser_key_name = dev_profile.base.serverkey
            ser_key_file = os.path.join(device_path, device, ser_key_name)
            if os.path.isfile(ser_cert_file):
                ser_cert = open(ser_cert_file, 'rb').read()
            else:
                return False, 'Server certificate {0} missing.'.format(
                    ser_cert_name
                )
            if os.path.isfile(ser_key_file):
                ser_key = open(ser_key_file, 'rb').read()
            else:
                return False, 'Server key {0} missing.'.format(ser_cert_name)
            creds = grpc.ssl_server_credentials([(ser_key, ser_cert)])
            server_port = server.add_secure_port(
                '{0}:{1}'.format(address, port), creds
            )
        else:
            server_port = server.add_insecure_port(
                "{0}:{1}".format(address, port)
            )
        if server_port == 0:
            return False, 'Unable to start server on {0} port {1}'.format(
                address, port)
        # Tell it to pass inbound MDT RPCs to an instance of
        # YSGrpcMdtDialoutServicer for servicing
        servicer = YSGrpcMdtDialoutServicer(out_queue=cls.stdout_queue)
        add_gRPCMdtDialoutServicer_to_server(servicer, server)
        # Start it - all above setup MUST be applied before calling start()!
        server.start()
        cls.servers[str(port)] = (server, servicer, address, tls, '', '')
        log.info("Server started on %s port %s", address, port)
        return True, 'Server started on {0} port {1}'.format(address, port)

    @classmethod
    def get(cls, port):
        return cls.servers.get(str(port), None)

    @classmethod
    def stop(cls, port):
        server, servicer, _, _, _, _ = cls.get(port)
        if server:
            server.stop(0)
            del cls.servers[port]
            del server
            del servicer
            log.warning("Server stopped on port %s", port)
            return True, 'Server stopped on port {0}'.format(port)
        else:
            log.warning("Tried to stop server on port %s, not running!",
                        port)
            return (
                False,
                'Retry stop for server running on port {0}'.format(port)
            )

    @classmethod
    def set_output(cls, fileout=None, uri=None):
        """Setup additional output methods."""
        # TODO: Output should be set per stream not global
        if fileout:
            if not os.path.isdir(os.path.dirname(fileout)):
                log.error("File output directory {0} missing.".format(
                    os.path.dirname(fileout)
                ))
                raise OSError(
                    'File output directory "{0}"" missing.'.format(
                        os.path.dirname(fileout)
                    )
                )
            cls.out_file = fileout
            log.info("Servicer output set to {0}".format(fileout))
        if uri:
            if not urlparse(uri).scheme:
                raise OSError('Invalid URL "{0}"'.format(uri))

            cls.out_uri = uri
            cls.es = Elasticsearch([uri])
            log.info("Servicer output set to {0}".format(uri))

    @classmethod
    def get_output(cls):
        """Collect streaming data from servicer and send to output(s)."""
        data = {'output': []}
        while len(cls.stdout_queue):
            msg = cls.stdout_queue.popleft()
            data['output'].append(msg)

            if cls.out_file:
                if os.path.isdir(
                    os.path.dirname(
                        cls.out_file)):
                    try:
                        if os.path.isfile(cls.out_file):
                            with open(cls.out_file, 'a') as fd:
                                json.dump(msg, fd, indent=2)
                        else:
                            with open(cls.out_file, 'a') as fd:
                                json.dump(msg, fd, indent=2)
                        log.debug('Record added to file.')
                    except Exception as e:
                        data['output'].append({'ERROR: Output file': str(e)})
                        log.error("JSON convert for {0} failed: {1}".format(
                            str(msg),
                            str(e)
                        ))
                else:
                    msg = 'Output file directory "{0}" not found.'.format(
                        cls.out_file
                    )
                    data['output'].append({'ERROR: Output file': msg})

            if cls.out_uri:
                try:
                    if not hasattr(cls, 'es'):
                        cls.es = Elasticsearch([cls.out_uri])
                    cls.es.index('yangsuite', body=msg)
                    log.debug('Record added to Elasticsearch.')
                except Exception as e:
                    data['output'].append({'ERROR: Elasticsearch': str(e)})
                    log.error("Elasticsearch add {0} failed : {1}".format(
                        str(msg),
                        str(e))
                    )

        return data

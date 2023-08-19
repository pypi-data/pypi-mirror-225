# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from yangsuite import get_logger
from ysdevices import YSDeviceProfile
from .grpctelemetry import YSGrpcTelemetryServer

log = get_logger(__name__)


@login_required
def render_main_page(request):
    """Return the main grpctelemetry.html page."""
    devices = YSDeviceProfile.list(require_feature="netconf")
    return render(request, 'ysgrpctelemetry/grpctelemetry.html',
                  {'devices': devices})


@login_required
def start_servicer(request):
    """Start servicer listening on the given port (and IP)."""
    try:
        address = request.POST.get('address', None)
        if address in ['localhost', '127.0.0.1']:
            address = None
        port = request.POST.get('port')
        secure = request.POST.get('secure', None)
        result, message = YSGrpcTelemetryServer.serve(
            address, port, request.user.username, secure,
        )
    except Exception as exc:
        return JsonResponse(
            {},
            status=500,
            reason='Start servicer: ' + str(exc)
        )
    return JsonResponse({'result': result, 'message': message})


@login_required
def stop_servicer(request, port):
    """Stop servicer listening on the given port."""
    try:
        result, message = YSGrpcTelemetryServer.stop(port)
    except Exception as exc:
        return JsonResponse(
            {},
            status=500,
            reason='Stop servicer: ' + str(exc)
        )
    return JsonResponse({'result': result, 'message': message})


@login_required
def get_servicer_list(request):
    servers = []
    for s in YSGrpcTelemetryServer.servers.items():
        if s:
            port, svr = s
            _, _, ip, tls, out_file, out_uri = svr
            servers.append([ip, port, tls, out_file, out_uri])
    fileout = YSGrpcTelemetryServer.out_file
    uri = YSGrpcTelemetryServer.out_uri
    return JsonResponse(
        {"servers": servers, 'fileout': fileout, 'uri': uri}
    )


@login_required
def set_output(request):
    """Set telemetry output destinations."""
    result = {}
    file_output = request.POST.get('file')
    uri = request.POST.get('uri')

    if file_output or uri:
        try:
            YSGrpcTelemetryServer.set_output(file_output, uri)
        except Exception as exc:
            return JsonResponse(
                {},
                status=500,
                reason='Set output: ' + str(exc)
            )
    return JsonResponse(result)


@login_required
def get_output(request):
    """Get the latest output from any given listener stream."""
    try:
        result = YSGrpcTelemetryServer.get_output()
    except Exception as exc:
        return JsonResponse(
            {},
            status=500,
            reason='Get output: ' + str(exc)
        )
    return JsonResponse(result)


@login_required
def get_primary_ip(request):
    """Yangsuite server is primary address to listen on."""
    primary_ip = os.getenv('GRPC_PRIMARY_IP_ADDRESS', 'IP Address')
    return JsonResponse({'address': primary_ip})

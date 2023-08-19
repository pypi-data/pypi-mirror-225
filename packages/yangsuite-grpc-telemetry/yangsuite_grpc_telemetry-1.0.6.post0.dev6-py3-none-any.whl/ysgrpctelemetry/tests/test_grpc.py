import os
import json
import unittest2 as unittest

from ysgrpctelemetry.grpctelemetry import YSGrpcTelemetryServer


BASE_DIR = os.path.dirname(__file__)


class TestGrpcClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.msg = {
            "timestamp": "2023 Aug 17 16:31:00:992000",
            "subscription": "7",
            "node": "ddmi-9500-2",
            "subscribe_path": "/Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization",  # noqa
            "fields": [
                {
                    "child_path": "/",
                    "name": "five-seconds",
                    "value": 0
                }
            ]
        }
        cls.logfile = os.path.join(BASE_DIR, 'fileout.log')

    def tearDown(self):
        if os.path.isfile(self.logfile):
            os.remove(self.logfile)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_set_output_file(self):
        """Make sure file output is set."""
        json.dump(self.msg, open(self.logfile, 'w'))
        YSGrpcTelemetryServer.set_output(self.logfile)
        self.assertTrue(
            YSGrpcTelemetryServer.out_file == self.logfile
        )

    def test_set_output_uri(self):
        """Make sure ElasticSearch uri is set."""
        YSGrpcTelemetryServer.set_output(uri='http://localhost:9200')
        self.assertTrue(
            YSGrpcTelemetryServer.out_uri == 'http://localhost:9200'
        )

    def test_get_output_file(self):
        "Verify output file receives msg"
        with open(self.logfile, 'w') as fd:
            fd.write('')
        YSGrpcTelemetryServer.set_output(self.logfile)
        YSGrpcTelemetryServer.stdout_queue.append(self.msg)
        data = YSGrpcTelemetryServer.get_output()
        file_data = json.load(open(self.logfile))

        self.assertTrue(data['output'][0] == self.msg)
        self.assertTrue(file_data == self.msg)

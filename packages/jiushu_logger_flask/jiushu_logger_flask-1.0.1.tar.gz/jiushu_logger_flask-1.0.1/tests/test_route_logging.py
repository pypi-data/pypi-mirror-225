# coding: utf-8
from time import sleep
from unittest import TestCase

import orjson
from flask import Flask, g
from flask_unittest import ClientTestCase
from jiushu_logger import Logger
from werkzeug.test import EnvironBuilder

from jiushu_logger_flask import RouteLogging


def _create_app():
    app = Flask(__name__)
    RouteLogging(app,
                 skip_routes=['/api/health'],
                 skip_regexes=[r'''^.*skip.*$'''])

    @app.get('/api/test')
    def _test():
        return g.trace_id.encode('utf_8'), 200

    @app.get('/api/test2')
    def _test2():
        sleep(1.23456)
        return orjson.dumps({'result': True}), 200, {'Content-Type': 'application/json'}

    @app.get('/api/should-be-skip')
    def _should_be_skip():
        return b'Hello, world!', 200

    @app.get('/api/health')
    def _health():
        return orjson.dumps({'status': 'UP'}), 200, {'Content-Type': 'application/json'}

    return app


class RouteLoggingTest(ClientTestCase, TestCase):
    app = _create_app()

    def test_route_logging(self, client):
        with self.assertLogs(Logger.req) as captured:
            rv = client.get('/api/test')
            trace_id = g.trace_id

            client.get(EnvironBuilder(
                path='/api/test2',
                query_string={'a': '1'},
                headers=[('My-Header', 'My-Value')],
                json={'b': '2'},
            ))

        self.assertEqual(rv.get_data(), trace_id.encode('utf_8'))
        record = captured.records[0]
        self.assertEqual(record.body, "b''")
        self.assertTrue(isinstance(record.duration, int))
        self.assertEqual(record.path, '/api/test')
        self.assertEqual(record.query, '{}')
        self.assertEqual(record.name, 'jf_service_req')

        record = captured.records[1]
        self.assertEqual(record.body, '{"b":"2"}')
        self.assertTrue(isinstance(record.duration, int))
        self.assertEqual(record.path, '/api/test2')
        self.assertEqual(record.query, '{"a":"1"}')

    def test_skip(self, client):
        with self.assertRaises(AssertionError):
            with self.assertLogs(Logger.req):
                client.get('/api/should-be-skip')
                client.get('/api/health')

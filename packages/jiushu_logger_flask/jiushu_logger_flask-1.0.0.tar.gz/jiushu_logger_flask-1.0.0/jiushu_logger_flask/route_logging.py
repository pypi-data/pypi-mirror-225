# coding: utf-8
import re
import typing
from itertools import chain
from time import perf_counter

import orjson
from flask import Flask, request, Response, g
from jiushu_logger import Logger, ReqLogExtra
from ulid import ULID

from ._helpers import *

try:
    import skywalking
    from skywalking.trace.context import get_context
except:
    skywalking = NotImplemented

__all__ = ['RouteLogging']


def _get_headers():
    headers = dict(request.headers.items())
    for key in ENV_HEADERS:
        if key in headers:
            del headers[key]
    return headers


class RouteLogging:
    def __init__(self,
                 app: Flask,
                 *,
                 skip_routes: typing.Sequence[str] = None,
                 skip_regexes: typing.Sequence[str] = None):
        self._skip_routes = skip_routes or []
        self._skip_regexes = (
            [re.compile(regex) for regex in skip_regexes]
            if skip_regexes
            else [])
        app.before_request(self._before_request_func)
        app.after_request(self._after_request_func)

    def __should_route_be_skipped(self, request_route: str) -> bool:
        return any(chain(
            iter(True for route in self._skip_routes if request_route.startswith(route)),
            iter(True for regex in self._skip_regexes if regex.match(request_route)),
        ))

    def _before_request_func(self):
        # Try to get apache-skywalking trace id. If error, use uuid
        try:
            g.trace_id = str(get_context().segment.segment_id)
        except:
            g.trace_id = ULID().hex
        g.begin_time = perf_counter()

    def _after_request_func(self, response: Response):
        # DO NOT output logs for the route which should be skipped
        if self.__should_route_be_skipped(request.path):
            pass

        else:
            # request body
            data = request.data
            form = request.form.to_dict()
            try:
                json_ = orjson.loads(data)
            except:
                json_ = None

            if json_ is None:
                if form:
                    body = form
                else:
                    body = data
            else:
                body = json_

            # response body
            try:
                resp = orjson.loads(response.get_data())
            except:
                resp = response.get_data()

            Logger.req.info(
                None,
                extra=ReqLogExtra(
                    trace_id=g.trace_id,
                    duration=perf_counter() - g.begin_time,
                    method=request.method,
                    path=request.path,
                    client_ip=request.headers.get('X-Forwarded-For', request.remote_addr),
                    host=request.host,
                    headers=safely_jsonify(_get_headers()),
                    query=safely_jsonify(request.args.to_dict()),
                    body=safely_jsonify(body),
                    resp=safely_jsonify(resp)
                )
            )

        response.headers.setdefault('X-Request-Id', g.trace_id)
        return response

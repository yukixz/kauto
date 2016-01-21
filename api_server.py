#!/usr/bin/env python3

import json
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

import config


class Request():
    path = None
    _body = None

    def __init__(self, path, body=None):
        self.path = path
        self.body = body

    def __str__(self):
        return '''Request(path="%s")''' % self.path

    @property
    def body(self):
        if type(self._body) is str:
            body = None
            try:
                body = json.loads(self._body)
                self._body = body
            finally:
                return body
        else:
            return self._body

    @body.setter
    def body(self, body):
        self._body = body


class APIServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # self.log_request()
        try:
            APIServer.REQUESTS_LOCK.acquire()
            APIServer.REQUESTS.append(Request(self.path))
        finally:
            APIServer.REQUESTS_LOCK.release()
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        # self.log_request()
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        try:
            APIServer.REQUESTS_LOCK.acquire()
            APIServer.REQUESTS.append(Request(self.path, body))
        finally:
            APIServer.REQUESTS_LOCK.release()
        self.send_response(200)
        self.end_headers()

    # override
    def send_response(self, code, message=None):
        """ Override to avoid log_request() on each response
        """
        self.send_response_only(code, message)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())

    # override
    def log_request(self, message=''):
        self.log_message("%s %s - %s",
                         self.command, self.path, message)

    # override
    def log_message(self, format, *args):
        sys.stderr.write("[%s] %s\n" %
                         (self.log_date_time_string(),
                          format % args))


class APIServer():
    REQUESTS = []
    REQUESTS_LOCK = threading.Lock()

    def __init__(self):
        self.httpd = HTTPServer(config.host, APIServerHandler)
        self.threaded_httpd = threading.Thread(target=self.httpd.serve_forever)
        self.threaded_httpd.daemon = True
        self.threaded_httpd.start()
        print("Threaded API server listening on %s:%d" % config.host)

    def wait(self, path):
        ''' Wait for specified API request.
            User can use Control-C to break this wait
            @param  API path
            @return Request object
        '''
        if type(path) not in [list, tuple]:
            path = (path,)
        print("wait: %s" % path[0])

        request = None
        while True:
            if len(APIServer.REQUESTS) > 0:
                try:
                    APIServer.REQUESTS_LOCK.acquire()
                    request = APIServer.REQUESTS.pop(0)
                finally:
                    APIServer.REQUESTS_LOCK.release()
                if request.path in path:
                    break
            else:
                time.sleep(0.2)
        return request

    def empty(self):
        try:
            APIServer.REQUESTS_LOCK.acquire()
            del APIServer.REQUESTS[:]
        finally:
            APIServer.REQUESTS_LOCK.release()

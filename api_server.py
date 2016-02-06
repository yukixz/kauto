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

    def __init__(self, raw_data):
        # Throw exception to parent
        data = json.loads(raw_data)
        self.method = data["method"]
        self.path = data["path"]
        self.body = data["body"]
        self.post_body = data["postBody"]
        print(self)

    def __str__(self):
        return '''Request(path="%s")''' % self.path


class APIServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        try:
            APIServer.REQUESTS_LOCK.acquire()
            APIServer.REQUESTS.append(Request(body))
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


api_server = APIServer()

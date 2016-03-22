#!/usr/bin/env python3

import json
import math
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

import config


REQUESTS = []
REQUESTS_LOCK = threading.Lock()


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
            REQUESTS_LOCK.acquire()
            REQUESTS.append(Request(body))
        finally:
            REQUESTS_LOCK.release()
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
    SLEEP_INTERVAL = 0.1

    def __init__(self):
        self.httpd = HTTPServer(config.host, APIServerHandler)
        self.threaded_httpd = threading.Thread(target=self.httpd.serve_forever)
        self.threaded_httpd.daemon = True
        self.threaded_httpd.start()
        print("Threaded API server listening on %s:%d" % config.host)

    def wait(self, path, timeout=86400, keep=False):
        ''' Wait for specified API request.
        '''
        if type(path) in [list, tuple]:
            paths = path
        else:
            paths = (path, )
        timeout_limit = math.ceil(timeout / self.SLEEP_INTERVAL)
        timeout_count = 1

        print("wait: %s" % paths[0])
        while True:
            if len(REQUESTS) == 0:
                if timeout_count > timeout_limit:
                    return None
                timeout_count += 1
                time.sleep(self.SLEEP_INTERVAL)
                continue
            try:
                REQUESTS_LOCK.acquire()
                request = REQUESTS.pop(0)
                print(request)
                if request.path in paths:
                    if keep:
                        REQUESTS.insert(0, request)
                    return request
            finally:
                REQUESTS_LOCK.release()

    def flush(self):
        try:
            REQUESTS_LOCK.acquire()
            del REQUESTS[:]
        finally:
            REQUESTS_LOCK.release()

    def empty(self):
        return self.flush()


api_server = APIServer()

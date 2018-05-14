#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import re
import json

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.routes = {
            r'^/api/vm': {'media_type': 'application/json'},
            r'^/records$': {'file': 'GET', 'media_type': 'application/json'}}

        return BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_HEAD(self):
        self.handle_method('HEAD')

    def do_POST(self):
        self.handle_method('POST')

    def do_PUT(self):
        self.handle_method('PUT')

    def do_DELETE(self):
        self.handle_method('DELETE')

    # GET
    def do_GET(self):
        self.handle_method('GET')


    def handle_method(self, method):
        route = self.get_route()
        if route is None:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Route not found\n')

        elif 'file' in route:
            if method == 'GET':
                self.send_response(200)
                self.send_header('Content-type', "application/json")
                self.end_headers()
                process = subprocess.check_output('ls /var/', shell=True)
                # response = {"status": True, "message": "success"}
                return self.wfile.write(process)

        else:
            if method == 'HEAD':
                self.send_response(200)
                if 'media_type' in route:
                    self.send_header('Content-type', route['media_type'])
                self.end_headers()
            else:
                if method == 'GET':
                    self.send_response(200)
                    self.send_header('Content-type', "application/json")
                    self.end_headers()
                    proc = subprocess.check_output('ls /etc/', shell=True)
                    #response = {"status": True, "message": "success"}
                    return self.wfile.write(proc)
                if method == 'POST':
                    self.send_response(200)
                    self.send_header('Content-type', "application/json")
                    self.end_headers()
                    response = {"status": True, "message": "success1"}
                    return self.wfile.write(json.dumps(response))
                if method == 'PUT':
                    self.send_response(200)
                    self.send_header('Content-type', "application/json")
                    self.end_headers()
                    response = {"status": True, "message": "success"}
                    return self.wfile.write(json.dumps(response))
                if method == 'DELETE':
                    self.send_response(200)
                    self.send_header('Content-type', "application/json")
                    self.end_headers()
                    response = {"status": True, "message": "success"}
                    return self.wfile.write(json.dumps(response))
                else:
                    self.send_response(405)
                    self.send_header('Content-type', "application/json")
                    self.end_headers()
                    response = {"status": True, "message": "Unsupport Method"}
                    return self.wfile.write(json.dumps(response))

    def get_route(self):
        for path, route in self.routes.items():
            print(route)
            print(path)
            if re.match(path, self.path):
                return route
        return None




def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()
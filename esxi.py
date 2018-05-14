#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import re
import shlex
import json


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.routes = {
            r'^/api/vm/list': {'file': 'GET', 'media_type': 'application/json'},
            r'^/records$': {'media_type': 'application/json'}}

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
                #process = subprocess.check_output('df', shell=True)
                vm_array = [shlex.split(x) for x in subprocess.check_output(['df']).decode('utf8').rstrip().split('\n')]
                ids = vm_array[0]
                vm_json = { }
                vm_json["filesystem"] = []
                vm_num_lines = vm_array[:].__len__()
                for row in range(1, vm_num_lines):
                    vm_json["filesystem"].append(self.vm_to_json(vm_array[row]))
                print(json.dumps(vm_json, sort_keys=True, indent=2))
                #print(json.dumps(vm_json, sort_keys=True, indent=2))
                # response = {"status": True, "message": "success"}
                return self.wfile.write(json.dumps(vm_json, sort_keys=True, indent=2))
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
                print(self.path)
                return route
        return None

    def vm_to_json(tokenList):
        """Take a list of tokens from df and return a python object."""
        # If df's ouput format changes, we'll be in trouble, of course.
        # the 0 token is the name of the filesystem
        # the 1 token is the size of the filesystem in 1K blocks
        # the 2 token is the amount used of the filesystem
        # the 5 token is the mount point
        result = {}
        fsName = tokenList[0]
        fsSize = tokenList[1]
        fsUsed = tokenList[2]
        fsMountPoint = tokenList[5]
        result["filesystem"] = {}
        result["filesystem"]["name"] = fsName
        result["filesystem"]["size"] = fsSize
        result["filesystem"]["used"] = fsUsed
        result["filesystem"]["mount_point"] = fsMountPoint
        return result




def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()
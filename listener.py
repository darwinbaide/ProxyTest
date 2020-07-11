#!/usr/bin/env python3

import http.server as SimpleHTTPServer
import socketserver as SocketServer
import logging, requests , pprint

PORT = 8000

class GetHandler(
        SimpleHTTPServer.SimpleHTTPRequestHandler
        ):

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        
    def do_GET(self):
        print("\n\n\n------------Get Requests Received-------------")
        print("Website: "+str(self.path  ))
        print("Website Host: "+str(self.headers["Host"]))
        websiteTarget=str(self.path  )# this is the requested site
        proxies = {'http' : 'http://127.0.0.1:8000/' }# this is the proxy list for target
        r = requests.get(websiteTarget)
        """print(r.content)
        print(r.cookies)
        print(r.elapsed)
        print(r.encoding)
        print(r.headers)
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header('Content-type',    'text/html')                                    
        self.end_headers()              
        self.wfile.write(str.encode("<html><body>Hello worldww!</body></html>"))
        self.connection.shutdown(1) 
        
        print("------------End of Requests-------------\n\n\n")


Handler = GetHandler
httpd = SocketServer.TCPServer(('127.0.0.1', PORT), Handler)
try:
    print("Starting to listen")
    httpd.serve_forever()

   
except KeyboardInterrupt:
    pass
    print("Closing out")
    httpd.server_close()
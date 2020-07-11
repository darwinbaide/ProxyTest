#!/usr/bin/env python3

import http.server as SimpleHTTPServer
import socketserver as SocketServer
import logging, requests , pprint
import config


PORT = 9000


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def set_header(hostname):
    headers = {
        'Host': hostname
    }

    return headers


class GetHandler(
        SimpleHTTPServer.SimpleHTTPRequestHandler
        ):

  
    def do_HEAD(self):
        self.do_GET(body=False)

    def do_GET(self, body=True):
        print("------------------------Start------------------------")
        hostname= str(self.headers["Host"])
        sent = False
        print("Hostname:  "+hostname)
        try:

            url=str(self.path  )
            req_header = self.parse_headers()
            
            pprint.pprint(req_header)
            print("Website: "+url)
            resp = requests.get(url, headers=merge_two_dicts(req_header, set_header(hostname)), verify=False)
            sent = True
            

            self.send_response(resp.status_code)
            print("status code: "+str(resp.status_code))
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)# if it has a return body
            return
        finally:
            self.connection.close()
            self.finish()
            
            print("At the End")
            if not sent:
                print("------------------------ End ------------------------")
                self.send_error(404, 'error trying to proxy')
            print("------------------------ End ------------------------")

    def do_POST(self, body=True):
        hostname= str(self.headers["Host"])
        print("In the post \n\n\n\n")
        print(hostname)
        sent = False
        try:
            url = 'https://{}{}'.format(hostname, self.path)
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            req_header = self.parse_headers()

            resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, set_header(hostname)), verify=False)
            sent = True

            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
            return
        finally:
            self.finish()
            if not sent:
                self.send_error(404, 'error trying to proxy')

    """ def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>") """


    def do_CONNECT(self, body=True):
        print("------------------------Start------------------------")
        hostname= str(self.headers["Host"])
        
        print("Hostname:  "+hostname)




        url = 'https://{}'.format( self.path)
        req_header = self.parse_headers()
        print("1:"+str(self.client_address))
        print("2:"+str(self.command))
        
        #pprint.pprint(self.headers.__dict__)
        
        print("6:"+str(self.path))
        
        
        
        print("10:"+str(self.requestline))
        print("11:"+str(self.responses))
      
        print("16:"+str(self.address_string.__dict__))
     
        
        
        print("Website: "+url)
        
        
        
        
        
        
        exit()# this breaks when it gerts here

      
        

        self.send_response(100)
        #print("status code: "+str(resp.status_code))
        print("Website: "+url)
        return
        
        try:

            url=str(self.path  )
            req_header = self.parse_headers()
            
            pprint.pprint(req_header)
            print("Website: "+url)
            #resp = requests.get(url, headers=merge_two_dicts(req_header, set_header(hostname)), verify=False)
            sent = True
            

            self.send_response(100)
            print("status code: "+str(resp.status_code))
            #self.send_resp_headers(resp)
            
        finally:
            self.connection.close()
            self.finish()
            
            
            print("------------------------ End ------------------------")


    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        
        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
            return
        if not self.raw_requestline:
            self.close_connection = 1
            return
        if not self.parse_request():
            # An error code has been sent, just exit
            return
        mname = 'do_' + self.command
        if not hasattr(self, mname):
            self.send_error(501, "Unsupported method (%r)" % self.command)
            return
        method = getattr(self, mname)
        method()
        print(self.close_connection)
        print()
        #self.wfile.flush() #actually send the response if not already done.
        self.wfile.close()
        self.rfile.close()
    


    def parse_headers(self):
        req_header = {}
        for line in self.headers:
            print("H: "+str(line))
            line_parts = [o.strip() for o in line.split(':', 1)]
            if len(line_parts) == 2:
                req_header[line_parts[0]] = line_parts[1]
        return req_header

    def send_resp_headers(self, resp):
        respheaders = resp.headers
        print ('Response Header')
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                #print (key, respheaders[key])
                self.send_header(key, respheaders[key])
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()

def RunListen():
    Handler = GetHandler
    httpd = SocketServer.TCPServer((config.socketURL, config.PORT), Handler)
    try:
        print("Starting to listen")
        httpd.serve_forever()

    
    except KeyboardInterrupt:
        pass
        print("Closing out")
        httpd.server_close()



if __name__ == '__main__':
    RunListen()
import argparse
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from typing import List

class RequestFilter:

    def validate(self, handler: BaseHTTPRequestHandler) -> bool:
        return True

class DenyAllFilter(RequestFilter):

    def validate(self, handler: BaseHTTPRequestHandler) -> bool:
        return False       

class IosSimulatorFilter(RequestFilter):

    def validate(self, handler: BaseHTTPRequestHandler) -> bool:
        try:
            if re.search('^CFNetworkAgent.*CFNetwork.*Darwin.*\d$', handler.headers['User-Agent']):
                return True
            else:
                return False    
        except:
            return False 

class CompositeRequestFilter(RequestFilter):

    def __init__(self, filters: List[RequestFilter]) -> None:
        super().__init__()
        self.filters = filters;

    def validate(self, handler: BaseHTTPRequestHandler) -> bool:
        for filter in self.filters:
            if filter.validate(handler=handler):
                return True
        return False        

filter = RequestFilter();

class AutoProxyServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/x-ns-proxy-autoconfig')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()

    def _autoproxy_string(self, host, port, proxy):
        content = "function FindProxyForURL(url, host) {{ return \"{proxy} {host}:{port}; DIRECT\"; }}".format(host=host, port=port, proxy=proxy)

        return content.encode("utf8")

    def do_GET(self):
        try:
            if filter.validate(handler=self):
                self._set_headers()
                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))

                requested_port = query_components['port']
                requested_host = query_components['host']
                requested_protocol = None

                try:
                    requested_protocol = query_components['proxy']
                except:
                    requested_protocol = 'PROXY'

                self.wfile.write(self._autoproxy_string(host=requested_host, port=requested_port, proxy=requested_protocol))
            else:
                self.send_response(502)
                self.wfile.write('Request doesn\'t satisfy any configured filters'.encode('utf8'))                    
        except:
            self.send_response(502)
            self.wfile.write('Error while handling request'.encode('utf8'))


    def do_HEAD(self):
        self._set_headers()


def run(server_class=HTTPServer, addr="localhost", port=8000):
    httpd = HTTPServer((addr, port), AutoProxyServer)

    print("Starting httpd server on {addr}:{port}".format(addr=addr, port=port))

    httpd.serve_forever()

def pyautoproxy():    
    parser = argparse.ArgumentParser(description='Configurable autoproxy')
    parser.add_argument(
        '-l',
        '--listen',
        default="localhost",
        required=False,
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        '-p', 
        '--port', 
        type=int, 
        default='8081', 
        required=False, 
        help='Specify the port on which the server listens')

    parser.add_argument(
        '-s',
        '--simulator',
        action='store_true',
        default=False,
        required=False,
        help='Send proxy configuration only to requests from iOS simulator'
    )    

    args = parser.parse_args()

    if args.simulator:
        filter = CompositeRequestFilter(filters= [
            DenyAllFilter(),
            IosSimulatorFilter()
        ])

    run(addr=args.listen, port=args.port)

if __name__ == "__main__":
    pyautoproxy()

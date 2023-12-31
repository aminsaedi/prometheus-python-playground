import http.server
from prometheus_client import start_http_server, Histogram


LATENCY = Histogram("hello_world_latency_seconds", "Description of histogram")


class MyHandler(http.server.BaseHTTPRequestHandler):
    @LATENCY.time()
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World - No CI 7")


if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(("0.0.0.0", 8080), MyHandler)
    server.serve_forever()

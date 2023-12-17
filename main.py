import http.server
from prometheus_client import start_http_server, Counter
from random import random


TOTAL_REQUESTS = Counter(
    "hello_worlds_total", "Hello Worlds requested of the HTTP server."
)

TOTAL_EXCEPTIONS = Counter(
    "hello_worlds_exceptions_total",
    "Exceptions serving Hello World.",
    ["exception"],
)


class MyHandler(http.server.BaseHTTPRequestHandler):
    @TOTAL_EXCEPTIONS.count_exceptions()
    def do_GET(self):
        TOTAL_REQUESTS.inc()
        if random() < 0.2:
            raise Exception
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World - No CI 7")


if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(("0.0.0.0", 8080), MyHandler)
    server.serve_forever()

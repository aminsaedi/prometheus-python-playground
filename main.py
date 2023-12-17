import http.server
from prometheus_client import start_http_server, Counter, Gauge, Summary
import time


TOTAL_REQUESTS = Counter(
    "hello_worlds_total", "Hello Worlds requested of the HTTP server."
)


IN_PROGRESS = Gauge(
    "hello_worlds_in_progress",
    "Hello Worlds in progress.",
)

LAST = Gauge(
    "hello_worlds_last_time_seconds",
    "The last time a Hello World was served.",
)

LATENCY = Summary(
    "hello_worlds_latency_seconds",
    "Time for a request Hello World.",
)


class MyHandler(http.server.BaseHTTPRequestHandler):
    @IN_PROGRESS.track_inprogress()
    def do_GET(self):
        start = time.time()
        TOTAL_REQUESTS.inc()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World - No CI 7")
        LATENCY.observe(time.time() - start)
        LAST.set_to_current_time()


if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(("0.0.0.0", 8080), MyHandler)
    server.serve_forever()

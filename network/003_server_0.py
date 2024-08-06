from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)  # 간단한 서버를 만들 수 있는 모듈
from urllib.parse import urlparse, parse_qs


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # get 요청 처리
        parsed_url = urlparse(self.path)  # URL 파싱
        query_params = parse_qs(parsed_url.query)  # 쿼리 파싱

        # hello world라고 응답
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, world!")


if __name__ == "__main__":
    # 나를 직접 실행시키는 경우에만 실행을 시키겠다는 의미
    # 나를 직접 실행시키지 않고 모듈로 불러오면 아래코드가 실행 안됨
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server running on port {server_address[1]}")
    httpd.serve_forever()

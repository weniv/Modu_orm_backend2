from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)  # 간단한 서버를 만들 수 있는 모듈
from urllib.parse import urlparse, parse_qs


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # get 요청 처리
        parsed_url = urlparse(self.path)  # URL 파싱
        query_params = parse_qs(parsed_url.query)  # 쿼리 파싱
        print(self.path)  # str
        print(type(self.path))
        print(parsed_url)  # ParseResult
        print(type(parsed_url))
        print(query_params)  # dict
        print(type(query_params))
        # 다시 나에게 데이터를 준 브라우저에게 응답을 주지 않았으므로
        # 브라우저는 기다리다가 페이지가 동작하지 않습니다를 띄움

        # 사용자에게 응답 전달
        self.send_response(200)
        # self.send_response(404)
        # 이 응답 코드는 숫자일 뿐입니다.
        # 그렇기에 이 응답코드를 정보보안 차원에서 제대로 주지 않는 경우도 많습니다.
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello World")


if __name__ == "__main__":
    # 나를 직접 실행시키는 경우에만 실행을 시키겠다는 의미
    # 나를 직접 실행시키지 않고 모듈로 불러오면 아래코드가 실행 안됨
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server running on port {server_address[1]}")
    httpd.serve_forever()

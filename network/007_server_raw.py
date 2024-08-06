import http.server
import socketserver
import json


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        raw_data = self.get_raw_request_data()
        print("Raw GET request data:")
        print(raw_data)
        # 실제로는 아래와 같이 파싱된 데이터를 사용하게 됩니다.
        # parsed_url = urlparse(self.path)
        # query_params = parse_qs(parsed_url.query)
        # response_data = {
        #     'method': 'GET',
        #     'path': self.path,
        #     'headers': dict(self.headers),
        #     'query_params': query_params,
        #     'raw_data': f"GET {self.path} {self.protocol_version}\n{self.headers}"
        # }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Success"}).encode("utf-8"))

    def do_POST(self):
        raw_data = self.get_raw_request_data()
        print("Raw POST request data:")
        print(raw_data)

        # 실제로는 아래와 같이 파싱된 데이터를 사용하게 됩니다.
        # content_length = int(self.headers['Content-Length'])
        # post_data = self.rfile.read(content_length).decode('utf-8')

        # response_data = {
        #     'method': 'POST',
        #     'path': self.path,
        #     'headers': dict(self.headers),
        #     'post_data': post_data,
        #     'raw_data': f"POST {self.path} {self.protocol_version}\n{self.headers}\n\n{post_data}"
        # }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Success"}).encode("utf-8"))

    def get_raw_request_data(self):
        raw_data = f"{self.command} {self.path} {self.request_version}\n"
        raw_data += str(self.headers)

        content_length = self.headers.get("Content-Length")
        if content_length:
            body = self.rfile.read(int(content_length)).decode("utf-8")
            raw_data += f"\n\n{body}"

        return raw_data


PORT = 8000

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()

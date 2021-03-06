import socket
from urllib.parse import quote
import ssl

AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
CONTENT = "application/x-www-form-urlencoded"


class Request:
    def __init__(self, host, uri='/', port=80, https=False, request_type="POST", agent=AGENT, content_type=CONTENT, parameters={}):
        self.host = host
        self.uri = uri
        self.port = port
        self.agent = agent
        self.request_type = request_type
        self.content_type = content_type
        self.parameters = parameters
        self.https = https

        self.redirects = 0

        self.main()

    def main(self):
        self.generate_request()
        self.generate_socket()
        self.send_request()
        self.receive_response()
        self.parse_headers()
        self.redirect()

    def redirect(self):
        if self.parsed_headers['type'] in ('301', '302'):
            location = self.parsed_headers['Location']
            location = location.split('//')[1]
            host, uri = location.split('/', 1)
            self.host = host
            self.uri = '/' + uri
            self.redirects += 1
            print(f'[+] Redirect to {self.parsed_headers["Location"]}')
            if self.redirects < 16:
                self.main()

    def receive_response(self):
        data = b''
        response_part = self.sock.recv(4096)
        while response_part != b'':
            data += response_part
            try:
                response_part = self.sock.recv(4096)
            except:
                break
        self.raw = data
        self.response = data.decode()
        self.headers, self.text = data.decode().split('\r\n\r\n', 1)
        self.text = self.text[:-1]

    def parse_headers(self):
        headers = self.headers.split('\r\n')
        self.parsed_headers = {"type": headers[0].split()[1]}
        for header in headers[1:]:
            key, value = header.split(": ", 1)
            self.parsed_headers[key] = value

    def send_request(self):
        self.sock.sendall(self.request.encode())

    def generate_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.https:
            self.context = ssl.create_default_context()
            self.sock = self.context.wrap_socket(
                self.sock, server_hostname=self.host)
        self.sock.settimeout(2)
        self.sock.connect((self.host, self.port))

    def generate_request(self):
        if self.content_type == 'application/x-www-form-urlencoded' and type(self.parameters) == type(dict()):
            self.parameters = '&'.join('{}={}'.format(quote(key), quote(
                value)) for key, value in self.parameters.items())

        self.request = f'{self.request_type} {self.uri} HTTP/1.1\r\n'
        self.request += f'Host: {self.host}\r\n'
        self.request += f'User-agent: {self.agent}\r\n'
        self.request += f'Accept: text/html\r\n'
        self.request += f'Accept-Language: en-US\r\n'
        self.request += f'Accept-Encoding: text/html'
        self.request += f'Connection: close'
        self.request += f'Content-Type: {self.content_type}\r\n'
        self.request += f'Content-Length: {len(self.parameters)}\r\n'
        self.request += f'\r\n'
        self.request += f'{self.parameters}'


if __name__ == '__main__':
    request = Request(
        'www.rit.edu', '/study/computing-security-bs', port=443, https=True)

    with open('test.html', 'w') as f:
        f.write(request.text)

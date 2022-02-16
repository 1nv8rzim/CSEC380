from curses import raw
import socket
from urllib.parse import quote
import ssl
from threading import Thread
from queue import Queue
from bs4 import BeautifulSoup

AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
CONTENT = "application/x-www-form-urlencoded"


class Request:
    def __init__(self, url, port=None, https=False, request_type="POST", agent=AGENT, content_type=CONTENT, parameters={}, decode=True):
        self.host, self.uri = url.split('/', 1)
        self.uri = f'/{self.uri}'

        if port is not None:
            self.port = port
        elif https:
            self.port = 443
        else:
            self.port = 80

        self.agent = agent
        self.request_type = request_type
        self.content_type = content_type
        self.parameters = parameters
        self.https = https
        self.decode = decode

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
            if not location.startswith('http'):
                self.uri = '/' + location
            else:
                location = location.split('//')[1]
                self.host, uri = location.split('/', 1)
                self.uri = '/' + uri
            self.redirects += 1
            print(f'[+] Redirect to {self.host}{self.uri}')
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
        if self.decode:
            self.response = data.decode()
            self.headers, self.text = data.decode().split('\r\n\r\n', 1)
            self.text = self.text[:-1]
        else:
            self.headers, self.text = data.split(b'\r\n\r\n', 1)
            self.headers = self.headers.decode()

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
        self.sock.settimeout(3)
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


class ImageDownload:
    def __init__(self, urls, threads=5, folder='.'):
        self.urls = urls
        self.threads = threads
        self.folder = folder

        self.main()

    def url_generator(self):
        for url in self.urls:
            yield url
        for _ in range(self.threads):
            yield None

    def main(self):
        urls_gen = self.url_generator()
        for _ in range(self.threads):
            thread = self.ImageDownloadThread(urls_gen, self.folder)
            thread.start()
        thread.join()

    class ImageDownloadThread(Thread):
        def __init__(self, urls, folder="."):
            Thread.__init__(self)
            self.urls = urls
            self.folder = folder
            self.url = next(self.urls)

        def run(self):
            while self.url:
                self.main()
                self.url = next(self.urls)

        def main(self):
            self.get_raw_image()
            if self.request.parsed_headers['type'] not in ('400'):
                self.write_file()

        def get_raw_image(self):
            self.request = Request(self.url, https=True,
                                   port=443, decode=False)

        def write_file(self):
            name = self.url.split('&UN=')[1].split('&HASH')[0]
            with open(f'{self.folder}/{name}.jpg', 'wb') as image:
                image.write(self.request.text)


class WebCrawlerThread(Thread):
    def __init__(self, domain, urls, port=None, https=False):
        Thread.__init__(self)
        self.domain = domain
        self.urls = urls
        self.port = port
        self.https = https

    def get_addresses(self, request):
        links = []
        good_soup = BeautifulSoup(request)
        for a in good_soup.find_all('a'):
            links.append(a.get('href'))
        for link in links:
            print(link)

    def main(self):
        while not self.urls.empty():
            url = self.urls.get()
            request = Request(url, https=self.https, port=self.port)
            self.get_addresses(request.text)


queue = Queue()
queue.put("www.rit.edu")
WebCrawlerThread("rit.edu", queue, https=True)

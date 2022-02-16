import socket
from urllib.parse import quote
import ssl
from threading import Thread
from queue import Queue
from bs4 import BeautifulSoup
from re import match
from multiprocessing import Process

AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
CONTENT = "application/x-www-form-urlencoded"
URL_RE = '(?:www\.|(?!www)[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'


class Request:
    def __init__(self, url, port=None, https=False, request_type="POST", agent=AGENT, content_type=CONTENT, parameters={}, decode=True):
        try:
            self.host, self.uri = url.split('/', 1)
        except:
            self.host = url
            self.uri = ''
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

        self.failures = 0
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
            if self.redirects < 16:
                self.main()

    def receive_response(self):
        data = b''
        ignore = False
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
        self.sock.settimeout(2)
        try:
            self.sock.connect((self.host, self.port))
        except:
            print('[-] Failure: restarting binding')
            self.failures += 1
            if self.failures > 5:
                self.generate_socket()

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


class WebCrawler:
    def __init__(self, domain, port=None, https=False, depth=1, threads=10, processes=2, path=''):
        self.domain = domain
        self.port = port
        self.https = https
        self.depth = depth
        self.threads = threads
        self.path = path
        self.processes = processes

        self.main()

    def main(self):
        self.queue = Queue()
        self.queue.put((self.domain, 0))
        self.all_urls = set()
        self.all_urls.add(self.domain)
        self.emails = set()

        thread = self.WebCrawlerThread(self.domain, self.queue, self.all_urls, self.emails,
                                       https=True, init=True, depth=self.depth)
        thread.start()
        thread.join()

        processes = []

        for _ in range(self.processes):
            processes.append(Process(target=self.start_threads()))
            processes[-1].start()

        for process in processes:
            if process.is_alive():
                process.join()

        with open(self.path + f'emails_d{self.depth}.txt', 'w') as f:
            for email in self.emails:
                f.write(email + '\n')

    def start_threads(self):
        threads = []
        for _ in range(self.threads):
            threads.append(self.WebCrawlerThread(
                self.domain, self.queue, self.all_urls, self.emails, https=True, depth=self.depth))
            threads[-1].start()

        for thread in threads:
            if thread.is_alive():
                thread.join()

    class WebCrawlerThread(Thread):
        def __init__(self, domain, urls, all_urls, emails, port=None, https=False, depth=1, init=False):
            Thread.__init__(self)
            self.domain = domain
            self.urls = urls
            self.port = port
            self.https = https
            self.all_urls = all_urls
            self.depth = depth
            self.init = init
            self.emails = emails

        def get_addresses(self, request, depth):
            hrefs = []
            good_soup = BeautifulSoup(request, 'html.parser')

            for a in good_soup.find_all('a'):
                hrefs.append(a.get('href'))

            links = []

            for href in hrefs:
                if href is None:
                    continue
                elif href.startswith('#'):
                    continue
                href = href.split('#')[0]
                if href.startswith('/'):
                    links.append(self.domain + href[1:])
                    continue
                elif href.startswith('https://'):
                    links.append(href[8:])
                    continue
                elif href.startswith('http://'):
                    links.append(href[7:])
                    continue
                elif match(URL_RE, href):
                    links.append(href)
                elif '@' in href:
                    if '?' in href:
                        href = href.split('?')[0]
                    if '\r\n' in href:
                        href = href.split('\r\n')
                        href = href[0] + href[-1]
                    self.emails.add(href)

            if self.depth <= depth + 1:
                for link in links:
                    self.all_urls.add(link)
            else:
                for link in links:
                    if link in self.all_urls:
                        continue
                    elif link.split('/')[0].endswith(self.domain[:-1]):
                        self.all_urls.add(link)
                        self.urls.put((link, depth + 1))
                    else:
                        self.all_urls.add(link)

        def run(self):
            while not self.urls.empty():
                url, depth = self.urls.get()
                left = self.urls.qsize()
                if url.endswith('.pdf'):
                    continue
                if '\r\n' in url:
                    temp = url.split('\r\n')
                    if len(temp) > 1:
                        url = temp[0] + temp[-1]
                    else:
                        url = temp[0]
                print(
                    f'[+] Scraping https://{url}, depth={depth}, queued={left}')
                try:
                    request = Request(url, https=self.https, port=self.port)
                    self.get_addresses(request.text, depth)
                    if self.init:
                        break
                except:
                    pass

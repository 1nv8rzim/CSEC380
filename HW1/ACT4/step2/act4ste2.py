from requests import get
from argparse import ArgumentParser
from ipaddress import IPv4Address
from threading import Thread


class Scanner:
    def __init__(self):
        self.args = ArgumentParser()
        self.args.add_argument('start_ip', help="Starting IP of proxy scanner")
        self.args.add_argument('end_ip', help="Ending IP of proxy scanner")
        self.args.add_argument('-t', '--threads', default=10,
                               type=int, help="Number of threads to run the Scanner")
        self.args.add_argument('-a', '--all-ports', default=False,
                               action='store_true', help='Use uncommon proxy ports too')
        self.args = self.args.parse_args()

        self.threads = []
        self.common_ports = (80, 443, 808, 1080, 3128, 8080, 8118)
        self.uncommon_ports = (81, 82, 83, 84, 85, 86, 88, 1337, 3124, 3127, 3129, 6515, 6588,
                               6666, 6675, 8000, 8001, 8008, 8081, 8082, 8085, 8088, 8090, 8123, 8800, 8888, 8909, 9000, 9415, 36081, 54321, 60099)
        self.main()

    def get_address(self):
        print("[+] Checking common proxy ports")
        for address in range(int(IPv4Address(self.args.start_ip)), int(IPv4Address(self.args.end_ip))):
            for port in self.common_ports:
                yield str(IPv4Address(address)) + f':{port}'
        if self.args.a:
            print('[+] Checking uncommon ports')
            for address in range(int(IPv4Address(self.args.start_ip)), int(IPv4Address(self.args.end_ip))):
                for port in self.uncommon_ports:
                    yield str(IPv4Address(address)) + f':{port}'
        for _ in range(self.args.threads):
            yield None

    def main(self):
        generator = self.get_address()
        for _ in range(self.args.threads):
            self.threads.append(self.ScannerThread(generator))
            self.threads[-1].start()
        self.threads[-1].join()

        proxies = []

        for thread in self.threads:
            proxies += thread.proxies

        proxies = sorted(proxies)

        print(f'[+] Listing found proxies')
        for proxy in proxies:
            print(f'\t[+] {proxy}')

    class ScannerThread(Thread):
        def __init__(self, generator):
            Thread.__init__(self)

            self.generator = generator
            self.proxies = []

        def run(self):
            while (address := next(self.generator)) is not None:
                request = get("https://csec.rit.edu",
                              proxies={"http": address})
                if request.status_code == 200:
                    self.proxies += address


Scanner()

from argparse import ArgumentParser
from ipaddress import IPv4Address
from threading import Thread
from proxy_checker import ProxyChecker


class Scanner:
    def __init__(self):
        self.args = ArgumentParser()
        self.args.add_argument('start_ip', help="Starting IP of proxy scanner")
        self.args.add_argument('end_ip', help="Ending IP of proxy scanner")
        self.args.add_argument('-t', '--threads', default=3,
                               type=int, help="Number of threads to run the Scanner. WARNING: going above 3 threads results in false negatives")
        self.args.add_argument('-p', '--ports', default=False,
                               action='store_true', help='Use uncommon proxy ports too')
        self.args = self.args.parse_args()

        self.threads = []
        self.common_ports = (80, 443, 808, 1080, 3128, 8080, 8118, 8888)
        self.uncommon_ports = (81, 82, 83, 84, 85, 86, 88, 1337, 3124, 3127, 3129, 6515, 6588,
                               6666, 6675, 8000, 8001, 8008, 8081, 8082, 8085, 8088, 8090, 8123, 8800, 8909, 9000, 9415, 36081, 54321, 60099)
        self.main()

    def get_address(self):
        print("[+] Checking common proxy ports")
        for address in range(int(IPv4Address(self.args.start_ip)), int(IPv4Address(self.args.end_ip))):
            for port in self.common_ports:
                yield str(IPv4Address(address)) + f':{port}'
        if self.args.ports:
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

        for thread in self.threads:
            if thread.is_alive():
                thread.join()

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
            self.checker = ProxyChecker()

        def run(self):
            while (address := next(self.generator)) is not None:
                # This is my initial solution, requests no longer force use proxies so when I was running this code using
                # using a proxy of 0.0.0.0:1, I was getting back status codes of 200. The only thing that I could get
                # working was the proxy_checker.ProxyChecker() solution (I tried requests.get, requests.sessions.get,
                # urllib.requests.get(), and other and ran into the same issue). I am assuming that the requests.get
                # solution was the intended one, but it was not working no matter my attempts at researching and trying to
                # fix the issues.
                #
                # request requests.get("https://csec.rit.edu", proxies={"http": address})
                # if request.status_code == 200:
                #     self.proxies.append(address)
                test = self.checker.check_proxy(address)
                if test != False:
                    self.proxies.append(address)


Scanner()

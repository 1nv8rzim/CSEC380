from requests import get
from argparse import ArgumentParser
from ipaddress import IPv4Address
from threading import Thread


class Scanner():
    def __init__(self):
        self.args = ArgumentParser()
        self.args.add_argument('start_ip', help="Starting IP of proxy scanner")
        self.args.add_argument('end_ip', help="Ending IP of proxy scanner")
        self.args.add_argument('-t', '--threads', default=10,
                               type=int, help="Number of threads to run the Scanner")
        self.args = self.args.parse_args()

        self.threads = []
        self.main()

    def get_address(self):
        for address in range(int(IPv4Address(self.args.start_ip)), int(IPv4Address(self.args.end_ip))):
            yield str(IPv4Address(address))
        for _ in range(self.args.threads):
            yield None

    def main(self):
        gen = self.get_address()
        for _ in range(self.args.threads):
            self.threads.append(Thread(target=Scanner.run, args=(gen, )))
            self.threads[-1].start()
        self.threads[-1].join()

    @classmethod
    def run(self, gen):
        while (temp := next(gen)) is not None:
            print(temp)


Scanner()

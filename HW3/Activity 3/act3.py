from request import WebCrawler
from threading import Thread
from queue import Queue


def run_thread(line):
    line = line.strip()
    url = line.split(',')[1]
    url = url.split('://')[1]
    if not url.endswith('/'):
        url += '/'

    crawler = WebCrawler(url, https=True, port=443, depth=4)

    with open('crawls/' + url[:-1], 'w') as output:
        for _url in crawler.all_urls:
            if '\r\n' in url:
                temp = url.split('\r\n')
                if len(temp) > 1:
                    url = temp[0] + temp[-1]
                else:
                    url = temp[0]
            output.write(_url + '\n')


def main_thread(queue):
    while not queue.empty():
        line = queue.get()
        run_thread(line)


with open('companies.csv', 'r') as csv:
    queue = Queue()
    threads = []
    for line in csv:
        queue.put(line)

    for _ in range(4):
        threads.append(Thread(target=main_thread, args=(queue, )))
        threads[-1].start()

    for thread in threads:
        thread.join()

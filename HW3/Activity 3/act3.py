from request import WebCrawler
from threading import Thread
from queue import Queue
from os import listdir


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


def run_crawlers():
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


def parse_results():
    paths = {}
    with open('paths.list', 'w') as f:
        for file in listdir('crawls/'):
            with open(f'crawls/{file}', 'r') as crawl:
                for line in crawl:
                    if '/' not in line:
                        continue
                    line = line.strip()
                    line = line[line.index('/'):]
                    if '?' in line:
                        line = line[:line.index('?')]

                    _paths = line.split('/')

                    if _paths[-1] in paths:
                        paths[_paths[-1]] += 1
                    else:
                        paths[_paths[-1]] = 1

                    for path in _paths[:-1]:
                        path += '/'
                        if path in paths:
                            paths[path] += 1
                        else:
                            paths[path] = 1
                print(f'[+] {file} finished')
        paths = sorted(paths.items(), key=lambda x: x[1], reverse=True)
        for path in paths:
            f.write(f'{path[0]}\n')


# run_crawlers()
# parse_results()

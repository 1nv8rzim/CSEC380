from request import Request
from queue import Queue
from threading import Thread

site = 'csec380-core.csec.rit.edu'
port = 83


def thread_check_pages(queue, pages):
    while True:
        if queue.empty():
            break
        path = queue.get()
        qsize = queue.qsize()
        request = Request(f'{site}/{path}', port=port)
        if request.parsed_headers['type'] == '200':
            print(f'[+] path found: http://{site}:{port}/{path}')
            pages.add(f'{path}')
        else:
            print(f'\t[-] queued:{qsize} /{path}')


def spider(all_pages, thread_num=80, subdir_list=['']):
    queue = Queue()
    pages = set()
    for subdir in subdir_list:
        for line in open('paths2500.list'):
            queue.put(subdir + line.strip())

    threads = []

    for _ in range(thread_num):
        threads.append(Thread(target=thread_check_pages,
                              args=(queue, pages)))
        threads[-1].start()

    for thread in threads:
        thread.join()

    pages = pages - all_pages

    return list(pages)


def main():
    subdir_list = ['']
    all_found = set()
    while True:
        subdir_list = spider(all_found, subdir_list=subdir_list)
        for subdir in subdir_list:
            all_found.add(subdir)
        if not len(subdir_list):
            break
        temp = []
        for subdir in subdir_list:
            if subdir.endswith('/'):
                temp.append(subdir)
        subdir_list = temp[:]
    with open('paths_found.txt', 'w') as f:
        for path in all_found:
            f.write(f'{path}\n')


main()

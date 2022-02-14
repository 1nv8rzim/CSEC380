from request import Request, ImageDownload
from bs4 import BeautifulSoup

URL_RE = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

request = Request(
    'www.rit.edu/computing/directory?term_node_tid_depth=4919', port=443, https=True)
good_soup = BeautifulSoup(request.text, 'html.parser')

images = []

for img in good_soup.find_all('img', {"class": "card-img-top"}):
    img = img.get('data-src')
    if '\r\n' in img:
        img = img.split('\r\n')
        img = img[0] + img[-1]
    images.append(img[8:])

ImageDownload(
    images, folder='/home/max/Repositories/CSEC380/HW3/Activity 1/step2/images')

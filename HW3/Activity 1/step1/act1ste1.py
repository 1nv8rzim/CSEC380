from request import Request
from bs4 import BeautifulSoup

request = Request(
    'www.rit.edu', '/study/computing-security-bs', port=443, https=True)

good_soup = BeautifulSoup(request.text, 'html.parser')

for tr in good_soup.find_all('tr', {"class": "hidden-row"}):
    tr = BeautifulSoup(tr, 'html.parser')
    class_number = tr

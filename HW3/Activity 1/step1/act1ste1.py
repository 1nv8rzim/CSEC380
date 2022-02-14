from request import Request
from bs4 import BeautifulSoup
from re import match

request = Request(
    'www.rit.edu', '/study/computing-security-bs', port=443, https=True)

good_soup = BeautifulSoup(request.text, 'html.parser')
classes = {}

for tr in good_soup.find_all('tr', {"class": "hidden-row"}):
    class_code, class_name = (temp := tr.find_all('td')[0:2])
    if not match('[A-Z]{4}-[0-9]{2,3}', class_code.text.strip()):
        continue
    classes[class_code.text.strip()] = class_name.find(
        'div', {'class': 'course-name'}).text.split('\n')[0].strip()

with open('classes.csv', 'w') as csv:
    csv.write('Class Code,Class Name\n')
    for code, name in classes.items():
        csv.write(f'{code},{name}\n')

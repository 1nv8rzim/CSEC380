import socket
import json
from urllib.parse import quote

HOST = 'csec380-core.csec.rit.edu'
PORT = 82
user = 'msf9542'


def make_request(page, **parameters):
    parameters = '&'.join('{}={}'.format(quote(key), quote(value))
                          for key, value in parameters.items())
    print(parameters)
    request = f'''POST /{page} HTTP/1.1\r
Host: {HOST}:{PORT}\r
User-Agent: Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko\r
Connection: keep-alive\r
Accept: text/html\r
Accept-Encoding: deflate\r
Accept-Language: en-US,en;q=0.9\r
Content-Length: {len(parameters)}\r
Content-Type: application/x-www-form-urlencoded\r
Connection: keep-alive\r
\r
{parameters}\r\n'''
    return request.encode()


def parse_request(s):
    return json.loads(s.recv(4096).decode().split('\r\n\r\n')[-1][:-1])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(make_request('getSecure', user=user))
    token = parse_request(s)['token']
    s.send(make_request('createAccount', user=user, username=user, token=token))
    password = parse_request(s)['account_password']
    s.send(make_request('login', token=token, user=user, username=user,
           password=password))
    print(s.recv(4096).decode())

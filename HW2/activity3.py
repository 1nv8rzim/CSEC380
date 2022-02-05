import socket
import json

HOST = 'csec380-core.csec.rit.edu'
PORT = 82
user = 'msf9542'


def make_request(page, parameters):
    request = f'''POST /{page} HTTP/1.1\r
Host: {HOST}:{PORT}\r
Connection: keep-alive\r
Content-Length: {len(parameters)}\r
Content-Type: application/x-www-form-urlencoded\r
\r
{parameters}\r\n'''
    return request


def parse_request(s):
    return json.loads(s.recv(4096).decode().split('\r\n\r\n')[-1][:-1])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    request = make_request('getSecure', f'user={user}')
    s.send(request.encode())
    receive = parse_request(s)
    request = make_request(
        'getFlag3Challenge', 'user={}&token={}'.format(user, receive["token"]))
    s.send(request.encode())
    captcha = eval(parse_request(s)['CAPTCHA'])
    request = make_request(
        'getFlag3Challenge', 'user={}&token={}&solution={}'.format(user, receive["token"], captcha))
    s.send(request.encode())
    print(parse_request(s))

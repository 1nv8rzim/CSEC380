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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    request = make_request('getSecure', f'user={user}')
    s.send(request.encode())
    receive = json.loads(s.recv(4096).decode().split('\r\n\r\n')[-1][:-1])
    request = make_request(
        'getFlag2', 'user={}&token={}'.format(user, receive["token"]))
    s.send(request.encode())
    print(s.recv(4096).decode())

import socket
import json

HOST = 'csec380-core.csec.rit.edu'
PORT = 82
user = 'msf9542'


def make_request(page, parameters):
    request = f'''POST /{page} HTTP/1.1\r
Host: {HOST}:{PORT}\r
User-Agent: Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko\r
Connection: keep-alive\r
Content-Length: {len(parameters)}\r
Content-Type: application/x-www-form-urlencoded\r
\r
{parameters}\r\n'''
    return request.encode()


def parse_request(s):
    return json.loads(s.recv(4096).decode().split('\r\n\r\n')[-1][:-1])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(make_request('getSecure', f'user={user}'))
    token = parse_request(s)['token']
    s.send(temp := make_request('createAccount',
           f'user={user}&username={user}&token={token}'))
    print(temp.decode())
    print(s.recv(4096).decode())

import socket

HOST = 'csec380-core.csec.rit.edu'
PORT = 82
user = 'msf9542'

request = f'''POST / HTTP/1.1\r
Host: {HOST}:{PORT}\r
Connection: keep-alive\r
Content-Length: 12\r
Content-Type: application/x-www-form-urlencoded\r
\r
user={user}\r\n'''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(request.encode())
    print(s.recv(4096).decode())

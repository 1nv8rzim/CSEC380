from flask import Flask, request
import logging

app = Flask(__name__)
logging.basicConfig(filename='access.log', level=logging.INFO,
                    format=f'%(asctime)s %(levelname)s : %(message)s')


@app.route('/')
def index():
    remote = request.remote_addr
    user_agent = request.user_agent
    method = request.method
    path = request.path
    logging.info(f'"{method} {path}" - {remote} - {user_agent}')
    return "Hello World!", 200


app.run("0.0.0.0")

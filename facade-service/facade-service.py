import random
import uuid

import requests
from flask import Flask, request

app = Flask(__name__)

logging_web_clients = ["http://localhost:8082/log",
                       "http://localhost:8083/log",
                       "http://localhost:8084/log"]

messages_web_client = "http://localhost:8081/message"


@app.route("/facade", methods=['POST', 'GET'])
def facade():
    if request.method == 'POST':
        msg = {"id": uuid.uuid4(), "txt": request.get_json()}
        resp = requests.post(random.choice(logging_web_clients), data=msg)
        return resp.text

    elif request.method == 'GET':
        return requests.get(random.choice(logging_web_clients)).text + ": " + requests.get(messages_web_client).text


if __name__ == "__main__":
    app.run()

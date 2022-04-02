from flask import Flask, request
import uuid
import requests

app = Flask(__name__)

logging_web_client = "http://localhost:8081/log"
messages_web_client = "http://localhost:8082/message"


@app.route("/facade", methods=['POST', 'GET'])
def facade():
    if request.method == 'POST':
        msg = {"id": uuid.uuid4(), "txt": request.get_json()}
        resp = requests.post(logging_web_client, data=msg)
        return resp.text
    elif request.method == 'GET':
        return requests.get(logging_web_client).text + ": " + requests.get(messages_web_client).text


if __name__ == "__main__":
    app.run()

import random
import uuid

import hazelcast
import requests
from flask import Flask, request

app = Flask(__name__)

logging_web_clients = ["http://localhost:8082/log",
                       "http://localhost:8083/log",
                       "http://localhost:8084/log"]

messages_web_clients = ["http://localhost:8085/message",
                        "http://localhost:8086/message"]

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
client = hazelcast.HazelcastClient(cluster_name="dev",
                                   cluster_members=[
                                       "127.0.0.1:5701",
                                       "127.0.0.1:5702",
                                       "127.0.0.1:5703"
                                   ])

messages_queue = client.get_queue("messages-queue").blocking()


@app.route("/facade", methods=['POST', 'GET'])
def facade():
    if request.method == 'POST':
        # For message service
        messages_queue.put(f"{request.get_json()}")

        # For logging service
        msg = {"id": uuid.uuid4(), "txt": request.get_json()}
        resp = requests.post(random.choice(logging_web_clients), data=msg)
        return resp.text

    elif request.method == 'GET':
        return "Messages from logging service: " + requests.get(
            random.choice(logging_web_clients)).text + "\nMessages from message service: " + requests.get(
            random.choice(messages_web_clients)).text


if __name__ == "__main__":
    app.run()

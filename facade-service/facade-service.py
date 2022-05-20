import argparse
import random
import uuid

import consul
import hazelcast
import requests
from flask import Flask, request

# Parse port
parser = argparse.ArgumentParser(description='Parsing port.')
parser.add_argument('--port', type=int)
args = parser.parse_args()
port = args.port

# Consul
session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('facade-service',
                               port=port,
                               service_id=f"facade-{str(uuid.uuid4())}")
# Flask app
app = Flask(__name__)

# Find ports of other services
agent = session.agent
services = agent.services()

logging_web_clients = []
messages_web_clients = []
for key, value in services.items():
    service_name = key.split("-")[0]
    if service_name == "logging":
        logging_web_clients.append(f"http://localhost:{value['Port']}/log")
    elif service_name == "messages":
        messages_web_clients.append(f"http://localhost:{value['Port']}/message")

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
client = hazelcast.HazelcastClient(cluster_name="dev",
                                   cluster_members=session.kv.get('hazelcast_ports')[1]['Value'].decode("utf-8").split()
                                   )

messages_queue = client.get_queue(session.kv.get('queue')[1]['Value'].decode("utf-8")).blocking()


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
    app.run(host='localhost', port=port)

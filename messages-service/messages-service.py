import argparse
import uuid

import consul
import hazelcast
from flask import Flask

# Parse port
parser = argparse.ArgumentParser(description='Parsing port.')
parser.add_argument('--port', type=int)
args = parser.parse_args()
port = args.port

# Consul
session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('messages-service',
                               port=port,
                               service_id=f"messages-{uuid.uuid4()}")
# Flask app
app = Flask(__name__)

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
client = hazelcast.HazelcastClient(cluster_name="dev",
                                   cluster_members=session.kv.get('hazelcast_ports')[1]['Value'].decode(
                                       "utf-8").split())

messages_queue = client.get_queue(session.kv.get('queue')[1]['Value'].decode("utf-8")).blocking()

data = list()


@app.route("/message", methods=["GET"])
def message():
    while not messages_queue.is_empty():
        data.append(messages_queue.take())
        print("Got new message: ", data[-1])
    return ", ".join(data)


if __name__ == "__main__":
    app.run(host='localhost', port=port)

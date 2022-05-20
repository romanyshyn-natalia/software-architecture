import argparse
import uuid

import consul
import hazelcast
from flask import Flask, request

# Parse port
parser = argparse.ArgumentParser(description='Parsing port.')
parser.add_argument('--port', type=int)
args = parser.parse_args()
port = args.port

# Consul
session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('logging-service',
                               port=port,
                               service_id=f"logging-{uuid.uuid4()}")
# Flask app
app = Flask(__name__)

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
client = hazelcast.HazelcastClient(cluster_name="dev",
                                   cluster_members=session.kv.get('hazelcast_ports')[1]['Value'].decode(
                                       "utf-8").split())

# Get the Distributed Map from Cluster.
messages = client.get_map(session.kv.get('map')[1]['Value'].decode("utf-8")).blocking()


@app.route("/log", methods=['GET', 'POST'])
def logging():
    if request.method == 'POST':
        uid = str(request.form["id"])
        text = request.form["txt"]
        print("Id: ", uid, "\nmessage: ", text)

        messages.lock(uid)
        try:
            messages.put(uid, text)
        finally:
            messages.unlock(uid)

        return ""

    elif request.method == 'GET':
        return " ".join(messages.values())


if __name__ == "__main__":
    app.run(host='localhost', port=port)

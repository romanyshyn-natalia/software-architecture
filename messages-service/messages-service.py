import hazelcast
from flask import Flask

app = Flask(__name__)
# Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
client = hazelcast.HazelcastClient(cluster_name="dev",
                                   cluster_members=[
                                       "127.0.0.1:5701",
                                       "127.0.0.1:5702",
                                       "127.0.0.1:5703"
                                   ])

messages_queue = client.get_queue("messages-queue").blocking()

data = list()


@app.route("/message", methods=["GET"])
def message():
    while not messages_queue.is_empty():
        data.append(messages_queue.take())
        print("Got new message: ", data[-1])
    return ", ".join(data)


if __name__ == "__main__":
    app.run()

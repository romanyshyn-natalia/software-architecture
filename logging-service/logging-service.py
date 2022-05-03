from flask import Flask, request
import hazelcast

app = Flask(__name__)


@app.route("/log", methods=['GET', 'POST'])
def logging():
    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
    client = hazelcast.HazelcastClient(cluster_name="dev",
                                       cluster_members=[
                                           "127.0.0.1:5701",
                                           "127.0.0.1:5702",
                                           "127.0.0.1:5703"
                                       ])

    # Get the Distributed Map from Cluster.
    messages = client.get_map("logging-map").blocking()

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
    app.run()

from flask import Flask

app = Flask(__name__)


@app.route("/message", methods=["GET"])
def message():
    return "message-service is not implemented yet"


if __name__ == "__main__":
    app.run()

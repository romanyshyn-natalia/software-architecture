from flask import Flask, request

app = Flask(__name__)
messages = dict()


@app.route("/log", methods=['GET', 'POST'])
def logging():
    if request.method == 'POST':
        uid = request.form["id"]
        text = request.form["txt"]
        print("Id: ", uid, "\nmessage: ", text)
        messages[uid] = text
        return ""

    else:
        return " ".join(messages.values())


if __name__ == "__main__":
    app.run()

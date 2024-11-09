from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_current_time():
    return "", 200


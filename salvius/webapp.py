from flask import Flask
from flask import send_from_directory, render_template


app = Flask(__name__, static_url_path='')


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(path)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

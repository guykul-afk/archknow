from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='webapp')

@app.route('/')
def serve_index():
    return send_from_directory('webapp', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('webapp', path)

if __name__ == '__main__':
    print("Starting ArchiCheck Web Server...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(host='127.0.0.1', port=5000)

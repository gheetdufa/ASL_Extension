from flask import Flask, request, Response
from flask_cors import CORS
import json
import queue
import threading

app = Flask(__name__)
CORS(app)

clients = []
lock = threading.Lock()  # Lock for thread-safe access to clients

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    recognized_character = data['character']
    print(f'Received character: {recognized_character}')
    with lock:
        for client in clients:
            client.put(recognized_character)
    return '', 204

@app.route('/listen')
def listen():
    def stream():
        client_queue = queue.Queue()
        with lock:
            clients.append(client_queue)
        try:
            while True:
                character = client_queue.get()
                yield f'data: {json.dumps({"character": character})}\n\n'
        except GeneratorExit:
            with lock:
                clients.remove(client_queue)

    return Response(stream(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(port=5000)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import socket
import json
from whereami.pipeline import get_model
import threading



app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/test')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('data')
def handle_data(data):
    s = socket.socket()
    s.bind(('0.0.0.0', 9999))
    s.listen(0)
    while True:
        client, addr = s.accept()
        while True:
            data = b''
            while True:
                packet = client.recv(32)
                if not packet:
                    break
                data += packet

            if len(data) == 0:
                break
            else:
                decoded_string = str(data.decode("utf-8"))
                decoded_string = decoded_string[:-3] + "}"
                print(decoded_string)
                prediction = predict(decoded_string)
                emit('prediction_update', {'prediction': prediction})
                
def predict(input_string, model_path=None):
    lp = get_model(model_path)
    data_sample = json.loads(input_string)
    return lp.predict(data_sample)[0]

if __name__ == '__main__':
    number_thread = threading.Thread(target=predict)
    number_thread.daemon = True
    number_thread.start()
    socketio.run(app, debug=True)

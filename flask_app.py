from flask import Flask, render_template_string
import socket
import json
from whereami.pipeline import get_model

app = Flask(__name__)


@app.route('/')
def home():
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
                print('Prediction: ')
                print(prediction)
                return render_template_string("""
                    <html>
                        <body style="display: flex; justify-content: center; align-items: center; height: 100vh;">
                            <h1 style="font-size: 50px;">{{ prediction }}</h1>
                        </body>
                    </html>
                """, prediction=prediction)

        print("Closing connection")
        client.close()


def predict(input_string, model_path=None):
    lp = get_model(model_path)
    data_sample = json.loads(input_string)
    return lp.predict(data_sample)[0]


if __name__ == '__main__':
    app.run(debug=True)

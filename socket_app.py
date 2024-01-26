import socket
import json
from whereami.pipeline import get_model


def predict(input_string, model_path=None):
    lp = get_model(model_path)
    data_sample = json.loads(input_string)
    return lp.predict(data_sample)[0]


s = socket.socket()

s.bind(('0.0.0.0', 8090))
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
            print('Prediction: ')
            print(predict(decoded_string))

    print("Closing connection")
    client.close()

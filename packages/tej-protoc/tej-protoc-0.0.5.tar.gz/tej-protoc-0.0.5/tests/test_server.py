import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tej_protoc.serve import create_server
from src.tej_protoc import protocol


class Callback(protocol.Callback):
    def start(self, client):
        builder = protocol.BytesBuilder()
        builder.set_message(b'Hello')
        client.send(builder.bytes())

    def receive(self, files, message):
        print('---- Received in server ----')
        for file in files:
            print(file.name)
        print('Message: ', message.decode())
        print('---------------------------------')


create_server('localhost', 8000, Callback)

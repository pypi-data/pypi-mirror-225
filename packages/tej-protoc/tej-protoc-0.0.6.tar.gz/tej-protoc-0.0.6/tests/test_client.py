import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tej_protoc.client import create_client
from src.tej_protoc import protocol


class ClientCallback(protocol.Callback):
    def start(self, client):
        print('Connected to server...')

    def receive(self, files, message):
        print('---- Received in client ----')
        for file in files:
            print(file.name)

        print('Message: ', message.decode())
        print('---------------------------------')

        builder = protocol.BytesBuilder()
        builder.add_file('hello.txt', b'randombytes')
        builder.add_file('hello.txt', b'randombytes')
        builder.set_message(b'Hello')
        self.client.send(builder.bytes())


create_client('localhost', 8000, ClientCallback)

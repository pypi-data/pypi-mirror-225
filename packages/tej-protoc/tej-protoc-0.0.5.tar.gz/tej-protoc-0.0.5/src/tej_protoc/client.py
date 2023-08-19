import socket
from typing import Type

from . import protocol


def create_client(host: str, port: int, callback_class: Type[protocol.Callback]):
    client = socket.socket()
    client.connect((host, port))

    callback = callback_class(client)
    callback.start(client)

    while True:
        protocol.read(client, callback)

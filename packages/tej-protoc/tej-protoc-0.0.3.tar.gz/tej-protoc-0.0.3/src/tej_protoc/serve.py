from typing import Tuple, Any, Type

import os
import importlib
import subprocess
import socket
import threading

from . import protocol
from .exceptions import ConnectionClosed, ProtocolException


def handle_client(client: socket.socket, address: Tuple[Any], callback_class: Type[protocol.Callback]):
    print(f'Client connected: {address}')
    callback = callback_class(client)

    while True:
        try:
            protocol.read(client, callback)

        except (ConnectionClosed, ProtocolException, Exception) as e:
            print(e)
            break

    del callback
    client.close()
    print('Connection closed')


def serve(server: socket.socket, callback_class: Type[protocol.Callback]):
    if not callback_class:
        raise Exception('Please provide a callback class to pass you received data')

    while True:
        client, address = server.accept()

        # Create new thread for each client
        thread = threading.Thread(target=handle_client, args=(client, address, callback_class))
        thread.start()


def tunnel_ngrok(port: int, token: str):
    try:
        importlib.import_module('ngrok')
    except ImportError:
        print('Installing ngrok...')
        subprocess.run('pip install ngrok'.split(' '))

    import ngrok

    os.environ['NGROK_AUTHTOKEN'] = token
    tunnel = ngrok.connect(port, 'tcp', authtoken_from_env=True)
    print('Ngrok proxied url: ', tunnel.url())


def create_server(host: str, port: int, callback_class: Type[protocol.Callback], **kwargs):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    print(f'Running server in {host}:{port}')

    if kwargs.get('tunnel_ngrok', False):
        ngrok_token = kwargs.get('ngrok_token')
        if not ngrok_token:
            raise Exception('Please provide ngrok token to authenticate')
        tunnel_ngrok(port, ngrok_token)

    server.listen()
    serve(server, callback_class)

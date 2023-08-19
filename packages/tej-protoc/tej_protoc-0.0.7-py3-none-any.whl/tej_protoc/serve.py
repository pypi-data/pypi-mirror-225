from typing import Tuple, Any, Type

import importlib
import subprocess
import socket
import threading

from . import protocol
from .exceptions import ConnectionClosed, ProtocolException


def handle_client(client: socket.socket, address: Tuple[Any], callback_class: Type[protocol.Callback]):
    print(f'Client connected: {address}')

    callback = callback_class(client)
    callback.start(client)

    while True:
        try:
            protocol.read(client, callback)

        except (ConnectionClosed, ProtocolException, Exception) as e:
            print(e)
            break

    client.close()
    del callback
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
        importlib.import_module('pyngrok')
    except ImportError:
        print('Installing pyngrok...')
        subprocess.run('pip install pyngrok'.split(' '))

    from pyngrok import ngrok
    ngrok.set_auth_token(token)
    print(f'Connecting to ngrok...')
    ssh_tunnel = ngrok.connect(port, "tcp")
    print(f'Ngrok proxy is running at {ssh_tunnel.public_url}')


def create_server(host: str, port: int, callback_class: Type[protocol.Callback], **kwargs):
    server = socket.create_server((host, port), reuse_port=True)
    print(f'Running server in {host}:{port}')

    if kwargs.get('proxy_ngrok'):
        ngrok_token = kwargs.get('ngrok_token')
        if not ngrok_token:
            raise Exception('Please provide ngrok token to authenticate')

        tunnel_ngrok(port, ngrok_token)

    serve(server, callback_class)

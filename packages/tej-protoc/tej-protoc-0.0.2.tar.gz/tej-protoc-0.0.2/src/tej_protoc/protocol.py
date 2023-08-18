from typing import Tuple, Optional, List
import logging
import socket

from exceptions import InvalidStatusCode, InvalidProtocolVersion, ConnectionClosed, ProtocolException

logger = logging.getLogger('__main__')


class Callback:
    files_count: int = 0
    protocol_version: int = 1
    status: int = 0
    __files = []
    __message = None

    def __init__(self, client: socket.socket):
        self.client = client

    def receive_file_data(self, filename: str, data: bytes, size: int):
        self.__files.append((filename, data, size))

    def message(self, data: bytes):
        self.__message = data

    def clean(self):
        self.files_count = 0
        self.protocol_version = 1
        self.status = 0
        self.__files = []
        self.__message = None

    def complete(self):
        self.receive(self.__files, self.__message)

    def receive(self, files: List[Tuple[str, bytes, int]], message: bytes):
        pass


def read_bytes(client: socket.socket, size: int) -> bytes:
    buffer_size = 1024
    data = b''
    bytes_in = 0

    while bytes_in != size:
        remaining_size = size - bytes_in
        max_read = min(remaining_size, buffer_size)
        chunk = client.recv(max_read)
        if not chunk:
            raise ConnectionClosed()

        data += chunk
        bytes_in += len(chunk)

    return data


def read_status(client: socket.socket) -> Tuple[int, int]:
    """
    Reads first byte from the dataframe
    """

    first_byte = read_bytes(client, 1)
    status = ord(first_byte) >> 7
    custom_status = ord(first_byte) & 0b01111111
    return status, custom_status


def read_protocol_version(client: socket.socket) -> int:
    return ord(read_bytes(client, 1))


def count_number_of_files(client: socket.socket) -> int:
    return int.from_bytes(read_bytes(client, 8), byteorder='big')


def read_file(client: socket.socket) -> Tuple[str, bytes, int]:
    filename_length = int.from_bytes(read_bytes(client, 2), byteorder='big')
    filename = read_bytes(client, filename_length).decode()
    file_length = int.from_bytes(read_bytes(client, 8), byteorder='big')
    file_data = read_bytes(client, file_length)
    return filename, file_data, file_length


def read_message(client: socket.socket) -> Optional[bytes]:
    message_length = int.from_bytes(read_bytes(client, 8), byteorder='big')

    if message_length == 0:
        return None

    return read_bytes(client, message_length)


def read(client: socket.socket, callback: Callback):
    status, custom_status = read_status(client)
    if status != 1:
        print('Invalid starting bit. Received: ', bin(status)[2:])
        raise ProtocolException()  # First bit must be 1 to be valid

    callback.clean()
    callback.status = custom_status
    callback.protocol_version = read_protocol_version(client)
    callback.files_count = count_number_of_files(client)

    for e in range(callback.files_count):
        filename, file_data, file_size = read_file(client)
        callback.receive_file_data(filename, file_data, file_size)

    message = read_message(client)
    if message:
        callback.message(message)

    callback.complete()


class BytesBuilder:
    """
    Constructs bytes for TEJ protocol
    """

    _bytearray = bytearray()
    _protocol_version: int = 1
    _status_code: int = 0
    _files: List[Tuple[str, bytes, int]] = []
    _message: str = None

    def __init__(self, status_code: Optional[int] = None):
        if status_code:
            in_range = (status_code >= 0 or status_code <= 0b01111111)
            if not in_range:
                raise InvalidStatusCode('The allowed range is 0 to 127')

            self._status_code = status_code

    def set_protocol_version(self, version: int) -> 'BytesBuilder':
        if not (version >= 0 or version <= 256):
            raise InvalidProtocolVersion('The allowed range is 0 to 256')

        self._protocol_version = version
        return self

    def add_file(self, filename: str, data: bytes):
        self._files.append((filename, data, len(data)))
        return self

    def set_message(self, message):
        self._message = message
        return self

    def bytes(self) -> bytes:
        # Status byte 8 bit
        status_byte = self._status_code | 0b10000000  # Set 1 to MSB
        self._bytearray.append(status_byte)

        # Protocol version 8 bit
        self._bytearray.append(self._protocol_version)

        # Files count 64 bits
        files_count = len(self._files)
        self._bytearray += files_count.to_bytes(8, byteorder='big')

        # Add files information to data frame
        for (filename, file_data, size) in self._files:
            # File length 16 bit
            filename_length = len(filename)
            self._bytearray += filename_length.to_bytes(2, byteorder='big')

            # n bits from filename length
            self._bytearray += bytes(filename, 'utf-8')

            # file size
            file_length = size.to_bytes(8, byteorder='big')
            self._bytearray += file_length

            # file n bits from file size
            self._bytearray += file_data

        message_length = 0
        if self._message:
            message_length = len(self._message)

        # Message length 64 bit
        message_length = message_length.to_bytes(8, byteorder='big')
        self._bytearray += message_length

        if self._message:
            # Message n bits from message length
            self._bytearray += self._message

        return bytes(self._bytearray)

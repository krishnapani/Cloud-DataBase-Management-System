from http import server
from pydoc import cli
import socket
import os

SERVER_ADDRESS = ('192.168.199.15', 8000)
BUFFER_SIZE = 4096
FILES_DIRECTORY = 'files'

def handle_client_connection(client_socket):
    request = client_socket.recv(BUFFER_SIZE).decode()
    if request.startswith('upload'):
        _, filename, filesize = request.split(':')
        filesize = int(filesize)
        with open(os.path.join(FILES_DIRECTORY, filename), 'wb') as f:
            client_socket.send(("ready").encode())
            while filesize > 0:
                data = client_socket.recv(BUFFER_SIZE)
                f.write(data)
                filesize -= len(data)
        client_socket.send(b'Upload successful')

    elif request.startswith('download'):
        _, filename = request.split(':')
        filepath = os.path.join(FILES_DIRECTORY, filename)
        if not os.path.isfile(filepath):
            client_socket.send(b'File not found')
        else:
            filesize = os.path.getsize(filepath)
            client_socket.send(f'filesize:{filesize}'.encode())
            with open(filepath, 'rb') as f:
                response = client_socket.recv(BUFFER_SIZE).decode()
                if response == 'ready':
                    data = f.read(BUFFER_SIZE)
                    while data:
                        client_socket.send(data)
                        data = f.read(BUFFER_SIZE)

    elif request.startswith('list'):
        files = os.listdir(FILES_DIRECTORY)
        files_str = ','.join(files)
        client_socket.send(f'files:{files_str}'.encode())
    client_socket.close()

def main():
    if not os.path.exists(FILES_DIRECTORY):
        os.makedirs(FILES_DIRECTORY)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(1)
    print(f'Server is listening on {SERVER_ADDRESS}')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Client connected from {client_address}')
        handle_client_connection(client_socket)

if __name__ == '__main__':
    main()

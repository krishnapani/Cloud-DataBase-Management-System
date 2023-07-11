import socket
import os

SERVER_ADDRESS = ('192.168.64.14', 8000)
BUFFER_SIZE = 4096

def upload_file(filename):
    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as f:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(SERVER_ADDRESS)
        client_socket.send(f'upload:{filename}:{filesize}'.encode())
        response = client_socket.recv(BUFFER_SIZE).decode()
        if response == 'ready':
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                client_socket.send(data)
            response = client_socket.recv(BUFFER_SIZE).decode()
            print(response)
        else:
            print(response)
        client_socket.close()

def download_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    client_socket.send(f'download:{filename}'.encode())
    response = client_socket.recv(BUFFER_SIZE).decode()
    if response.startswith('filesize'):
        _, filesize = response.split(':')
        filesize = int(filesize)
        with open(filename, 'wb') as f:
            client_socket.send(("ready").encode())
            while filesize > 0:
                data = client_socket.recv(BUFFER_SIZE)
                f.write(data)
                filesize -= len(data)
        print('Download successful')
    else:
        print(response)
    client_socket.close()

def list_files():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    client_socket.send('list'.encode())
    response = client_socket.recv(BUFFER_SIZE).decode()
    if response.startswith('files'):
        files_str = response.split(':')[1]
        files = files_str.split(',')
        for file in files:
            print(file)
    else:
        print(response)
    client_socket.close()

def main():
    while True:
        command = input('Enter command (upload, download, or list): ')
        if command == 'upload':
            filename = input('Enter filename: ')
            if os.path.isfile(filename):
                upload_file(filename)
            else:
                print('File not found')
        elif command == 'download':
            filename = input('Enter filename: ')
            download_file(filename)
        elif command == 'list':
            list_files()
        else:
            print('Invalid command')

if __name__ == '__main__':
    main()
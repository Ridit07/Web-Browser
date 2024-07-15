import socket
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=1080
server_socket.bind((host,port))
server_socket.listen(1)
print('server is working, waiting for connection')
client_socket,addr=server_socket.accept()
print(f'server has found a connection from {addr}')
while True:
    data=client_socket.recv(1024).decode()
    if not data:
        break
    print(f"message Received from client:{data}")
    client_socket.send(data.encode())
    if data.strip().lower()in['stop','exit','close connection']:
        break
print("Closing connection...")
client_socket.close()

import socket
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=1080
client_socket.connect((host,port))
while True:
    sentence=input("Send any message to the server (echo):")
    if not sentence:
        break
    client_socket.send(sentence.encode())
client_socket.close()

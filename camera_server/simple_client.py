import socket
import pickle

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 10
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

for _ in xrange(5):
    print "Sending hello from client side."
    s.send(MESSAGE)
    while True:
        data = s.recv(BUFFER_SIZE)
        if not data:
            break
        print data
    print "Received message from server side:", data

s.close()


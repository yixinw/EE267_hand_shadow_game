import socket
import pickle
from PIL import Image
import StringIO

def recv_end(the_socket, end_string):
    total_data=[];data=''
    while True:
        data=the_socket.recv(8192)
        if end_string in data:
            total_data.append(data[:data.find(end_string)])
            break
        total_data.append(data)
        if len(total_data)>1:
            #check if end_of_data was split
            last_pair=total_data[-2]+total_data[-1]
            if end_string in last_pair:
                total_data[-2]=last_pair[:last_pair.find(end_string)]
                total_data.pop()
                break
    return ''.join(total_data)


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

for _ in xrange(5):
    print "Sending hello from client side."
    s.send(MESSAGE)

    # Receive message.
    array_string = recv_end(s, "$$$")
    print len(array_string)
    tempBuff = StringIO.StringIO()
    tempBuff.write(array_string)
    tempBuff.seek(0)
    im = Image.open(tempBuff)
    print im.size, im.mode
    #hand_image = pickle.loads(array_string)
    #print hand_image.shape

    # print "Received message from server side:", data

s.shutdown(socket.SHUT_RDWR)
s.close()


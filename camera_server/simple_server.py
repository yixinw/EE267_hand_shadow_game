import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

'''
conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    conn.send(data)  # echo
conn.close()
'''

conn, addr = s.accept()
s.setblocking(0)
while True:
    try:
        data = conn.recv(BUFFER_SIZE)
        if data == 'Hello, World!':
            response = "Hello received at server side."
            print response
            conn.send(str(len(response)) + ":" + response)
    except socket.error:
        pass


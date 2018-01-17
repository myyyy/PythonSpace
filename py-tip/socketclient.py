import socket 
s = socket.socket()
host = socket.gethostname()
port = 1234
s.connect((host,port))
s.sendall('suyf')
print s.recv(1024)


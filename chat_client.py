import socket
import sys

host = str(sys.argv[1])
port = int(sys.argv[2])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = (host, port)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

data = sock.recv(4096)
print data

while data != "adios\r\n":
    message = raw_input('What is your command: ')
    sock.sendall(message + "\r\n")
    data = sock.recv(4096)
    print data


print >>sys.stderr, 'closing socket'
sock.close()
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
server_address = ('192.168.190.44', 9020)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
# Listen for incoming connections
sock.listen(10)
name = "unknown"


while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address
        message = "Welcome to " + name + "'s chat room\r\n"
        connection.sendall(message)
        chat_buffer = ""

        while True:
            data = connection.recv(4096)
            if data[-2:] != "\r\n":
                data = data + connection.recv(4096)
                print data
            print data
            checkdata = data.split('\r\n')


            for num in checkdata:
                if num == "":
                    continue

                elif num[:6] == "name: ":
                    name = num[6:]
                    message = "OK\r\n"
                    connection.sendall(message)
                elif num == "help":
                    message = "The available commands are: help test: words name: <chatname> get push: <stuff> getrange <startline> <endline> adios\r\n"
                    connection.sendall(message)
                elif num[:6] == "test: ":
                    message = num[6:]
                    connection.sendall(message + "\r\n")

                elif num == "get":
                    if chat_buffer == "":
                        message = ""
                        connection.sendall(message + "\r\n")
                    else:
                        message = chat_buffer
                        connection.sendall(message + "\r\n")
                elif num[:6] == "push: ":
                    chat_buffer = chat_buffer + name + ": " + num[6:] + "\n"
                    message = "OK"
                    connection.sendall(message + "\r\n")
                elif num[:9] == "getrange ":
                    myrange = num.split(' ')
                    try:
                        beginrange = myrange[1]
                        endrange = myrange[2]
                        chatrange = chat_buffer
                        chatrange = chatrange.split('\n')
                        beginrange = int(beginrange)
                        endrange = int(endrange)
                        message = ""
                        while(beginrange <= endrange):
                            message = message + chatrange[beginrange] + "\n"
                            beginrange += 1
                        connection.sendall(message + "\r\n")
                    except IndexError:
                        endrange = 'null'
                        message = "You didn't enter in both arguements, or the numbers were out of range"
                        connection.sendall(message)
                elif num == "adios":
                    message = num
                    connection.sendall(message + "\r\n")
                    
                elif num[:6] != "name: " or num != "help" or num[:6] != "test: " or num != "get" or num[:6] != "push: " or num[:9] != "getrange " or num != "adios" :
                    message = "Error: unrecognized command: " + num
                    connection.sendall(message + "\r\n")      
    finally:
        # Clean up the connection
        connection.close()
#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

def client():
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 54321                # Reserve a port for your service.

    while True:
        user_input = raw_input('Client says: ')
        s.connect((host, port))
        if user_input == 'exit':
            return 'Client exited.'
        else:
            #s.connect((host, port))
            s.sendall(user_input)
            data = s.recv(2048)
            s.close             # Close the socket when done
            print("Received: {0}".format(data))
    
if __name__ == '__main__':
    client_result = client()
    print(client_result)
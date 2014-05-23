#!/usr/bin/python           # This is client.py file

import sys
from socket import *                # Import socket module

host = 'localhost'                  # Get local machine name
port = 54321                        # Reserve a port for your service.

message = [b'line 1: Hello', b'line 2: World', b'line 3: This is ...', b'...Shanks...', b'This is the default message']

def client():
    while True:
        sockobj = socket(AF_INET, SOCK_STREAM)         # Create a socket object
        
        try:
            user_input = raw_input('Client says: ')
            if len(user_input) == 0:
                user_input = None
        except EOFError:
            user_input = None
        except ValueError:
            user_input = None
        except Exception as e:
            return e
        
        sockobj.connect((host, port))
        
        if user_input == 'exit':
            return 'Client exited.'
        elif user_input is None:
            for line in message:
                sockobj.send(line)
                data = sockobj.recv(2048)
                print('Client received: {0}'.format(data))
            #sockobj.close()
        else:
            #pass
            #s.connect((host, port))
            sockobj.send(user_input)
            data = sockobj.recv(2048)
            print("Received: {0}".format(data))
    
    sockobj.close()             # Close the socket when done
    
if __name__ == '__main__':
    client_result = client()
    print(client_result)
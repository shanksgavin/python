#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

def server(action=None):
    if action is None:
        return "Please define a server action"
    elif action == 'start':
        print('Server Starting...')
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 54321                # Reserve a port for your service.
        s.bind((host, port))        # Bind to the port
        
        s.listen(5)                 # Now wait for client connection.
        print('Server Running...')
        
        while True:
            c, addr = s.accept()        # Establish connection with client.
            print('Got connection from {0}'.format(addr))
            data = c.recv(2048)
            if not data:
                c.sendall('{0}'.format('No Data Sent From Client'))
            elif data == 'server stop':
                c.sendall('{0}'.format('Server has been stopped.'))
                c.close()           # Close the connection
                return 'Server Stopped By Client...'
            else:
                c.sendall('Thank you for sending: {0}'.format(data))
            
    elif action == 'stop':
        return "Not Implemented Yet but will stop server"
    else:
        return "Unknown Server Error"
        
if __name__ == '__main__':
    server_result = server('start')
    print(server_result)
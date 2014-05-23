#!/usr/bin/python           # This is server.py file

from socket import *                        # Import socket module

host = 'localhost'                          # Get local machine name
port = 54321                                # Reserve a port for your service.
    
def server_comm():
    print('Server Starting...')
    sockobj = socket(AF_INET, SOCK_STREAM)  # Create a socket object
    sockobj.bind((host, port))              # Bind to the port
    sockobj.listen(5)                       # Now wait for client connection.
    print('Server Running...')
    
    while True:
        conn, addr = sockobj.accept()       # Establish connection with client.
        print('Got connection from {0}'.format(addr))
        
        while True:
            data = conn.recv(2048)
            if not data:
                #conn.send(b'{0}'.format('No Data Sent From Client'))
                break
            elif data == 'server stop':
                conn.send(b'{0}'.format('Server has been stopped.'))
                return 'Server Stopped By Client...'
            else:
                conn.send(b'Thank you for sending: {0}'.format(data))
        conn.close()
            
def server(action=None):
    if action is None:
        return "Please define a server action"
    elif action == 'start':
        serv_result = server_comm()
        return serv_result
    elif action == 'stop':
        return "Not Implemented Yet but will stop server"
    else:
        return "Unknown Server Error"
        
if __name__ == '__main__':
    server_result = server('start')
    print(server_result)
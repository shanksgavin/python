from SOAPpy import SOAPProxy

def run():
    url = 'http://services.xmethods.net:80/soap/servlet/rpcrouter'
    namespace = 'urn:xmethods-Temperature'
    server = SOAPProxy(url, namespace)
    return server.getTemp('27502')

if __name__ == '__main__':
    temp = run()
    print(temp)
import socketserver

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass
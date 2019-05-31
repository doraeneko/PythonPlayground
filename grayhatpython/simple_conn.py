#
# Inspired by "Black Hat Python", Justin Seitz.
# A simple TCP server / client
# with "EXEC <cmd>", shell commands can be executed on the server machine.
#

import socket
import threading
import sys, getopt, os

BUFFERSIZE=4096

class Server(object):

    def __init__(self, bind_ip, bind_port):
        self._bind_ip = bind_ip
        self._bind_port = bind_port

    def connect(self):
        try:
            self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server.bind((self._bind_ip, self._bind_port))
        except Exception as e:
            print("Could not connect the server: %s." % e)

    def listen(self):
        self._server.listen(5)
        print("Listening...")
        while True:
            client, addr = self._server.accept()
            client_handler = threading.Thread(target=lambda client: self._handle_client(client), args=(client,))
            client_handler.start()


    def _handle_client(self, client_socket : socket.SocketType):
        print("Connection started: %s" % client_socket)
        try:
            while True:
                request = client_socket.recv(BUFFERSIZE).decode('utf-8')
                print("Got a request: %s (length: %s)" % (request, len(request)))
                if request.startswith("ECHO "):
                    print("SEND ECHO")
                    client_socket.send(request[len("ECHO "):].encode())
                elif request.startswith("EXEC "):
                    cmd = request[(len("EXEC ")):]
                    result = 'EXEC RESULT: %s' % '\n'.join(os.popen(cmd).readlines())
                    print("THE LINES: %s" % result)
                    client_socket.send(result.encode())
                else:
                    print('Close connection: %s' % request)
                    client_socket.close()
                    return
        except socket.error:
            pass
        print('Closing socket.')
        client_socket.close()


class Client(object):

    def __init__(self, target_host, target_port):
        self._target_host = target_host
        self._target_port = target_port
        self._client = None

    def connect(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect((self._target_host, self._target_port))
        print("Connected.")

    def send_input(self, message):
        try:
            self._client.send(message.encode())
            answer = self._client.recv(BUFFERSIZE).decode('utf-8')
            print("> %s" % answer)
        except socket.error:
            print("Connection aborted.")
            return False
        return True


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "sct:p:")
    except getopt.GetoptError as err:
        print(str(err))
        return
    server_mode = False
    target = None
    port = None
    for o,a in opts:
        print("%s-%s" % (o, a))
        if o in ['-s']:
            server_mode = True
        elif o in ['-c']:
            server_mode = False
        elif o in ['-t']:
            target = a
        elif o in ['-p']:
            port = int(a)
        else:
            print("What's %s supposed to mean? Exiting." % o)
            sys.exit(1)
        print(".")

    if server_mode:
        print("Running as server...")
        server = Server(target, port)
        server.connect()
        server.listen()
    else:
        print("Running as client...")
        client = Client(target, port)
        client.connect()
        while True:
            input = sys.stdin.readline()
            if (not client.send_input(input)):
                break

if __name__ == '__main__':

    main()
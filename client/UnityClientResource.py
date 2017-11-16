import socket
import time


class UnityClient:
    BUFFER_SIZE = 1024
    INTERVAL_TIME = 0.01  # 0.01 is absolute minimum for now...
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.oldTime = time.time()

    def connect(self, ipaddress, port):
        self.s.connect((ipaddress, port))
        # logging.debug("UnityClient connected")

    def send(self, message):
        elapsed = time.time() - self.oldTime
        wait = self.INTERVAL_TIME - elapsed
        if wait > 0:
            time.sleep(wait)
        self.oldTime = time.time()
        print(message.encode('utf-8'))
        self.s.sendall(message.encode('utf-8'))

    def send_with_response(self, message, async_function):
        self.send(message)
        data = self.s.recv(self.BUFFER_SIZE)
        print("raw data:", data)
        async_function(data)

    def close(self):
        self.s.close()
        # logging.debug("UnityClient closed")

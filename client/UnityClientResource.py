import socket
import time


class UnityClient:
    DEBUG = False
    BUFFER_SIZE = 1024
    INTERVAL_TIME = 0.01  # 0.009 is absolute minimum for now...
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    def __init__(self, ip='fe80::1848:f36b:4df9:7903', port=13000):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.oldTime = time.time()

    def connect(self):
        if self.DEBUG:
            return
        self.s.connect((self.TCP_IP, self.TCP_PORT, 0, 0))
        print("UnityClient connected")

    def send(self, message):
        if self.DEBUG:
            return
        elapsed = time.time() - self.oldTime
        wait = self.INTERVAL_TIME - elapsed
        if wait > 0:
            time.sleep(wait)
        self.oldTime = time.time()
        self.s.sendall(message.encode('utf-8'))

    def close(self):
        if self.DEBUG:
            return
        self.s.close()
        print("UnityClient closed")

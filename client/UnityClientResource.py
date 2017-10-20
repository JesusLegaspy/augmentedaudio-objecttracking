import socket
import time


class UnityClient:
    BUFFER_SIZE = 1024
    INTERVAL_TIME = 0.01  # 0.009 is absolute minimum for now...
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    def __init__(self, ip='fe80::1848:f36b:4df9:7903', port=13000):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.oldTime = time.time()

    def connect(self):
        self.s.connect((self.TCP_IP, self.TCP_PORT, 0, 0))
        print("UnityClient connected")

    def send(self, message):
        elapsed = time.time() - self.oldTime
        wait = self.INTERVAL_TIME - elapsed
        if wait > 0:
            time.sleep(wait)
        self.oldTime = time.time()
        self.s.sendall(message.encode('utf-8'))

    def send_with_response(self, message, async_function):
        self.send(message)
        data = self.s.recv(self.BUFFER_SIZE)
        async_function(data)

    def close(self):
        self.s.close()
        print("UnityClient closed")

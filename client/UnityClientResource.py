import logging
import socket
import time


class UnityClient:
    BUFFER_SIZE = 1024
    INTERVAL_TIME = 0.01  # 0.01 is absolute minimum for now...
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip='10.42.0.87', port=13000):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.oldTime = time.time()

    def connect(self):
        self.s.connect((self.TCP_IP, self.TCP_PORT))
        logging.debug("UnityClient connected")

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
        async_function(data)

    def close(self):
        self.s.close()
        logging.debug("UnityClient closed")

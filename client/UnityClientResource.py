import socket
import time


class UnityClient:
    DEBUG = True
    BUFFER_SIZE = 1024
    INTERVAL_TIME = 0.01  # 0.009 is absolute minimum for now...
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    developer_uid = [False]

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

    def send_with_response(self, message, async_function):
        if self.DEBUG:
            data = self.dev_build_receive_message(message)
            async_function(data)
            return
        self.send(message)
        data = self.s.recv(self.BUFFER_SIZE)
        async_function(data)

    def close(self):
        if self.DEBUG:
            return
        self.s.close()
        print("UnityClient closed")

    def dev_get_unused_id(self):
        for i, taken in enumerate(self.developer_uid):
            if taken is False:
                self.developer_uid[i] = True
                return i
        self.developer_uid.append(True)
        return len(self.developer_uid) - 1

    def dev_build_receive_message(self, send_message):
        numbers = send_message.split('+')
        receive_msg = ""
        if len(numbers) == 0:
            return receive_msg
        receive_msg = str(self.dev_get_unused_id())
        for i in range(1, len(numbers)):
            receive_msg += ',' + str(self.dev_get_unused_id())
        return receive_msg

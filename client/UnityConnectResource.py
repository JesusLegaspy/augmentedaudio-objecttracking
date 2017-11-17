from client.UnityClientResource import UnityClient
import re


class UnityConnect:
    client = UnityClient()
    run_this = None

    DEV_NO_UNITY = False
    DEV_MOCK_RECEIVE = False
    developer_uid = [False]

    def __init__(self):
        return

    def connect(self, ipaddress, port):
        if self.DEV_NO_UNITY:
            return
        self.client.connect(ipaddress, port)

    # points === [ID,(x, y, z)]
    def move(self, points):
        #print("Moving points: ", points)
        if self.DEV_NO_UNITY:
            return
        # logging.debug("UnityConnect.move")
        message = self.message_builder("M", points)
        self.client.send(message)

    def destroy(self, points):
        # logging.debug("UnityConnect.destroy")
        if self.DEV_NO_UNITY or self.DEV_MOCK_RECEIVE:
            for point in points:
                self.developer_uid[point[0]] = False
            if self.DEV_NO_UNITY:
                return
        message = self.message_builder("D", points)
        self.client.send(message)

    # coords === (x, y, z)
    def create(self, coords, uid_action_function):
        # logging.debug("UnityConnect.create")
        if self.DEV_NO_UNITY:
            uids = self.dev_build_receive_uids(coords)
            uid_action_function(uids)
            return
        points = list(zip([""] * len(coords), coords))  # ("",(x,y,z))
        message = self.message_builder("C", points)
        self.run_this = uid_action_function
        if self.DEV_MOCK_RECEIVE:
            self.client.send(message)
            uids = self.dev_build_receive_uids(coords)
            uid_action_function(uids)
            return
        self.client.send_with_response(message, self.message_decoder)

    def message_decoder(self, string):
        string = string.decode("utf-8")
        content = re.findall(r'[0-9]+', string, re.I)
        # uids = list(map(int, string.split(':')[1].split(',')))  # uids are ID's Unity returns
        print("split:", content)
        self.run_this(content)

    def cmd_builder(self, action, coord, uid=""):
        if action == "D":
            return "D" + str(uid)
        cmd = action + str(uid) + "(" + "{:.4f}".format(coord[0]) + ","
        cmd = cmd + "{:.4f}".format(coord[1]) + ","
        cmd = cmd + "{:.4f}".format(coord[2]) + ")"
        return cmd

    def message_builder(self, action, points):
        if len(points) == 0:
            return
        message = self.cmd_builder(action, points[0][1], points[0][0])
        iterpoints = iter(points)
        next(iterpoints)
        for point in iterpoints:
            message += "+" + self.cmd_builder(action, point[1], point[0])
        return message

    def close(self):
        if self.DEV_NO_UNITY:
            return
        self.client.close()

    def dev_get_unused_id(self):
        for i, taken in enumerate(self.developer_uid):
            if taken is False:
                self.developer_uid[i] = True
                return i
        self.developer_uid.append(True)
        return len(self.developer_uid) - 1

    def dev_build_receive_uids(self, coords):
        receive = []
        for _ in coords:
            receive.append(self.dev_get_unused_id())
        return receive


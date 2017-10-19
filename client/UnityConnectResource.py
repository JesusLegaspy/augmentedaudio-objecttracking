from UnityClientResource import UnityClient
import logging


class UnityConnect:
    client = UnityClient()

    def __init__(self):
        return

    def connect(self):
        self.client.connect()

    # [ID,(x, y, z)]
    def move(self, points):
        logging.debug("UnityConnect.move")
        message = self.message_builder("M", points)

    def destroy(self):
        logging.debug("UnityConnect.destroy")

    run_this = None

    # coords === (x, y, z)
    def create(self, coords, uid_action_function):
        logging.debug("UnityConnect.create")
        points = list(zip([""] * len(coords), coords))  # ("",(x,y,z))
        message = self.message_builder("C", points)
        self.run_this = uid_action_function
        self.client.send_with_response(message, self.message_decoder)

    def message_decoder(self, string):
        uids = list(map(int, string.split(',')))
        self.run_this(uids)

    def cmd_builder(self, action, coord, uid = ""):
        cmd = action + uid + "(" + f"{coord[0]:.4f}" + ","
        cmd = cmd + f"{coord[1]:.4f}" + ","
        cmd = cmd + f"{coord[2]:.4f}" + ")"
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
        self.client.close()
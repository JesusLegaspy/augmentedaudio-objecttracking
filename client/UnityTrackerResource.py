from UnityConnectResource import UnityConnect

class UnityTracker:
    RADIUS = 4
    FILTER = 1
    client = UnityConnect()

    prevFrame = []
    currFrame = []

    def __init__(self):
        self.client.DEBUG = True
        self.client.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()

    def send(self, x, y, z):
        cmd = "C(" + f"{x:.4f}" + ","
        cmd = cmd + f"{y:.4f}" + ","
        cmd = cmd + f"{z:.4f}" + ")"
        self.client.send(cmd)

    def add(self, x, y, z):
        # filtering
        for cF in self.currFrame:
            dist = (cF[0] - x) ** 2 + (cF[1] - y) ** 2 + (cF[2] - z) ** 2
            if dist <= (self.FILTER ** 2):
                cF[0] = cF[0] + (abs(cF[0] - x) / 2)
                cF[1] = cF[1] + (abs(cF[1] - y) / 2)
                cF[2] = cF[2] + (abs(cF[2] - z) / 2)
                return
        self.currFrame.append([x, y, z])

    def next_frame(self):
        c_done = [False] * len(self.currFrame)  # link found on curr frame
        move = []
        create = [True] * len(self.currFrame)
        destroy = [True] * len(self.prevFrame)

        # Link objects from both frames based on distance
        # Note: this algorithm doesn't try to get the most links possible
        if len(self.prevFrame) != 0:
            for pI in range(0, len(self.prevFrame)):
                short_dist = None
                for cI in range(0, len(self.currFrame)):
                    if not c_done[cI]:
                        dist = (self.currFrame[cI][0] - self.prevFrame[pI][0]) ** 2
                        dist += (self.currFrame[cI][1] - self.prevFrame[pI][1]) ** 2
                        dist += (self.currFrame[cI][2] - self.prevFrame[pI][2]) ** 2
                        if dist <= self.RADIUS ** 2:
                            if short_dist is None:
                                short_dist = [dist, cI]
                            else:
                                if dist < short_dist[0]:
                                    short_dist = [dist, cI]
                if short_dist is not None:
                    c_done[short_dist[1]] = True
                    move.append([pI, short_dist[1]])

        # Destroy/ Create
        for ele in move:
            destroy[ele[0]] = False
            create[ele[1]] = False

        self.prevFrame = list(self.currFrame)
        self.currFrame = []

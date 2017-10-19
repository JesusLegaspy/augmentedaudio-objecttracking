from UnityConnectResource import UnityConnect

class UnityTracker:
    RADIUS = 4
    FILTER = 1
    uconnect = UnityConnect()

    prevFrame = [] #deprecated
    pointStore = []
    currFrame = []

    def __init__(self):
        self.uconnect.DEBUG = True
        self.uconnect.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.uconnect.close()

    def send(self, x, y, z):
        cmd = "C(" + f"{x:.4f}" + ","
        cmd = cmd + f"{y:.4f}" + ","
        cmd = cmd + f"{z:.4f}" + ")"
        self.uconnect.send(cmd)

    def add(self, coord):
        # filtering
        for i, cF in enumerate(self.currFrame):
            dist = (cF[0] - coord[0]) ** 2 + (cF[1] - coord[1]) ** 2 + (cF[2] - coord[2]) ** 2
            if dist <= (self.FILTER ** 2):
                x = cF[0] + (abs(cF[0] - coord[0]) / 2)
                y = cF[1] + (abs(cF[1] - coord[1]) / 2)
                z = cF[2] + (abs(cF[2] - coord[2]) / 2)
                self.currFrame[i] = (x, y, z)
                return
        self.currFrame.append(coord)

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
                                short_dist = (cI, dist)
                            else:
                                if dist < short_dist[1]:
                                    short_dist = (cI, dist)
                if short_dist is not None:
                    c_done[short_dist[0]] = True
                    move.append((pI, short_dist[0]))

        # Destroy/ Create
        for ele in move:
            destroy[ele[0]] = False
            create[ele[1]] = False

        self.uconnect.create(self.currFrame, self.async_get_uid)

        '''
        #debug stuffs
        sendMoveIndex = [item[1] for item in move]
        sendMove = [self.currFrame[i] for i in sendMoveIndex]
        ids = list(range(len(sendMove)))
        desired_list = [x + (z,) for x, (y, z) in zip(ids, sendMove)]
        self.uconnect.move(desired_list)
        '''

        self.prevFrame = list(self.currFrame)
        self.currFrame = []

    def save_to_point_store(self, uid, coord):
        self.pointStore.append((uid, 0, coord))

    def async_get_uid(self, uids):
        if len(uids) != len(self.currFrame):
            raise ValueError("Unexpected number of uid's received from Unity!")
        for i, uid in enumerate(uids):
            self.save_to_point_store(uid, self.currFrame[i])


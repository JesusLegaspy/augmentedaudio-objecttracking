from client.UnityConnectResource import UnityConnect


class UnityTracker:
    RADIUS = 4
    FILTER = 12
    PERSISTENCE = 4  # Frames
    uconnect = UnityConnect()

    TEST_Z = []

    pointStore = []
    frame = []
    create_points = []

    def __init__(self):
        return

    def connect(self, ipaddress, port):
        self.uconnect.connect(ipaddress, port)

    def close(self):
        self.uconnect.close()

    def add(self, coord):
        # filtering
        for i, cF in enumerate(self.frame):
            dist = (cF[0] - coord[0]) ** 2 + (cF[1] - coord[1]) ** 2 + (cF[2] - coord[2]) ** 2
            if dist <= (self.FILTER ** 2):
                x = cF[0] + (abs(cF[0] - coord[0]) / 2)
                y = cF[1] + (abs(cF[1] - coord[1]) / 2)
                z = cF[2] + (abs(cF[2] - coord[2]) / 2)
                self.frame[i] = (x, y, z)
                return
        self.frame.append(coord)

    def next_frame(self):
        done = [False] * len(self.frame)  # link found on curr frame
        move = []
        create = [True] * len(self.frame)

        # logging.debug("***New Frame***")
        # logging.debug("Point store", self.pointStore)

        # Link objects from both frames based on distance
        # Note: this algorithm doesn't try to get the most links possible
        for ps_idx, point in enumerate(self.pointStore):
            short_dist = None
            for fr_idx, coord in enumerate(self.frame):
                if not done[fr_idx]:
                    dist = (coord[0] - point[2][0]) ** 2
                    dist += (coord[1] - point[2][1]) ** 2
                    dist += (coord[2] - point[2][2]) ** 2
                    if dist <= self.RADIUS ** 2:
                        if short_dist is None:
                            short_dist = (fr_idx, dist)
                        else:
                            if dist < short_dist[1]:
                                short_dist = (fr_idx, dist)
            if short_dist is not None:
                done[short_dist[0]] = True
                move.append((ps_idx, short_dist[0]))

        # Create in Unity and add to point store
        for ele in move:
            create[ele[1]] = False
        create_indices = [i for i, c in enumerate(create) if c is True]
        self.create_points = [self.frame[i] for i in create_indices]
        # logging.debug("Added to create points: ", self.create_points)
        if len(self.create_points) != 0:
            self.uconnect.create(self.create_points, self.async_get_uid)

        # Move linked points
        for ele in move:  # todo: optimise with above
            self.pointStore[ele[0]][2] = self.frame[ele[1]]
            self.pointStore[ele[0]][1] = 0
        move_points = [[self.pointStore[ele[0]][0], self.pointStore[ele[0]][2]] for ele in move]
        # logging.debug("Moving following points: ", move_points)
        if len(move_points) != 0:
            self.uconnect.move(move_points)

        # Destroy old points
        destroy_points = []
        new_point_store = []
        for point in self.pointStore:
            if point[1] >= self.PERSISTENCE:
                destroy_points.append([point[0], point[2]])
                continue
            new_point_store.append(point)
            point[1] += 1
        self.pointStore = new_point_store
        # logging.debug("Destroying following points", destroy_points)
        if len(destroy_points) != 0:
            self.uconnect.destroy(destroy_points)

        # Refresh
        self.create_points = []
        self.frame = []

    def async_get_uid(self, uids):
        for i, uid in enumerate(uids):
            print("received uid:", uid)
            self.pointStore.append([uid, 0, self.create_points[i]])


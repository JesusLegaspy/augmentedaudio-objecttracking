from UnityTrackerResource import UnityTracker
from time import sleep
import time

unity = UnityTracker()
unity.connect("192.168.0.101", 13000)
print("Waiting 5 seconds...")
sleep(5)
ticks = time.time()
for x in range(0, 10):
    for x in range(0, 10):
        unity.add((x, x, x))
    unity.next_frame()
    for x in range(0, 10):
        unity.add((x, x, -x))
    unity.next_frame()
    for x in range(0, 10):
        unity.add((x, -x, x))
    unity.next_frame()
    for x in range(0, 10):
        unity.add((x, -x, -x))
    unity.next_frame()
    for x in range(0, 10):
        unity.add((-x, x, x))
    unity.next_frame()
    for x in range(0, 10):
        unity.add((-x, x, -x))
    unity.next_frame()
    for x in range(0, 10):
        unity.add((-x, -x, x))
    unity.next_frame()
    for x in range(0, 10):
        unity.add((-x, -x, -x))
    unity.next_frame()
    for x in range(0, 10):
        unity.add((1, 0, -x))
    unity.next_frame()
    for x in range(0, 10):
        unity.add((0, 1, x))
    unity.next_frame()
for x in range(0,10):
    unity.next_frame()

print('[INFO] Total elapsed time for object tracking: {:.8f}'.format(time.time() - ticks))
sleep(1)
print("Done!")
unity.close()
t = time.time()
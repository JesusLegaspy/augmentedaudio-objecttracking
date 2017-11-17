from UnityTrackerResource import UnityTracker
from time import sleep
import time


unity = UnityTracker()
unity.connect()
print("Waiting 5 seconds...")
sleep(5)
ticks = time.time()
for x in range(0, 10):
    unity.add((x, x, x))
unity.add((15, 15, 15))
unity.next_frame()
for x in range(0, 10):
    unity.add((10 - x, 10 - x, 10 - x))
unity.add((1.25, 1.25, 1.25))
unity.add((-2, -2, -2))
unity.next_frame()
unity.add((20, 20, 20))
unity.next_frame()
unity.add((-20, -20, -20))
unity.next_frame()
unity.add((1, 2, 3))
unity.next_frame()
unity.next_frame()
unity.next_frame()
unity.add((-7, -7, -7))
unity.next_frame()
unity.next_frame()
unity.next_frame()
unity.next_frame()
unity.next_frame()
print('[INFO] Total elapsed time for object tracking: {:.8f}'.format(time.time() - ticks))
sleep(1)
print("Done!")
unity.close()
t = time.time()


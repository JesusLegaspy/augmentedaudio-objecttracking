from UnityTrackerResource import UnityTracker

with UnityTracker() as unity:
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
    print("HELLO!!!")
    unity.add((-7, -7, -7))
    unity.next_frame()
    unity.next_frame()
    unity.next_frame()
    unity.next_frame()
    unity.next_frame()
from Robot_Line_Follower import Robot_Line_Follower
import time
import asyncio

lf = Robot_Line_Follower()
lf.start()
time.sleep(1)
print("running")
lf.stop()
print("done")
time.sleep(3)
lf.start()
time.sleep(3)
print("running again")
lf.stop()
print("done")
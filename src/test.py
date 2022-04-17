from Robot_Line_Follower import Robot_Line_Follower
import time
import asyncio

lf = Robot_Line_Follower()
lf.start()
time.sleep(3)
print("running")
lf.stop()
print("done")
time.sleep(2)
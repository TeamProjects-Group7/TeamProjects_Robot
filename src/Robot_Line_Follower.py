#!/usr/bin/env python
from SunFounder_Line_Follower import Line_Follower
from picar import front_wheels
from picar import back_wheels
import time
import picar
import asyncio
import multiprocessing

class Robot_Line_Follower:
    def __init__(self):
        self.fw = front_wheels.Front_Wheels(db='config')
        self.bw = back_wheels.Back_Wheels(db='config')

# def __init__(self):
    #     picar.setup()
    #     self.forward_speed = 80
    #     self.backward_speed = 70
    #     self.turning_angle = 40
    #     self.max_off_track_count = 40
    #     self.delay = 0.0005
    #     self.fw = front_wheels.Front_Wheels(db='config')
    #     self.bw = back_wheels.Back_Wheels(db='config')
    #     self.lf = Line_Follower.Line_Follower()
    #     self.lf.references = [288.5, 280.5, 285.5, 283.5, 281.5]
    #     self.fw.ready()
    #     self.bw.ready()
    #     self.fw.turning_max = 45

    # def __del__(self):
    #     self.bw.stop()
    #     self.fw.turn(90)

    # def straight_run(self):
    #     while True:
    #         self.bw.speed = 70
    #         self.bw.forward()
    #         self.fw.turn_straight()

    def start(self):
        global loop
        loop = asyncio.get_event_loop()
        loop_in_thread = self.loop_in_thread
        self.proc = multiprocessing.Process(target=loop_in_thread, args=(loop,))
        self.proc.start()
    
    def stop(self):
        self.proc.terminate()
        self.bw.stop()
        self.fw.turn(90)

    def loop_in_thread(self, loop):
        asyncio.set_event_loop(loop)
        follow_line = self.follow_line
        loop.run_until_complete(follow_line())

    @asyncio.coroutine
    def follow_line(self):    
        picar.setup()
        REFERENCES = [288.5, 280.5, 285.5, 283.5, 281.5]
        forward_speed = 80
        backward_speed = 70
        turning_angle = 40
        max_off_track_count = 40
        delay = 0.0005

        lf = Line_Follower.Line_Follower()

        lf.references = REFERENCES
        self.fw.ready()
        self.bw.ready()
        self.fw.turning_max = 45

        off_track_count = 0
        self.bw.speed = forward_speed
        a_step = 3
        b_step = 10
        c_step = 30
        d_step = 45
        self.bw.backward()
        while True:
            lt_status_now = lf.read_digital()
            #print(lt_status_now)
            # Angle calculate
            if	lt_status_now == [0,0,1,0,0]:
                step = 0	
            elif lt_status_now == [0,1,1,0,0] or lt_status_now == [0,0,1,1,0]:
                step = a_step
            elif lt_status_now == [0,1,0,0,0] or lt_status_now == [0,0,0,1,0]:
                step = b_step
            elif lt_status_now == [1,1,0,0,0] or lt_status_now == [0,0,0,1,1]:
                step = c_step
            elif lt_status_now == [1,0,0,0,0] or lt_status_now == [0,0,0,0,1]:
                step = d_step

            # Direction calculate
            if	lt_status_now == [0,0,1,0,0]:
                off_track_count = 0
                self.fw.turn(90)
            # turn right
            elif lt_status_now in ([0,1,1,0,0],[0,1,0,0,0],[1,1,0,0,0],[1,0,0,0,0]):
                off_track_count = 0
                turning_angle = int(90 - step)
            # turn left
            elif lt_status_now in ([0,0,1,1,0],[0,0,0,1,0],[0,0,0,1,1],[0,0,0,0,1]):
                off_track_count = 0
                turning_angle = int(90 + step)
            elif lt_status_now == [0,0,0,0,0]:
                off_track_count += 1
                if off_track_count > max_off_track_count:
                    #tmp_angle = -(turning_angle - 90) + 90
                    tmp_angle = (turning_angle-90)/abs(90-turning_angle)
                    tmp_angle *= self.fw.turning_max
                    self.bw.speed = backward_speed
                    self.bw.forward()
                    self.fw.turn(tmp_angle)
                    
                    lf.wait_tile_center()
                    self.bw.stop()

                    self.fw.turn(turning_angle)
                    time.sleep(0.2)
                    self.bw.speed = forward_speed
                    self.bw.backward()
                    time.sleep(0.2)

                    

            else:
                off_track_count = 0
        
            self.fw.turn(turning_angle)
            #time.sleep(delay)
            yield from asyncio.sleep(delay)
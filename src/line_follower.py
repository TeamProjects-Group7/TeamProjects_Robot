#!/usr/bin/env python
'''
**********************************************************************
* Filename    : line_follower
* Description : An example for sensor car kit to followe line
* Author      : Dream
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Dream    2016-09-21    New release
**********************************************************************
'''

from SunFounder_Line_Follower import Line_Follower
from picar import front_wheels
from picar import back_wheels
import time
import picar

class Robot_Line_Follower:
    def __init__(self):
        picar.setup()
        self.calibrate = True
        self.calibrate = False
        self.forward_speed = 80
        self.backward_speed = 70
        self.turning_angle = 40
        self.max_off_track_count = 40
        self.delay = 0.0005
        self.fw = front_wheels.Front_Wheels(db='config')
        self.bw = back_wheels.Back_Wheels(db='config')
        self.lf = Line_Follower.Line_Follower()
        self.lf.references = [200, 200, 200, 200, 200]
        self.fw.ready()
        self.bw.ready()
        self.fw.turning_max = 45

    def __del__(self):
        self.bw.stop()
        self.fw.turn(90)

    def straight_run(self):
        while True:
            self.bw.speed = 70
            self.bw.forward()
            self.fw.turn_straight()

    def start(self):
        global turning_angle
        off_track_count = 0
        self.bw.speed = self.forward_speed

        a_step = 3
        b_step = 10
        c_step = 30
        d_step = 45
        self.bw.forward()
        self.driving = True
        while self.driving:
            lt_status_now = self.lf.read_digital()
            print(lt_status_now)
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
                if off_track_count > self.max_off_track_count:
                    #tmp_angle = -(turning_angle - 90) + 90
                    tmp_angle = (turning_angle-90)/abs(90-turning_angle)
                    tmp_angle *= self.fw.turning_max
                    self.bw.speed = self.backward_speed
                    self.bw.backward()
                    self.fw.turn(tmp_angle)
                    
                    self.lf.wait_tile_center()
                    self.bw.stop()

                    self.fw.turn(turning_angle)
                    time.sleep(0.2)
                    self.bw.speed = self.forward_speed
                    self.bw.forward()
                    time.sleep(0.2)

                    

            else:
                off_track_count = 0
        
            self.fw.turn(turning_angle)
            time.sleep(self.delay)

        def stop(self):
            self.driving = False
#!/usr/bin/env python3
import serial
from constants import DIM

class Wheel:
    def __init__(self, id, flipVel=False):
        # If flipVel is true, the velocity commands to this wheel are multiplied by -1
        # This is because the wheels need to be spinning in opposite directions for the robot to move forward/backward
        # However, the velocity calculated by the unicycle model will give wheel vels of the same sign
        self.id = id
        self.current_vel = 0.
        self.goal_vel = 0.
        self.pos = 0
        self.flipVel = flipVel
    
    def set_rot_vel(self, goal_vel):
        self.goal_vel = goal_vel
        if self.flipVel:
            self.goal_vel *= -1

class RobotVelocityController:
    def __init__(self, baud=115200):
        self.serial_handler=serial.Serial(port='/dev/ttyUSB0', baudrate=baud, timeout=1)
        self.serial_handler.flush()

        # Initialize wheels
        self.wheels = {"right":Wheel('right'), "left":Wheel('left', flipVel=True)}


    def get_command_from_vel(self, right_vel, left_vel):
        return f"<{right_vel:.2f},{left_vel:.2f}>".encode('utf-8')
    
    def parse_feedback(self, inp):
        # Example input: b'(1.00,1.00,14824,14558)\r\n'
        # 4 comma-separated values:
        # 1: right wheel vel
        # 2: left wheel vel
        # 3: right wheel encoder pos
        # 4: left wheel pos
        try:
            out = inp.decode('utf-8').replace('(', '').replace(')', '').rsplit()[0].split(',')
            if(len(out) == 4):
                self.wheels["right"].current_vel = out[0]
                self.wheels["left"].current_vel = out[1]
                self.wheels["right"].pos = out[2]
                self.wheels["left"].pos = out[3]
        except:
            pass
    
    def get_goal_robot_vel(self):
        '''
        Get the goal linear vel and angular vel of the robot here
        This function should be redefined when writing a ros wrapper
        Returning hardcoded values for now
        '''
        v = 0.12 # This is the speed of the robot at 1.0 rad/sec wheel speed
        w = 0.0
        return v,w

    def calc_wheel_vel_from_goal_vel(self, v, w=0.0):
        '''
        Store the wheel velocities required for the robot to move with a given linear and angular velocity using the unicycle model
        Calculated values are stored in the wheel class instances for this 
        @param v goal linear velocity
        @param w goal angular velocity
        '''
        r_vel = (2*v+ w*DIM.wheel_sep)/2/DIM.wheel_rad
        l_vel = (2*v -  w*DIM.wheel_sep)/2/DIM.wheel_rad

        self.wheels["right"].set_rot_vel(r_vel)
        self.wheels["left"].set_rot_vel(l_vel)

    def handle_arduino(self):
        self.serial_handler.write(self.get_command_from_vel(self.wheels["right"].goal_vel,
                                                            self.wheels["left"].goal_vel))
        self.parse_feedback(self.serial_handler.readline())


if __name__ == '__main__':
    from time import sleep
    rc = RobotVelocityController()
    while True:
        goal_v, goal_w = rc.get_goal_robot_vel()
        rc.calc_wheel_vel_from_goal_vel(goal_v, goal_w)
        rc.handle_arduino()

        sleep(1.0)
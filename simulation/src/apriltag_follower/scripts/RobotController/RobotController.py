#!/usr/bin/evn python3
#Author: mike4192 https://github.com/mike4192/spotMicro

import numpy as np
import tf
from . StateCommand import State, Command, BehaviorState
from . TrotGaitController import TrotGaitController

class Robot(object):

    def __init__(self, body, legs, imu):
        self.body = body
        self.legs = legs

        self.delta_x = self.body[0] * 0.5
        self.delta_y = self.body[1] * 0.5 + self.legs[1]
        self.x_shift_front = 0.006
        self.x_shift_back = -0.03
        self.default_height = 0.15

        self.trotGaitController = TrotGaitController(self.default_stance,
            stance_time = 0.18, swing_time = 0.34, time_step = 0.02,
            use_imu = imu)

        self.currentController = self.trotGaitController

        # reconfigure state
        self.state = State(self.default_height)
        self.state.foot_locations = self.default_stance
        self.state.behavior_state = BehaviorState.TROT
        self.state.ticks = 0

        self.currentController.pid_controller.reset()
        self.command = Command(self.default_height)


    def joystick_command(self,msg):
        self.currentController.updateStateCommand(msg, self.state, self.command)
    
    def imu_orientation(self,msg):
        q = msg.orientation
        rpy_angles = tf.transformations.euler_from_quaternion([q.x,q.y,q.z,q.w])
        self.state.imu_roll = rpy_angles[0]
        self.state.imu_pitch = rpy_angles[1]

    def run(self):
        return self.currentController.run(self.state, self.command)

    @property
    def default_stance(self):
        # FR, FL, RR, RL
        return np.array([[self.delta_x + self.x_shift_front,self.delta_x + self.x_shift_front,-self.delta_x + self.x_shift_back,-self.delta_x + self.x_shift_back],
                         [-self.delta_y                    ,self.delta_y                     ,-self.delta_y                    , self.delta_y                    ],
                         [0                                ,0                                ,0                                ,0                                ]])

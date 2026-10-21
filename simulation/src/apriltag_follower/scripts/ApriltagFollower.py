#!/usr/bin/env python3

import rospy 
import numpy as np
from sensor_msgs.msg import Joy
from RobotController import RobotController
from InverseKinematics import robot_IK
from std_msgs.msg import Float64


class ApriltagFollower:

    def __init__(self):
        rospy.init_node('apriltag_follower_node')

        self.distance_to_camera = 0

        self.rate = rospy.Rate(60)

        # Robot geometry
        self.body = [0.1908, 0.080]
        self.legs = [0.0, 0.04, 0.100, 0.094333] 
        self.bittle_robot = RobotController.Robot(self.body, self.legs, False)
        self.inverseKinematics = robot_IK.InverseKinematics(self.body, self.legs)

        self.publishers = []
        self.initialize_publishers()
        rospy.Subscriber('/distance_to_camera', Float64,callback=self.distance_to_camera_callback)
        rospy.Subscriber("bittle_joy/joy_ramped",Joy,self.bittle_robot.joystick_command)

    def initialize_publishers(self):
        """ This method is for publishing throttling values to move the robot """

        command_topics = ["/apriltag_follower/FR1_joint/command",
                  "/apriltag_follower/FR2_joint/command",
                  "/apriltag_follower/FR3_joint/command",
                  "/apriltag_follower/FL1_joint/command",
                  "/apriltag_follower/FL2_joint/command",
                  "/apriltag_follower/FL3_joint/command",
                  "/apriltag_follower/RR1_joint/command",
                  "/apriltag_follower/RR2_joint/command",
                  "/apriltag_follower/RR3_joint/command",
                  "/apriltag_follower/RL1_joint/command",
                  "/apriltag_follower/RL2_joint/command",
                  "/apriltag_follower/RL3_joint/command"]

        for i in range(len(command_topics)):
            self.publishers.append(rospy.Publisher(command_topics[i], Float64, queue_size = 0))
        

    def distance_to_camera_callback(self,msg):
        self.distance_to_camera = msg.data

        #####################################
        # Feeback control loop
        #####################################
        if self.distance_to_camera > 0.2:
            self.moving_forward()
        else:
            self.stop()

    def moving_forward(self):
        self.bittle_robot.trotGaitController.max_x_velocity = 0.15 
        self.bittle_robot.trotGaitController.max_y_velocity = 0.0
        # self.bittle_robot.trotGaitController.max_yaw_rate = 0.0 

    def moving_backward(self):
        self.bittle_robot.trotGaitController.max_x_velocity = -0.15 
        self.bittle_robot.trotGaitController.max_y_velocity = 0.0 
        self.bittle_robot.trotGaitController.max_yaw_rate = 0.0 

    def moving_right(self):
        self.bittle_robot.trotGaitController.max_x_velocity = 0.0 
        self.bittle_robot.trotGaitController.max_y_velocity = -0.15 
        self.bittle_robot.trotGaitController.max_yaw_rate = 0.0 

    def moving_left(self):
        self.bittle_robot.trotGaitController.max_x_velocity = 0.0 
        self.bittle_robot.trotGaitController.max_y_velocity = 0.15 
        self.bittle_robot.trotGaitController.max_yaw_rate = 0.0 
        
    def stop(self):
        self.bittle_robot.trotGaitController.max_x_velocity = 0.0 
        self.bittle_robot.trotGaitController.max_y_velocity = 0.0
        self.bittle_robot.trotGaitController.max_yaw_rate = 0.0 
    

    def initialize_trot_controller(self):
        pub = rospy.Publisher("bittle_joy/joy_ramped", Joy,queue_size=10)
        cmd = Joy()
        cmd.buttons = [0,1,0,0,0,0,0,0] # trot
        cmd.axes = list(np.array([0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]*7 ) )
        pub.publish(cmd)

    def follow(self):
        # initializing trot controller
        pub = rospy.Publisher("bittle_joy/joy_ramped", Joy,queue_size=10)

        a = np.array([0,0.1,0.1,0.0,0.2,0.1,0.1,0.1]*7 ) 

        cmd = Joy()
        cmd.buttons = [0,1,0,0,0,0,0,0] # trot
        cmd.axes = list(a)
        
        while not rospy.is_shutdown():
            pub.publish(cmd)
            # initialize running operation
            leg_positions = self.bittle_robot.run()

            # update leg positions
            dx = self.bittle_robot.state.body_local_position[0] 
            dy = self.bittle_robot.state.body_local_position[1]
            dz = self.bittle_robot.state.body_local_position[2] 
            
            roll = self.bittle_robot.state.body_local_orientation[0]
            pitch = self.bittle_robot.state.body_local_orientation[1]
            yaw = self.bittle_robot.state.body_local_orientation[2]

            roll = 0
            pitch = 0
            yaw = 0

            try:
                joint_angles = self.inverseKinematics.inverse_kinematics(leg_positions,
                                    dx, dy, dz, roll, pitch, yaw)

                for i in range(len(joint_angles)):
                    self.publishers[i].publish(joint_angles[i])
            except:
                print("error")

            # print(self.distance_to_camera)

            self.rate.sleep()


if __name__ =='__main__':
    follower = ApriltagFollower()
    follower.follow()
#!/usr/bin/env python3
import cv2
import time
import yaml
import rospy
import apriltag
import numpy as np  
from time import sleep
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float64

class ApriltagDetector:
    def __init__(self,K,apriltag_family="tag36h11",TAG_SIZE = .1):
        rospy.init_node('apriltag_detection_node')

        options = apriltag.DetectorOptions(families=apriltag_family,nthreads=4)
        self.detector = apriltag.Detector(options=options)
        self.camera_params = [K[0,0],K[1,1],K[0,2],K[1,2]] #elements from the K matrix
        self.TAG_SIZE = TAG_SIZE #Tag size from Step 1 in meters 
        self.cv_bridge = CvBridge()
        rospy.Subscriber('/bittle/camera1/image_raw', Image,self.camera_callback)

        self.pub = rospy.Publisher('distance_to_camera', Float64)

    def camera_callback(self,msg):
        try:
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg,desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
        
        # image restructuring
        height, width, channels = cv_image.shape
        decenter = 160
        rows_to_watch = 60
        # crop_img = cv_image[(height)/2 + decenter : (height)/2 + (decenter+rows_to_watch)][1:width]

        # convert to gray
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        results = np.array(self.detect_tags(image=gray,detector=self.detector,camera_params=self.camera_params))
        try:
            dist_to_cam = results[0][2][-1]
            print(f"dist= {dist_to_cam}")
            self.pub.publish(dist_to_cam)
        except:
            pass

    def detect_tags(self,
                image,
                detector,
                camera_params,
                tag_size=0.0762,
               ):

        gray = image
        detections, dimg = detector.detect(gray, return_image=True)
        overlay = gray // 2 + dimg // 2
        num_detections = len(detections)
        result = []

        for i, detection in enumerate(detections):
            pose, e0, e1 = detector.detection_pose(detection, camera_params, tag_size)
            #result.extend([detection, pose, e0, e1])
            result.append(pose)
            
        return result 



if __name__ == "__main__":
    K = np.array([[513.5091901768432, 0.0, 333.556219601284],[0.0, 514.0481036608813, 264.0053560914043],[0,0,1]])
    apriltag_detector = ApriltagDetector(K)
    print("Starting")
    rospy.spin()

#!usr/bin/python
import threading
import os, sys
import cv2
import time
import apriltag
import yaml
sys.path.append("/home/pi/OpenCat/serialMaster") # set the path to where Opencat is located on your Pi
from ardSerial import *
import Camera


class AprilTag:

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False
        self.command = ""  # can contain gaits and skills
        self.key = 255  # the last key that was pressed for remote control
        self.goodPorts = {}
        #connectPort(self.goodPorts) # for connecting to the NyBoard
            
    def getPicture():

        video_getter = Camera.VideoGet(0)
        video_getter.start()
        image = video_getter.frame

        return image


    def start(self):
        threading.Thread(target=self.localize, args=()).start()
        return self

    def leftOrRight(self,img):

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        #tag family??
        options = apriltag.DetectorOptions(
            border=1,
            nthreads=4,
            quad_decimate=1.0,
            quad_blur=0.0,
            refine_edges=True,
            refine_decode=False,
            refine_pose=True,
            debug=False,
            quad_contours=True)

        detector = apriltag.Detector(options)

        img_cx = img.shape[1] / 2
        
        while True:
            
            try:

                tags = detector.detect(gray)
                x = int(tags[0].center[0])
                print(tags[0].family)

                if x/img_cx > 6/5:

                    print("Turning Right") #add turn comment, can be also used with return flag = 'right'
                    self.command = 'kcrR'
                    #send(self.goodPorts, [self.command, "\n"])

                elif x/img_cx < 4/5:

                    print("Turning Left") #add turn comment, can be also used with return flag = 'left'
                    self.command = 'kcrL'
                    #send(self.goodPorts, [self.command, "\n"])

                else:

                    print('Going Straight')
                    self.command = 'kcrF'
                    #send(self.goodPorts, [self.command, "\n"])

            except: 
                print('Apriltag not found.')
               
                self.command = 'kbalance'
                #send(self.goodPorts, [self.command, "\n"])                

            time.sleep(2)

        

    def poseEstimation(self,img,cameraMatrix):
        
        # options = apriltag.DetectorOptions(
        #     border=1,
        #     nthreads=4,
        #     quad_decimate=1.0,
        #     quad_blur=0.0,
        #     refine_edges=True,
        #     refine_decode=False,
        #     refine_pose=True,
        #     debug=False,
        #     quad_contours=True)

        detector = apriltag.Detector()
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        tag = detector.detect(gray)
        tag_size = 1 #dummy
        cameraParams = [cameraMatrix[0][0],cameraMatrix[1][1],cameraMatrix[0][2],cameraMatrix[1][2]] # fx, fy, cx, cy
        #print(cameraParams)
        pose = detector.detection_pose(tag[0], cameraParams, tag_size)
        print(pose)
        return pose

    def calibrationResults(self):

        with open(r'calibrationResults.yaml') as file:
            data = yaml.full_load(file)
            cameraMatrix = data['camMatrix']
            return(cameraMatrix)
    
    def stop(self):
        self.stopped = True






# class movement():
#      def __init__(self):
#         self.stopped = False
#         self.command = ""  # can contain gaits and skills
#         self.key = 255  # the last key that was pressed for remote control
#         self.goodPorts = {}
#         connectPort(self.goodPorts) # for connecting to the NyBoard





#imagePath = 'image4.jpg'
#img = cv2.imread(imagePath)

tag = AprilTag()
img = tag.getPicture()
cameraMatrix = tag.calibrationResults()

tag.leftOrRight(img)

#tag.poseEstimation(img, cameraMatrix)


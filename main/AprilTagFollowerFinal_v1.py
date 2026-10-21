#!usr/bin/python
import threading
import os
import cv2
import time
import apriltag
import yaml

class AprilTag:

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False
            
    def start(self):
        threading.Thread(target=self.localize, args=()).start()
        return self

    def leftOrRight(self,img):

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        options = apriltag.DetectorOptions(families='tag36h11',
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

                if x/img_cx > 6/5:

                    print("Turning Right") #add turn comment, can be also used with return flag = 'right'

                elif x/img_cx < 4/5:

                    print("Turning Left") #add turn comment, can be also used with return flag = 'left'

                else:

                    print('Going Straight')

            except: 
                print('Apriltag not found.')

            time.sleep(1)

        

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



imagePath = 'image2.jpg'
img = cv2.imread(imagePath)
tag = AprilTag()
cameraMatrix = tag.calibrationResults()

#tag.leftOrRight(img)

tag.poseEstimation(img, cameraMatrix)


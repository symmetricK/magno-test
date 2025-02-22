#!/usr/bin/env python3

# Developed by Logan Rower
## Referenced Dickinson Lab

# 6.7.22 developed circle finding funcitonality
# 6.9.22 started developing the node to use Raw Image

from __future__ import print_function

import roslib
import sys
import rospy
import cv2
from std_msgs.msg import Header
from std_msgs.msg import String
from sensor_msgs.msg import Image

from cv_bridge import CvBridge, CvBridgeError
from datetime import datetime
#this is message type that you will subscribe to
#from basic_led_strip_ros.msg import StripLEDInfo
from basic_led_strip_ros.msg import LEDinfo
import os
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import queue
import time 
from std_msgs.msg import Float64

from magnotether.msg import MsgAngleData

from find_fly_angle import find_fly_angle 

# CHANGE SOURCE FOLDER TO ONE SPECFICALLY FOR ALIGNMENT?
## BELOW BASICALLY WILL AUTOMATICALLY SET THE PARAMS FOR THE CURRENT FLY...

# New class for aligning the fruit fly initially before the experiment.
class FlyAlign:  

    def __init__(self):
        
        rospy.init_node('fly_align', anonymous=True)
        self.bridge = CvBridge()
        rospy.on_shutdown(self.clean_up)

        # Subscribed to the raw image data from the pylon camera node
        self.image_sub = rospy.Subscriber("/pylon_camera_node/image_raw",Image,self.callback)
        rospy.logwarn('subscribed')

        self.queue = queue.Queue()

        self.threshold = 50
        self.mask_scale = 0.9
        self.frame_count = 0
        self.image_save_duration=60

        ##tw added
        ###You need to change self.data_path to a valid path for your filesystem
        ###e.g. '/home/giraldolab/data/'
        

        
        
    
        # Set the window for the continuously updating images..
        cv2.namedWindow('fly alignment', cv2.WINDOW_NORMAL)
        # moveable window
        cv2.moveWindow('fly alignment', 100, 100)

        # resize the windows
        cv2.resizeWindow('fly alignment',50,50)
        
    def clean_up(self):
        cv2.destroyAllWindows()

    def callback(self,data): 
        
        self.queue.put(data)
        
        #rospy.logwarn('printing queue_size')
        #rospy.logwarn(np.shape(tst))

    def run(self): 

        start_time=time.time()
        image_save_count=0
        while not rospy.is_shutdown():

            # Pull all new data from queue
            new_image_list = []
           
            # if self.current_led_position==149:
            #     break
            # while True:
                
            
            while(True):

                #try:
                ros_image = self.queue.get()

                new_image_list.append(ros_image)
                #rospy.logwarn(len(new_image_list))
                if len(new_image_list)>5:
                #rospy.logwarn('dropping frames')
                    new_image_list=new_image_list[-2:]

                #except queue.Empty:
                    #rospy.logwarn('re')
                    #print('error getting image')    
                 #   break

            for image_ct,ros_image in enumerate(new_image_list):
                rospy.logwarn('inside image loop')
                # try:
                cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
                #     cv2.imshow('fly alignment', cv_image)
                #     rospy.logwarn('showing alignment image')
                #     rospy.sleep(0.001)
                #     cv2.waitKey(1)
                     
                # except CvBridgeError as e:
                #     rospy.logwarn('error')
                #     print(e)

                self.frame_count += 1

                # Now that we have added a frame we can then 

                # IN HERE WE NEED TO EXECUTE THE CIRCLE...
                ### TEST CIRCLE...
                coord = [562, 551]
                radius = 20
                color = (255,0,0)
                thickness = 2
                cv2.circle(cv_image, coord, radius, color, thickness)
                # convert the image in to a grayscale..
                #cv_image_in = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)  
                
                #rospy.logwarn(np.shape(cv_image_in))
                # red_image=cv_image_in[:,360:1560]
               
                cr_time=time.time()
            

                #if cr_time-start_time<self.image_save_duration:
                    #image_save_count=image_save_count+1
                    #image_add_str=str(image_save_count).rjust(4, '0')

                    #image_file_name=self.image_file_name_base + image_add_str + '.png'
                    #rospy.logwarn(image_file_name)
                    #cv2.imwrite(self.image_path+image_file_name,self.angle_data['raw_image'])
                        
                #if image_ct==0:
                cv2.imshow('fly alignment', cv_image)
                #cv2.imshow('rotated image', self.angle_data['rotated_image'])
                rospy.sleep(0.001)
                cv2.waitKey(1)


# ---------------------------------------------------------------------------------------
if __name__ == '__main__': 
    test= FlyAlign()
    try:
        test.run()
    except rospy.ROSInterruptException:
        sys.exit()

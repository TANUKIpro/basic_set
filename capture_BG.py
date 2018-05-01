#!/usr/bin/env python

import os, time, sys
import cv2
import rospy
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from message_filters import ApproximateTimeSynchronizer, TimeSynchronizer, Subscriber

CAPTURE_RATE = 5.

class Capture_BG:
    def __init__(self, path):
        
        self.bridge = CvBridge()        
        image_sub = Subscriber('image', Image)
        self.sub = ApproximateTimeSynchronizer([image_sub], 10, .5)        
        
        self.path = path
        self.count = 0
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        files = filter(lambda x: x.startswith(basename) and x.endswith('.png'), os.listdir(dirname))
        if files:
            nums = [f.strip('.png').split('_')[-1] for f in files if '_' in f]
            nums = [int(num) for num in nums if num.isdigit()]
            if nums:
                self.count = max(nums) + 1
    
    def image_save(self, image):
        filename = self.path + '_%04d.png'%self.count
        cv2.imwrite(filename, image)
        self.count += 1

    def callback(self, image):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(image, 'bgr8')
        except CvBridgeError as e:
            rospy.logerr(e)
        
        self.image_save(self.cv_image)
        print "callback"
        cv2.imshow("image", self.cv_image)
        cv2.waitKey(1)
        
    def start(self):
        self.sub.callbacks.clear()
        self.rate = rospy.Rate(CAPTURE_RATE)
        self.sub.registerCallback(self.callback)
    
if __name__ == '__main__':
    path = sys.argv[1]
    rospy.init_node('capture_image')
    cbg = Capture_BG(path)
    rospy.loginfo('Images will be saved as "{}_xxxx.png."'.format(path))
    print('It starts in 5 seconds')
    time.sleep(5)
    while not rospy.is_shutdown():
        cbg.start()
    rospy.spin()

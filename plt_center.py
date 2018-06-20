#!/usr/bin/env python
#-*- coding:utf-8 -*-

import cv2
import numpy as np

def aimer(image, window_name):
    height, width, channels = image.shape
    
    cv2.line(image, (0, height/2), (width, height/2), (0, 0, 255), 1)
    cv2.line(image, (width/2, 0), (width/2, height), (0, 0, 255), 1)
    cv2.circle(image, (width/2, height/2), 100, (0, 0, 255), 1)
    cv2.circle(image, (width/2, height/2), 150, (0, 0, 255), 1)
    cv2.circle(image, (width/2, height/2), 200, (0, 0, 255), 1)
    
    fontType = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, "PLS aim the target to center ", (width/8, height-10), fontType, 1, (255, 255, 255), 1)

    cv2.imshow(window_name, image)


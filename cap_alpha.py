import sys, os
import rospy
from sensor_msgs.msg import Image
from mask_rcnn.client import Client
import numpy as np
import cv2
from cv_bridge import CvBridge
from plt_center import aimer

rospy.init_node('visualize_mask_rcnn')
mask_rcnn = Client()
bridge = CvBridge()

img_path = sys.argv[1]
print('Images will be saved as "{}_xxxx.png."'.format(img_path))

dirname = os.path.dirname(img_path)
name = os.path.basename(img_path)
files = filter(lambda x: x.startswith(name) and x.endswith('png'), os.listdir(dirname))
if files:
        nums = [f.strip('.png').split('_')[-1] for f in files if '_' in f]
        nums = [int(num) for num in nums if num.isdigist()]
count = 0

def data_saver(img, path):
    global count
    global nums
    filename = path + '_%04d.png'%count
    cv2.imwrite(filename, img)
    count += 1

def cb(imgmsg):
    image = bridge.imgmsg_to_cv2(imgmsg, 'bgr8')
    masks = mask_rcnn.process_image(image, 'bgr8')
    total = np.zeros(image.shape[:2]+(1,), dtype=np.float32)
    max_probability = 0.0
    counter = 0

    for mask in masks:
        if mask.name != 'person':
            continue
        
        mask_a = np.uint8(np.dstack([image, mask.mask*255]))
        mask_a = mask_a[int(mask.top):int(mask.bottom),int(mask.left):int(mask.right)]
	    
	    m_width =  int(mask.right + ((mask.right - mask.left)/2))
        m_height = int(mask.top + ((mask.bottom - mask.top)/2))
	    
        #cv2.circle(image, (m_width, m_height), 10, (255, 0, 255), 1)
        #print '%s (%f%%)' % (mask.name, mask.probability*100)
        total += np.expand_dims(mask.mask, -1) * mask.probability
        
        counter += 1
        print counter
    
    
    total[total>1.] = 1.
    height, width, channels = image.shape

    cv2.imshow('original', image)
    aimer(np.uint8(image*total), 'center_plt')
    cv2.moveWindow('center_plt', 0, width)
    cv2.waitKey(1)

rospy.Subscriber('/hsrb/head_rgbd_sensor/rgb/image_rect_color', Image, cb)
rospy.spin()

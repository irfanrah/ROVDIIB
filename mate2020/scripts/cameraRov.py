#!/usr/bin/python

import cv2
#from skimage import exposure
from cv_bridge import CvBridge, CvBridgeError
import rospy
from sensor_msgs.msg import  CompressedImage
import numpy as np

#def RecoverCLAHE(sceneRadiance):
    #clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(4, 4))
    #for i in range(3):
      #  sceneRadiance[:, :, i] = clahe.apply((sceneRadiance[:, :, i]))
    # return sceneRadiance

rospy.init_node("cameraROV")
# image_publisher = rospy.Publisher("/rov/image", Image, queue_size=8)
proccessed_image_publisher = rospy.Publisher("/rov/image/compressed", CompressedImage, queue_size=8)

vid = cv2.VideoCapture(1)
bridge = CvBridge()

while not rospy.is_shutdown():
    success, img = vid.read()
    resize = cv2.resize(img, (480,360))
    if img is None:
        break
    new_img = resize.copy()
    proccessed_image = CompressedImage()
    proccessed_image.header.stamp = rospy.Time.now()
    proccessed_image.format = "jpeg"
    proccessed_image.data = np.array(cv2.imencode(".jpg", new_img)[1]).tostring()
    proccessed_image_publisher.publish(proccessed_image)
    # new_img = RecoverCLAHE(new_img)

    # imgmsg = bridge.cv2_to_imgmsg(new_img, "bgr8")
    # comp_imgmsg = bridge.cv2_to_compressed_imgmsg()
    # image_publisher.publish(imgmsg)

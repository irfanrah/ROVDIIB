#!/usr/bin/python

import numpy as np
import cv2
from skimage import exposure
from cv_bridge import CvBridge, CvBridgeError
import rospy
from sensor_msgs.msg import Image, CompressedImage
# from Tkinter import *

angka = 50

def nothing(angka):
    pass

def RecoverCLAHE(sceneRadiance):
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(4, 4))
    for i in range(3):
        sceneRadiance[:, :, i] = clahe.apply((sceneRadiance[:, :, i]))
    return sceneRadiance

def image_callback(img):
    global frame
    ori_cv2 = np.fromstring(img.data, np.uint8)
    ori_cv2 = cv2.imdecode(ori_cv2, cv2.IMREAD_COLOR)
    frame = ori_cv2

if __name__ == '__main__':
    rospy.init_node("cameraGCS")

    # window = Tk()

    # window.title("Welcome to LikeGeeks app")

    # window.mainloop()

    image_subscriber = rospy.Subscriber('/rov/image/compressed', CompressedImage, image_callback)

    np.seterr(over='ignore')
    # cv2.startWindowThread()
    cv2.namedWindow("Trackbar")
    cv2.namedWindow("op")
    # cv2.namedWindow("clahe")
    cv2.createTrackbar("x", "Trackbar" , 0, 1024, nothing)
    cv2.createTrackbar("y", "Trackbar" , 0, 768, nothing)
    # vid = cv2.VideoCapture(0)
    bridge = CvBridge()

    while not rospy.is_shutdown():
        gambarmsgs = rospy.wait_for_message('/rov/image/compressed', CompressedImage)
        if frame is None:
            break
        new_img = frame.copy()


        cv2.imshow("clahe", new_img)
        #cv2.imshow("op", mask1)
        cv2.waitKey(30)

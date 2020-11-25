#!/usr/bin/python

import os
import numpy as np
import cv2
from skimage import exposure
from cv_bridge import CvBridge, CvBridgeError
import rospy
from sensor_msgs.msg import Image

angka = 50

def nothing(angka):
    pass

def RecoverCLAHE(sceneRadiance):
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(4, 4))
    for i in range(3):
        sceneRadiance[:, :, i] = clahe.apply((sceneRadiance[:, :, i]))
    return sceneRadiance

rospy.init_node("cariHSV")

np.seterr(over='ignore')
# cv2.startWindowThread()
cv2.namedWindow("Trackbar")
cv2.namedWindow("op")
# cv2.namedWindow("clahe")
cv2.createTrackbar("x", "Trackbar" , 0, 1024, nothing)
cv2.createTrackbar("y", "Trackbar" , 0, 768, nothing)
# vid = cv2.VideoCapture(0)
# bridge = CvBridge()

while not rospy.is_shutdown():
    x = cv2.getTrackbarPos("x", "Trackbar")
    y = cv2.getTrackbarPos("y", "Trackbar")
    img = cv2.imread('/home/nathan/Pictures/coral.png')
    # success, img = vid.read()
    if img is None:
        break
    new_img = img.copy()
    new_img = RecoverCLAHE(new_img)

    # KALO MAU DI PUBLISH
    # imgmsg = bridge.cv2_to_imgmsg(new_img, "bgr8")
    # image_publisher.publish(imgmsg)

    # cv2.imshow('clahe', new_img)
    # cv2.imshow('apa', img)

    roi = new_img[y-5:y+5, x-5:x+5]
    hue = np.mean(roi[:,:, 0])
    sat = np.mean(roi[:,:, 1])
    val = np.mean(roi[:,:, 2])

    h_low = hue - angka
    h_high = hue + angka
    s_low = sat - angka
    s_high = sat + angka
    v_low = val - angka
    v_high = val + angka

    print(h_low, h_high, s_high, s_low, v_high,v_low)

    # h_low = 74
    # s_low = 84
    # v_low = 100
    # h_high = 164
    # s_high = 174
    # v_high = 190
    # print("low ", end='')
    # print((h_low, s_low, v_low))
    # print("high ", end='')
    # print((h_high, s_high, v_high))

    cv2.circle(new_img, (x,y), 5, (255, 255, 255), thickness=1, lineType=8, shift=0)
    mask1 = cv2.inRange(new_img, (h_low, s_low, v_low), (h_high, s_high, v_high))
    kernel = np.ones((15, 2) ,np.uint8)
    erosion = cv2.erode(mask1,kernel,iterations = 1)
    _, contours, _= cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 200:
            continue
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.drawContours(new_img, contours, -1, (0,0,0), 2)
        # cv2.rectangle(new_img, (x, y), (x + w, y + h), (0, 255,0), 2)
    # cv2.imshow("apa", img)
    cv2.imshow("clahe", new_img)
    cv2.imshow("op", mask1)
    cv2.waitKey(30)

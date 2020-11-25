#!/usr/bin/python

import cv2
import rospy
import Tkinter
from PIL import Image, ImageTk
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CompressedImage
import numpy as np
from random import randint
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

ori = np.zeros([2000,1500, 3], dtype=np.uint8) #DISINI
count = 0 #mulai dari 0
path1 = 'logo.jpg'
path2 = 'ui.png'
path3 = 'dtm.jpeg'
path4 = 'ime.jpeg'

global axis
def image_callback(img):
	global ori
	ori_cv2 = np.fromstring(img.data, np.uint8)
	ori_cv2 = cv2.imdecode(ori_cv2, cv2.IMREAD_COLOR)
	ori = ori_cv2

def joystick_call(data):
	global L2
	global R2
	L2 = data.axes[2]
	R2 = data.axes[5]

if __name__ == '__main__':

	rospy.init_node('tkinter', anonymous=True)
	# image_subscriber = rospy.Subscriber("/rov/image", ROSImage, image_callback)
	image_subscriber_compressed = rospy.Subscriber("/rov/image/compressed", CompressedImage, image_callback)
	
	rospy.Subscriber("joy",Joy ,joystick_call)

	master = Tkinter.Tk() #ngebuat tkinter
	master.title("TKinter MATE")
	frame = Tkinter.Frame(master=master)
	master.geometry("1200x1000") 
	
	
	ori_label = Tkinter.Label(master=master, image=None)
	ori_label.place(x = 0, y =0)

	
	slider_frame1 = Tkinter.Frame(master=master)	
	Info_frame = Tkinter.Frame(master=master)

	imga1 = ImageTk.PhotoImage(Image.open(path1))
	Tkinter.Label(master=master, image=imga1).place(x=100,y=400)
	imga2 = ImageTk.PhotoImage(Image.open(path2))
	Tkinter.Label(master=master, image=imga2).place(x=480,y=250)
	imga3 = ImageTk.PhotoImage(Image.open(path3))
	Tkinter.Label(master=master, image=imga3).place(x=750,y=280)
	imga4 = ImageTk.PhotoImage(Image.open(path4))
	Tkinter.Label(master=master, image=imga4).place(x=980,y=280)


	Tkinter.Label(master=master, text="Suhu", fg='green',bg = 'white',bd = '10' ,font=("Helvetica", 15)).place(x = 650, y = 13)
	Tkinter.Label(master=master, text="Tekanan", fg='blue',bg = 'white',bd = '10' , font=("Helvetica", 15)).place(x = 650, y = 123)
	Tkinter.Label(master=master, text="Kedalaman", fg='red',bg = 'white',bd = '10' , font=("Helvetica", 15)).place(x = 650, y = 203)
	Tkinter.Label(master=master, text="C", fg='green',bg = 'white',bd = '10' ,font=("Helvetica", 15)).place(x = 860, y = 13)
	Tkinter.Label(master=master, text="KPa", fg='blue',bg = 'white',bd = '10' , font=("Helvetica", 15)).place(x = 860, y = 123)
	Tkinter.Label(master=master, text="cm", fg='red',bg = 'white',bd = '10' , font=("Helvetica", 15)).place(x = 860, y = 203)
	Info_frame.grid(row=1, column=1)
	rate = rospy.Rate(2)
	
	L2 = None
	R2 = None
	kedalam = 0
	while not rospy.is_shutdown():
		if ori is not None:
			b,g,r = cv2.split(ori)
			img = cv2.merge((r,g,b)) 
			im = Image.fromarray(img)
			imgtk = ImageTk.PhotoImage(image=im)
			ori_label.config(image=imgtk)
			
			
			count = count + 1
		if R2 == float(-1.0):
			kedalam = kedalam + 0.05
		if L2 == float(-1.0):
			kedalam = kedalam - 0.05
		if count >= 30:
			Tkinter.Label(master=master, text="25", fg='black',bg = 'green',bd = '3' ,font=("Helvetica", 15)).place(x = 800, y = 20)
			Tkinter.Label(master=master, text=str(kedalam*10), fg='black',bg = 'blue',bd = '3' , font=("Helvetica", 15)).place(x = 800, y = 130)
			Tkinter.Label(master=master, text=str(kedalam), fg='black',bg = 'red',bd = '3' , font=("Helvetica", 15)).place(x = 800, y = 210)
			count = 0
		master.update()

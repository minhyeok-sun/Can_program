#!/usr/bin/env python
import rospy
import cv2
import numpy as np
import time
from kaai_can.msg import Mobileye_det
blue = (255, 0, 0)
red = (0, 0, 255)
def offset(value):
	if -2.5<value<2.5:
		return 0
	elif -7.5<value<-2.5:
		return -10
	elif value < -7.5:
		return -20
	elif 2.5 <value< 7.5:
		return 10
	else:
		return 20
def callback(mobileye_detection):
	img = np.zeros((1000, 600, 3), np.uint8)
	img = cv2.line(img, (150,0),(150,1000),(255,255,255),2,8)
	img = cv2.line(img, (250,0),(250,1000),(255,255,255),2,8)
	img = cv2.line(img, (350,0),(350,1000),(255,255,255),2,8)
	img = cv2.line(img, (450,0),(450,1000),(255,255,255),2,8)
	img = cv2.line(img, (150, 800), (450, 800), (200, 200, 200), 2, 8)
	for i in range(10):
		if i == 7:
			img = cv2.line(img, (150, 1000 - 100 * i), (450, 1000 - 100 * i), (50, 50, 0), 2, 8)
		else:
			img = cv2.line(img, (150,1000-100*i),(450,1000-100*i),(50,50,0),1,8)

#	img = cv2.line(img, (450,0),(450,1000),(255,255,255),1,8)
	img = cv2.rectangle(img, (290, 780), (310, 820), blue, -1) #center position = 300, 700
	if mobileye_detection.o_id[0] is not 0:
		img = cv2.rectangle(img, (int(290 - offset(mobileye_detection.o_position_y[0])*10), int(760 - mobileye_detection.o_position_x[0]*10)), (int(310 - offset(mobileye_detection.o_position_y[0])*10), int(800 -mobileye_detection.o_position_x[0]*10)), red, -1)
	if mobileye_detection.o_id[1] is not 0:
		img = cv2.rectangle(img, (int(290 - offset(mobileye_detection.o_position_y[1])*10), int(760 - mobileye_detection.o_position_x[1]*10)), (int(310 - offset(mobileye_detection.o_position_y[1])*10), int(800 -mobileye_detection.o_position_x[1]*10)), red, -1)
	if mobileye_detection.o_id[2] is not 0:
		img = cv2.rectangle(img, (int(290 - offset(mobileye_detection.o_position_y[2])*10), int(760 - mobileye_detection.o_position_x[2]*10)), (int(310 - offset(mobileye_detection.o_position_y[2])*10), int(800 -mobileye_detection.o_position_x[2]*10)), red, -1)
	if mobileye_detection.o_id[3] is not 0:
		img = cv2.rectangle(img, (int(290 - offset(mobileye_detection.o_position_y[3])*10), int(760 - mobileye_detection.o_position_x[3]*10)), (int(310 - offset(mobileye_detection.o_position_y[3])*10), int(800 -mobileye_detection.o_position_x[3]*10)), red, -1)
	if mobileye_detection.o_id[4] is not 0:
		img = cv2.rectangle(img, (int(290 - offset(mobileye_detection.o_position_y[4])*10), int(760 - mobileye_detection.o_position_x[4]*10)), (int(310 - offset(mobileye_detection.o_position_y[4])*10), int(800 -mobileye_detection.o_position_x[4]*10)), red, -1)
#	img = cv2.rectangle(img, (250, 650), (350, 750), blue, 3)
#	img = cv2.rectangle(img, (250, 650), (350, 750), blue, 3)
#
	cv2.imshow('rec', img)
#	time.sleep(0.1)
	cv2.waitKey(1)
	print(mobileye_detection.msg_count)
#cv2.destroyAllWindows()
while not rospy.is_shutdown():
	rospy.init_node('vis')
	rospy.Subscriber('mobileye_detection', Mobileye_det, callback)
	rospy.spin()

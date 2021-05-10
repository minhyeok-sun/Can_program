#!/usr/bin/env python
import can
import time
from kaai_can.msg import can_std
import rospy


rospy.init_node('mobileye_listner')
can_pub = rospy.Publisher('msg_m', can_std, queue_size=20)

msg = can_std()


bus = can.interface.Bus(bustype='kvaser', channel='0', bitrate=500000)


i = 0


while not rospy.is_shutdown():
    time.sleep(0.0001)
    recv = bus.recv(0.001)


    if (recv is not None) and (recv.is_error_frame == 0):
        msg.id = recv.arbitration_id
        msg.len = recv.dlc
        msg.status = 1
        msg.count = i
        msg.data = recv.data
        can_pub.publish(msg)
        print(msg)
        i += 1


    elif (recv is not None) and (recv.is_error_frame == 1):
        print("can msg frame is error")


    elif recv is None:
        print("There is no can msg")

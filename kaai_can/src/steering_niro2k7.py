#!/usr/bin/env python
import rospy
import can
import time
from kaai_can.msg import Niro

''' decord and send msg / subscriber callback '''
def callback(niro_can):

        ''' decorder (Niro to K7) '''
        ''' refer to "20160422_kookminuniv_K7_v.2.xlsx" '''
	value = - (niro_can.N_Steering_Angle * 10)
	if value < 0:
		angle = int(0xffff + value)
		str_angle0 = angle & 0x00ff
		str_angle1 = (angle & 0xff00) / 256
	else:
		angle = int(value)
		str_angle0 = angle & 0x00ff
		str_angle1 = (angle & 0xff00) / 256

        ''' send msg to K7 '''
	for i in range(20, 70):
                ''' no change in streeing velocity '''
		input_msg = can.Message(arbitration_id=0x700, data=[1, str_angle0, str_angle1, 0, 0, 0, 0, i], is_extended_id=False)
		bus.send(input_msg)


if __name__ == "__main__":
        ''' create bus, node '''
	bus = can.interface.Bus(bustype='kvaser', channel='0', bitrate=500000)
	rospy.init_node('simulate_can', anonymous=True)
        ''' subscribe '''
	sub = rospy.Subscriber('niro_can', Niro, callback)
	rospy.spin()


#!/usr/bin/env python
import rospy
import can
import time
import sys
import threading
from kaai_can.msg import can_std
from kaai_can.msg import Mobileye_det

''' refer to Mobileye.xlsx '''
''' if msg_m.id is 0x669 '''
def func_0x669(msg):

    ''' decorder '''
    value = (msg.data[2]*16 + (msg.data[1]&0xF0)/16)
    if value & 0x800 == 0x800:
        data_mobileye_test.distance_left_lane = (~(value^0xfff) + 1) * 0.02
    else:
        data_mobileye_test.distance_left_lane = value * 0.02
    value = (msg.data[7]*16 + (msg.data[6]&0xF0)/16)
    if value & 0x800 == 0x800:
        data_mobileye_test.distance_right_lane = (~(value^0xfff) + 1) * 0.02
    else:
        data_mobileye_test.distance_right_lane = value * 0.02

''' if msg_m.id is 0x739*3i (i = the number of obstacles - 1)'''
def func_detect(msg):

    ''' choose the overlapping element for the new msg '''
    num = (msg.id - 0x739) / 3
    if msg.data[0] in data_mobileye_test.o_id:
        del_num = data_mobileye_test.o_id.index(msg.data[0])
        data_mobileye_test.o_id[del_num] = 0
        data_mobileye_test.o_position_x[del_num] = 0
        data_mobileye_test.o_position_y[del_num] = 0
        data_mobileye_test.o_relative_velocity_x[del_num] = 0
        data_mobileye_test.o_brake_light[del_num] = 0
        data_mobileye_test.o_type[del_num] = 0
        data_mobileye_test.o_status[del_num] = 0
        data_mobileye_test.o_change[del_num] = 0

    ''' decorder '''
    data_mobileye_test.o_id[num] = msg.data[0]
    data_mobileye_test.o_position_x[num] = ((msg.data[2] & 0x0f) * (16 ** 2) + msg.data[1]) * 0.0625
    value = (msg.data[4] & 0x03) * (16 ** 2) + msg.data[3]
    if value & 0x200 == 0x200:
        data_mobileye_test.o_position_y[num] = (~(value ^ 0x3ff) + 1) * 0.0625
    else:
        data_mobileye_test.o_position_y[num] = value * 0.0625
    value = (msg.data[6] & 0x0f) * (16 ** 2) + msg.data[5]
    if value & 0x800 == 0x800:
        data_mobileye_test.o_relative_velocity_x[num] = (~(value ^ 0xfff) + 1) * 0.0625
    else:
        data_mobileye_test.o_relative_velocity_x[num] = value * 0.0625
    data_mobileye_test.o_brake_light[num] = (msg.data[7] & 0x08) / 8
    data_mobileye_test.o_type[num] = (msg.data[6] & 0x70) / 16
    data_mobileye_test.o_status[num] = (msg.data[7] & 0x07)
    data_mobileye_test.o_change[num] = 0


def callback(msg):

    ''' if the o_change is 800, reset the data '''
    ''' o_change = the count of passing msg '''
    if 800 in data_mobileye_test.o_change:
        del_num = data_mobileye_test.o_change.index(800)
        data_mobileye_test.o_id[del_num] = 0
        data_mobileye_test.o_position_x[del_num] = 0
        data_mobileye_test.o_position_y[del_num] = 0
        data_mobileye_test.o_relative_velocity_x[del_num] = 0
        data_mobileye_test.o_brake_light[del_num] = 0
        data_mobileye_test.o_type[del_num] = 0
        data_mobileye_test.o_status[del_num] = 0
        data_mobileye_test.o_change[del_num] = 0

    ''' 0 <= the number of obstacles <= 5 '''
    func = {
        0x669 : func_0x669,        # about driver's car
        0x739 : func_detect,       # about surrounding cars
        0x73C : func_detect,
        0x73F : func_detect,
        0x742 : func_detect,
        0x745 : func_detect,
    }

    data_mobileye_test.msg_count = msg.count

    ''' if msg.id in func, act the func_XXX '''
    if msg.id in func:
        func[msg.id](msg)

    ''' the o_change keep going to increase '''
    data_mobileye_test.o_change = [(data_mobileye_test.o_change[i] + 1) for i in range(5)]

''' the function for subthread (publish the data / 10Hz) '''
def pub():
    while not rospy.is_shutdown():
            pubcan.publish(data_mobileye_test)
            data_mobileye_test.mobileye_can_message_test_number += 1
            time.sleep(0.1)


#mobileye_status = rospy.get_param("/mobileye_status")
mobileye_status = 1
if mobileye_status == 1:
    data_mobileye_test = Mobileye_det()
    print('\033[95m'+"mobileye_detection node is running"+'\033[0m')

    ''' create node '''
    rospy.init_node('mobileye_can_converter_test', anonymous=True)
    sub = rospy.Subscriber('msg_m', can_std, callback)
    pubcan = rospy.Publisher('mobileye_detection', Mobileye_det, queue_size=20)

    ''' subthread '''
    my_thread = threading.Thread(target=pub())

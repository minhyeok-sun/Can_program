#!/usr/bin/env python
import rospy
import can
import time
import sys
import threading
from kaai_can.msg import can_std
from kaai_can.msg import Mobileye

'''
function of specific can_ID
Refer to mobileye.xlss

'''
def func_0x669(msg_m):
    data_mobileye.Con_Left = msg_m.data[0] & 0x03
    data_mobileye.LDW_Left = (msg_m.data[0] & 0x04)/4
    data_mobileye.Type_Left = (msg_m.data[0] & 0xF0) / 16
    float_Temp = msg_m.data[2]*(16**2) + (msg_m.data[1] & 0xF0)
    if float_Temp & 0x0800 == 0x0800: #value1 $ value2 means extracting bits for progress
        data_mobileye.Dis_Left = -((0x0FFF - float_Temp + 0X01) * 0.02);
    else:
        data_mobileye.Dis_Left = float_Temp * 0.02
    data_mobileye.Con_Right = msg_m.data[5] & 0x03
    data_mobileye.LDW_Right = (msg_m.data[5] & 0x04)/4
    data_mobileye.Type_Left = (msg_m.data[5] & 0xF0) / 16
    float_Temp = msg_m.data[7] * (16**2) + (msg_m.data[6] & 0xF0)
    if float_Temp & 0x0800 == 0x0800:
        data_mobileye.Dis_Right = -((0x0FFF - float_Temp + 0X01) * 0.02);
    else:
        data_mobileye.Dis_Right = float_Temp * 0.02;


def func_0x700(msg_m):
    data_mobileye.Head_Valid = msg_m.data[2]
    data_mobileye.Head_Mea = (msg_m.data[2] & 0xFE)/10
    data_mobileye.LDW_OFF = msg_m.data[4] & 0x01
    data_mobileye.LDW_Left_On = (msg_m.data[4] & 0x02) / 2
    data_mobileye.LDW_Right_On = (msg_m.data[4] & 0x04) / 4
    data_mobileye.FCW_On = (msg_m.data[4] & 0x08) / 8
    data_mobileye.Left_Crossing_Event = (msg_m.data[4] & 0x16) / 16  #adding message
    data_mobileye.Right_Crossing_Event = (msg_m.data[4] & 0x32) / 32 #adding message
    data_mobileye.P_FCW = (msg_m.data[5] & 0x02) / 2
    data_mobileye.P_DZ = (msg_m.data[5] & 0x04) / 4
    data_mobileye.TSR_En = (msg_m.data[5] & 0x80) / 128
    data_mobileye.TSR_W_Lv = msg_m.data[6] & 0x07
    data_mobileye.Head_W_Lv = msg_m.data[7] & 0x03
    data_mobileye.HW_R_En = (msg_m.data[7] & 0x04) / 4


def func_0x727(msg_m):
    data_mobileye.Sign1 = msg_m.data[0]
    data_mobileye.Sign2 = msg_m.data[2]
    data_mobileye.Sign3 = msg_m.data[4]
    data_mobileye.Sign4 = msg_m.data[6]
    data_mobileye.S_Sign1 = msg_m.data[1]
    data_mobileye.S_Sign2 = msg_m.data[3]
    data_mobileye.S_Sign3 = msg_m.data[5]
    data_mobileye.S_Sign4 = msg_m.data[7]

def func_0x728(msg_m):
    data_mobileye.HLB_dec = msg_m.data[0] & 0x03
    data_mobileye.L_Beam = (msg_m.data[2] & 0x01) * (16**2) + msg_m.data[1]

def func_0x737(msg_m):
    float_Temp = msg_m.data[1]*(16**2) + msg_m.data[0]
    if (float_Temp & 0x8000) == 0x8000:
        data_mobileye.L_Cur = -((0xFFFF - float_Temp + 0X0001) * 3.81 * (10**(-6)))
    else:
        data_mobileye.L_Cur = float_Temp * 3.81 * (10**(-6))
    float_Temp = msg_m.data[3]*(16**2) + msg_m.data[2]
    if (float_Temp & 0x0800) == 0x0800:
        data_mobileye.L_Head = -((0x0FFF - float_Temp + 0X0001) * 0.0005)
    else:
        data_mobileye.L_Head = float_Temp * 0.0005
    data_mobileye.Con_Area = (msg_m.data[3] & 0x10) / 16
    data_mobileye.R_LDW = (msg_m.data[3] & 0x20) / 32
    data_mobileye.L_LDW = (msg_m.data[3] & 0x40) / 64
    float_Temp = msg_m.data[5]*(16**2) + msg_m.data[4]
    if (float_Temp < 0x7FFF):
        data_mobileye.Yaw = -(0X7FFF - float_Temp) / 1024 / 512
    else:
        data_mobileye.Yaw = (float_Temp - 0X7FFF) / 1024 / 512
    float_Temp = msg_m.data[7]*(16**2) + msg_m.data[6]
    if (float_Temp < 0x7FFF):
        data_mobileye.Pitch = -(0X7FFF - float_Temp) / 1024 / 512
    else:
        data_mobileye.Pitch = (float_Temp - 0X7FFF) / 1024 / 512


def func_0x760(msg_m):
    data_mobileye.L_Signal = (msg_m.data[0] & 0x02) / 2
    data_mobileye.R_Signal = (msg_m.data[0] & 0x04) / 4
    data_mobileye.Wiper = (msg_m.data[0] & 0x08) / 8
    data_mobileye.Lo_Beam = (msg_m.data[0] & 0x10) / 16
    data_mobileye.Hi_Beam = (msg_m.data[0] & 0x20) / 32
    data_mobileye.Speed = msg_m.data[2]


def func_0x720_0x726(msg_m):
    data_mobileye.Sign_Type = msg_m.data[0]
    data_mobileye.S_Sign_Type = msg_m.data[1]
    data_mobileye.Sign_X = msg_m.data[2]
    float_Temp = msg_m.data[3] & 0x7F
    if float_Temp & 0x40 == 0x40:
        data_mobileye.Sign_Y = -(0x7F - float_Temp + 0x01)
    else:
        data_mobileye.Sign_Y = float_Temp
    float_Temp = msg_m.data[4] & 0x3F
    if float_Temp & 0x20 == 0x20:
        data_mobileye.Sign_Z = -(0x3F - float_Temp + 0x01)
    else:
        data_mobileye.Sign_Z = float_Temp
    data_mobileye.Filter_Type = msg_m.data[5]


'''callback function to progress data subscribed. If there is any ID in func_dictionary, appropriate function is going to run'''
def callback(msg_m):
    func = {
        int("669", 16): func_0x669,
        int("700", 16): func_0x700,
        int("727", 16): func_0x727,
        int("728", 16): func_0x728,
        int("737", 16): func_0x737,
        int("760", 16): func_0x760,
        int("720", 16): func_0x720_0x726,
    }
    data_mobileye.msg_count = msg_m.count
    print('\033[95m'+"#############################################")
    print("              c_data_mobileye                " + '\033[0m')
    print(msg_m)
    if msg_m.id in func:
        func[msg_m.id](msg_m)
'''Function for publish. Use threading to match exact frequency'''
def pub():
    while not rospy.is_shutdown():
        data_mobileye.mobileye_can_message_number += 1
        pubcan.publish(data_mobileye)
        time.sleep(0.05) #20Hz

#mobileye_status = rospy.get_param("/mobileye_status")
mobileye_status = 1
if mobileye_status == 1:
    data_mobileye = Mobileye()
    rospy.init_node('mobileye_can_converter', anonymous=True)
    sub = rospy.Subscriber('msg_m', can_std, callback)
    pubcan = rospy.Publisher('mobileye_can', Mobileye, queue_size=20)
    my_thread = threading.Thread(target=pub())



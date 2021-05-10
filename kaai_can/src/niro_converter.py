#!/usr/bin/env python
import rospy
import can
import time
import sys
import threading
from kaai_can.msg import can_std
from kaai_can.msg import Niro

'''
function of specific can_ID
Refer to mobileye.xlss

'''
def func_0x541(msg_n):
    w = msg_n.data[2]
    if w == 0x40:
        data_niro.Driver_Door_switch = 0
    elif w == 0x41:
        data_niro.Driver_Door_switch = 1
    w = msg_n.data[4]
    if w == 0x00:
        data_niro.Passenger_Door_switch = 0
    elif w == 0x08:
        data_niro.Passenger_Door_switch = 1
    w = msg_n.data[1] & 0x0F
    if w == 0x04:
        data_niro.Driver_Seat_Belt = 1
    elif w == 0x00:
        data_niro.Driver_Seat_Belt = 0
    w = msg_n.data[1] & 0xF0
    if w == 0x40:
        data_niro.Assistant_Seat_Belt = 1
    elif w == 0x00:
        data_niro.Assistant_Seat_Belt = 0
    data_niro.Rear_Wiper_Speed = msg_n.data[2] / 16 / 2
    w = msg_n.data[5]
    if w == 0x04:
        data_niro.Left_Turn_Indicator = 1
    elif w == 0x00:
        data_niro.Left_Turn_Indicator = 0
    if w == 0x02:
        data_niro.Right_Turn_Indicator = 1
    elif w == 0x00:
        data_niro.Right_Turn_Indicator = 0
    if w == 0x01:
        data_niro.Fog_Light = 1
    elif w == 0x00:
        data_niro.Fog_Light = 0
    w = msg_n.data[2]
    if w == 0x29:
        data_niro.Left_Turn_Indicator_out_sign = 1
    elif w == 0x21:
        data_niro.Left_Turn_Indicator_out_sign = 0
    if w == 0x40:
        data_niro.Right_Turn_Indicator_out_sign = 1
    elif w == 0x00:
        data_niro.Right_Turn_Indicator_out_sign = 0
    if w == 0x69:
        data_niro.Emergency_Light_out_sign = 1
    else:
        data_niro.Emergency_Light_out_sign = 0
    w = msg_n.data[4]
    if w == 0x04:
        data_niro.Tail_Light = 1
    elif w == 0x00:
        data_niro.Tail_Light = 0
    if w == 0x80:
        data_niro.Head_Light = 1
    elif w == 0x00:
        data_niro.Head_Light = 0
    if (msg_n.data[4] & 0x01) == 0x01:
        data_niro.Up_Light = 1
    elif (msg_n.data[4] & 0x02) == 0x02:
        data_niro.Emergency_Light = 1
    else:
        data_niro.Up_Light = 0
        data_niro.Emergency_Light = 0
    if w == 0xc0:
        data_niro.Auto_Light = 1
    elif w == 0x00:
        data_niro.Auto_Light = 0
    w = msg_n.data[3]
    if w == 0x80:
        data_niro.Light_Status_out_sign = 1
    elif w == 0x00:
        data_niro.Light_Status_out_sign = 0
def func_0x553(msg_n):
    w = msg_n.data[3]
    if w == 0x03:
        data_niro.Rear_left_door_switch = 0
    elif w == 0x02:
        data_niro.Rear_left_door_switch = 1
    w = msg_n.data[2]
    if w == 0x11:
        data_niro.Rear_right_door_switch = 0
    elif w == 0x91:
        data_niro.Rear_right_door_switch = 1
    w = msg_n.data[4]
    if w == 0x00:
        data_niro.Wiper_Operation = 1
    elif w == 0x01:
        data_niro.Wiper_Operation = 0
def func_0x559(msg_n):
    w = msg_n.data[1]
    if w == 0x40:
        data_niro.Door_Lock = 1
    elif w == 0x00:
        data_niro.Door_Lock = 0
    data_niro.Wiper_Speed = msg_n.data[2] / 4
    data_niro.Rear_Wiper_Operation = msg_n.data[4] / 16 / 4
def func_0x340(msg_n):
    w=msg_n.data[6] & 0x0F
    if w == 0x0B:
        data_niro.LDWS_Switch = 1
    elif w == 0x07:
        data_niro.LDWS_Switch = 0
    w=msg_n.data[1] & 0x0F
    if w == 0x08:
        data_niro.LDWS_Left_Warning = 1
    elif w == 0x00:
        data_niro.LDWS_Left_Warning = 0
    w=msg_n.data[1] & 0xF0
    if w == 0x20:
        data_niro.LDWS_Right_Warning = 1
    elif w == 0x00:
        data_niro.LDWS_Right_Warning = 0
def func_0x394(msg_n):
    if (msg_n.data[7] == 0x93) and ((msg_n.data[5] & 0xF0) == 0xc0):
        data_niro.Brake_Switch = 1
    elif (msg_n.data[7] == 0x83) and (msg_n.data[5] == 0x84):
        data_niro.Brake_Switch = 0
    w=msg_n.data[7] & 0xF0
    if w == 0x10:
        data_niro.Parking_Brake = 1
    else:
        data_niro.Parking_Brake = 0
def func_0x372(msg_n):
    data_niro.Gear_Position = msg_n.data[2]
def func_0x371(msg_n):
    data_niro.RPM = float(msg_n.data[3] * 256 + msg_n.data[2]) / 4
    data_niro.Brake_Pedal_Pressure = msg_n.data[0]
    data_niro.Throttle_Position = msg_n.data[7] * 0.392157
    data_niro.N_Speed1 = msg_n.data[4]
    data_niro.Startup_key_state = msg_n.data[2]
def func_0x381(msg_n):
    data_niro.Eco_switch = msg_n.data[7]
def func_0x58B(msg_n):
    data_niro.Rear_Side_Warning = msg_n.data[0] & 0x0F
    data_niro.Rear_Camera = (msg_n.data[0] & 0x20) / 32
    w=msg_n.data[1]
    if w == 0x00:
        data_niro.L_SPAS_Warning = 0
    elif w == 0x01:
        data_niro.L_SPAS_Warning = 1
    elif w == 0x02:
        data_niro.L_SPAS_Warning = 2
    w=msg_n.data[2]
    if w == 0x04:
        data_niro.R_SPAS_Warning = 0
    elif w == 0x05:
        data_niro.R_SPAS_Warning = 1
    elif w == 0x16:
        data_niro.R_SPAS_Warning = 2
def func_0x2B0(msg_n):
    N_Steering_Angle =  msg_n.data[1]*(16**2) + msg_n.data[0]
    CAN_DATA_INT_temp = (N_Steering_Angle & 0xffffffff) & 0x8000
    if CAN_DATA_INT_temp == 0x8000:
        data_niro.N_Steering_Angle = (0xFFFF - N_Steering_Angle + 1) / 10
    else:
        data_niro.N_Steering_Angle = -(N_Steering_Angle / 10)
    data_niro.N_Steering_Angle_velocity = 4 * msg_n.data[2]
def func_0x52A(msg_n):
    data_niro.N_Speed2 = msg_n.data[0]
def func_0x130(msg_n):
    data_niro.Lateral_Acceleration = msg_n.data[5]
def func_0x5C4(msg_n):
    w=msg_n.data[0]
    data_niro.Air_Conditioner_Operation_Driver = w / 2 + 14
    if w == 0x00:
        data_niro.Air_Conditioner_Operation_Driver = 0
    w=msg_n.data[2]
    data_niro.Air_Conditioner_Operation_Assistant = w / 2 + 14
    if w == 0x00:
        data_niro.Air_Conditioner_Operation_Assistant = 0
def func_0x436(msg_n):
    if (msg_n.data[0] == 0x40) and (msg_n.data[1] == 0x08) and (msg_n.data[2] == 0x00) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 0
    elif (msg_n.data[0] == 0x80) and (msg_n.data[1] == 0x10) and (msg_n.data[2] == 0x00) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 1
    elif (msg_n.data[0] == 0xC0) and (msg_n.data[1] == 0x18) and (msg_n.data[2] == 0x10) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 2
    elif (msg_n.data[0] == 0x80) and (msg_n.data[1] == 0x00) and (msg_n.data[2] == 0x02) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 11
    elif (msg_n.data[0] == 0xC0) and (msg_n.data[1] == 0x00) and (msg_n.data[2] == 0x03) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 12
    elif (msg_n.data[0] == 0x80) and (msg_n.data[1] == 0x00) and (msg_n.data[2] == 0x10) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 21
    elif (msg_n.data[0] == 0xC0) and (msg_n.data[1] == 0x00) and (msg_n.data[2] == 0x18) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 22
    elif (msg_n.data[0] == 0x00) and (msg_n.data[1] == 0x41) and (msg_n.data[2] == 0x00) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 100
    elif (msg_n.data[0] == 0x00) and (msg_n.data[1] == 0x82) and (msg_n.data[2] == 0x00) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 101
    elif (msg_n.data[0] == 0x00) and (msg_n.data[1] == 0xC3) and (msg_n.data[2] == 0x00) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 102
    elif (msg_n.data[0] == 0x02) and (msg_n.data[1] == 0x80) and (msg_n.data[2] == 0x00) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 111
    elif (msg_n.data[0] == 0x03) and (msg_n.data[1] == 0xC0) and (msg_n.data[2] == 0x00) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 112
    elif (msg_n.data[0] == 0x10) and (msg_n.data[1] == 0x80) and (msg_n.data[2] == 0x00) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 121
    elif (msg_n.data[0] == 0x18) and (msg_n.data[1] == 0xC0) and (msg_n.data[2] == 0x00) and (msg_n.data[3] == 0x09):
        data_niro.Parking_Assistance_System = 122

'''callback function to progress data subscribed. If there is any ID in func_dictionary, appropriate function is going to run'''
def callback(msg_n):
    func = {
        int("130", 16): func_0x130,
        int("2B0", 16): func_0x2B0,
        int("340", 16): func_0x340,
        int("371", 16): func_0x371,
        int("372", 16): func_0x372,
        int("381", 16): func_0x381,
        int("394", 16): func_0x394,
        int("436", 16): func_0x436,
        int("52A", 16): func_0x52A,
        int("541", 16): func_0x541,
        int("553", 16): func_0x553,
        int("559", 16): func_0x559,
        int("58B", 16): func_0x58B,
        int("5C4", 16): func_0x5C4
    }
    data_niro.msg_count = msg_n.count
    print('\033[96m'+"#############################################")
    print("              c_data_niro                " + '\033[0m')
    print(msg_n)
    if msg_n.id in func:
        func[msg_n.id](msg_n)

'''Function for publish. Use threading to match exact frequency'''
def pub():
    while not rospy.is_shutdown():
        data_niro.niro_can_message_number += 1
        pubcan.publish(data_niro)
        time.sleep(0.05)#20Hz

niro_status = 1
#niro_status = rospy.get_param("/niro_status")
if niro_status == 1:
    data_niro = Niro()
    rospy.init_node('niro_can_converter', anonymous=True)
    sub = rospy.Subscriber('msg_m', can_std, callback)
    pubcan = rospy.Publisher('niro_can', Niro, queue_size=20)
    my_thread = threading.Thread(target=pub())


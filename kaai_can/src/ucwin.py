#!/usr/bin/env python
import rospy
import socket
import threading
import can
import time
from niro_test.msg import can_std
trans = can_std()
HOST = '210.123.37.182'
PORT = 8888
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def callback(msg_k):
    if msg_k.id == 0x710:
        trans.data = msg_n.data
        a = msg_n.data[1]
        b = msg_n.data[2]
        data = (b*256 + a)
        if data < 1000:
            angle = data/10
        else:
            data = data^0b1111111111111111
            angle = ~data/10
       
        if angle > 23:
            data_to_send = 65
            trans.id = data_to_send
        elif angle < -23:
            data_to_send = 68
            trans.id = data_to_send
        else:
            data_to_send = 0
            trans.id = data_to_send
        print(msg_n.data)
        print(angle)

def pub():
    while not rospy.is_shutdown():
        send = str(trans.id)        
        client_socket.sendall(send.encode())
#        print(trans.data)
#        print(send)
        time.sleep(0.1)

rospy.init_node('ucwin', anonymous=True)
sub = rospy.Subscriber('msg_k', can_std, callback)

my_thread = threading.Thread(target=pub())

client_socket.close()
rospy.spin()

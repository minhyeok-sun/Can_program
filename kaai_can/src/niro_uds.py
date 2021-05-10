import can

# decorder list...

def VehicleSpeed_1(x):
    print('vehicle speed1')
    return x[0]

def VehicleSpeed_2(x):
    print('vehicle speed2')
    return x[0] * 1.250196

def AccleatorPosition_(x):
    print('accelator position')
    return x[0] * 0.392157

def DriverSettingTargetSpeed_(x):
    print('driver setting target speed')
    return x[0], 16

def DistanceToTarget_(x):
    print('distance to target')
    return x[0] * 0.588236

def RelativeSpeedToTarget_(x):
    print('relative speed to target')
    return x[0] - 170

def AbsoluteSteeringAngle_(x):
    print('absolute steering angle')
    PH = x[0] * 256 + x[1] * 0.1
    if PH > int("7FFF", 16):
        return PH - int("FFFF", 16)
    return PH

def SteeringWheelAngleSensor_(x):
    print('steering wheel angle sensor')
    PH = x[0] * 256 + x[1] * 0.1
    if PH > int("7FFF", 16):
        return PH - int("FFFF", 16)
    return PH

def OBD_speed_(x):
    print('obd_speed')
    return x[0]

def OBD_RPM_(x):
    print('obd_rpm')
    return (256 * x[0] + x[1])/4


# Command definition

class Command:

    def __init__(self, request_id, service_mode, DID1, DID2):
        self.request_id = request_id
        self.DID1 = int(DID1, 16)
        self.DID2 = int(DID2, 16)
        self.service_mode = int(service_mode, 16)
        self.data_list = []

    def send_message(self):
        # Single frame data
            msg = can.Message(arbitration_id=self.request_id, data=[3, self.service_mode, self.DID1, self.DID2, 0, 0, 0, 0], is_extended_id=False)
            print(msg)
            bus.send(msg)
            response = bus.recv(timeout=2)
            print(response)

            if response is None:
                print ('\033[31m' + "Error : There is no response" + '\033[0m')
            else:
                index = response.data[0]

        # Single frame (error or OBD)
                if index != 16:
                    if response.data[1] == int('7F', 16):  # 7f = 126 => negative code
                        print('\033[31m')
                        print("first frame error. error code : ", response.data[3])
                        print('\033[0m')
                    else:
                        if response.data[0] == 0:   # Maybe OBD data
                            print('\033[31m' + "Fatal error. First frame unknown error. Error response : " + '\033[0m')
                        elif response.data[1] <= int('49', 16):
                            for i in range(3, response.data[0] + 1):
                                print("OBD protocol")
                                self.data_list.append(response.data[i])
                        else:
                            for i in range(4, response.data[0] + 1):
                                print("UDS protocol - single frame")
                                self.data_list.append(response.data[i])


        # First frame
                else:
                    for i in range(3):
                        self.data_list.append(response.data[i + 5])
                    data_block = response.data[1]

        # Flow control frame
                    msg = can.Message(arbitration_id=self.request_id, data=[int("30", 16), 0, 2, 0, 0, 0, 0, 0], is_extended_id=False)
                    print(msg)
                    bus.send(msg)

        # Consecutive frame
                    j = 6  # j is the number of data_list's element(+3)
                    while j < data_block:
                        response = bus.recv(timeout=1)
                        print(response)
                        if response != None:
                            for i in range(7):
                                self.data_list.append(response.data[i + 1])
                                j = j + 1

    def get_data(self):
        return self.data_list



class CommandList:

    def __init__(self):
        self.commands = []
        self.decorders = []     # decorders = [[decorder, byte_add, byte_ind], ....]
        self.top = 0

    def input_command(self, request_id, service_mode, DID1, DID2, decorder):
        self.commands.append(Command(request_id, service_mode, DID1, DID2))
        self.decorders.append(decorder)
        self.top += 1

    def decorder(self, i):
        if self.decorders[i] == None:
            return None
        else:
            callback = self.decorders[i][0]
            byte_add = self.decorders[i][1]
            byte_ind = self.decorders[i][2]
            x = []
            for j in range(byte_ind):
                x.append(self.commands[i].data_list[byte_add - 1 + j])
            return callback(x)


    def refresh_command(self):
        for i in range(self.top):
            self.commands[i].data_list = []
            self.commands[i].send_message()
            print(self.commands[i].get_data())
            print(self.decorder(i))
            print('======================================================================================================================')



bus = can.interface.Bus(bustype='kvaser', channel='0', bitrate=500000)

UDSdata = CommandList()

''' ex) UDSdata.input_command(request_id, service_mode, DID1, DID2, decorder = [decorder, byte_add, byte_int]) '''

'''OBD data'''
#UDSdata.input_command(0x7E0, '01', '0C', '00', [OBD_RPM_, 1, 2])
#UDSdata.input_command(0x7E1, '01', '0D', '00', [OBD_speed_, 1, 1])
#UDSdata.input_command(0x7E1, '09', '02', '00', None)

'''UDS data'''
UDSdata.input_command(0x7E1, '22', '01', 'A4', [VehicleSpeed_1, 7, 1])
UDSdata.input_command(0x7E0, '22', 'E0', '02', [VehicleSpeed_2, 13, 1])
#UDSdata.input_command(0x7E1, '22', '01', 'A4', [AccleatorPosition_, 9, 1])
#UDSdata.input_command(0x7D0, '22', '02', '01', [DriverSettingTargetSpeed_, 1, 1])
#UDSdata.input_command(0x7D0, '22', '02', '03', [DistanceToTarget_, 1, 1])
#UDSdata.input_command(0x7D0, '22', '02', '20', [RelativeSpeedToTarget_, 1, 1])
UDSdata.input_command(0x7D4, '22', '01', '01', [AbsoluteSteeringAngle_, 4, 2])
UDSdata.input_command(0x7C4, '22', 'F0', '10', [SteeringWheelAngleSensor_, 7, 2])
UDSdata.refresh_command()

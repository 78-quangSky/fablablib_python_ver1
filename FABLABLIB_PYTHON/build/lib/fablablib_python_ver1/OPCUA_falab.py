"""This code is used to read data from PLC Siemens S7-1200 through OPC UA protocol."""
import time
import datetime
import os
import sys
from opcua import Client, ua


class OPCUA:
    def __init__(
        self,
        ip_addr=None,
        port=None,
        type_of_OS="raspberry"  # "raspberry" or "laptop"
    ):
        self.ip_addr = ip_addr
        self.port = port
        self.type_of_OS = type_of_OS

    def init(self):
        timeout_connect = 0
        while True:
            if self.type_of_OS == "laptop":
                res = os.system("ping -n 1 " + str(self.ip_addr) + " > nul")
            elif self.type_of_OS == "raspberry":
                res = os.system("ping -c 1 " + str(self.ip_addr) + " > /dev/null 2>&1")

            time.sleep(1)
            if res == 0:
                print("Connected to the ip.")
                break
            else:
                print("No opcua connection.")
                if timeout_connect == 10:
                    timeout_connect = 0
                timeout_connect += 1
                print(timeout_connect)

        # Connect to OPC UA
        url = "opc.tcp://" + str(self.ip_addr) + ":" + str(self.port)
        self.uaclient = Client(url)
        self.uaclient.connect()
        print("ua client connected")

    def ua_getnodedata(self, ua_nodeid):
        ua = self.uaclient.get_node(str(ua_nodeid))
        ua_value = ua.get_value()
        ua_name = ua.get_display_name().Text
        # ua_name = ua.nodeid.__dict__["Identifier"]
        return (str(ua_name), ua_value)


class OPCUA_S7_1200_ThaiDuong(OPCUA):
    def __init__(
        self,
        ip_addr="192.168.0.1",
        port=4840,
        type_of_OS="raspberry"  # "raspberry" or "laptop"
    ):
        # IP address of PLC S7-1200 HAITAIN at Thai Duong
        # self.ip_addr = "192.168.2.130"
        # self.port = "16664"
        super().__init__(ip_addr, port, type_of_OS)

    def ua_getnodedata(self, ua_nodeid, type_of_plc="old"):
        ua = self.uaclient.get_node(str(ua_nodeid))
        ua_value = ua.get_value()

        # The way to get name of variable based on the specific type of plc
        if type_of_plc == "old":
            ua_name = ua.get_display_name().Text
        elif type_of_plc == "new":
            ua_name = ua.nodeid.__dict__["Identifier"]

        ua_name = self.config_name_before_publish(ua_name)
        return (str(ua_name), ua_value)

    def config_name_before_publish(self, data_name):
        if data_name == "tmTemp1_Current":
            data_name = "Nozzle Temp"
        elif data_name == "tmInjMaxPress":
            data_name = "Injection Peak Pressure"
        elif data_name == "tmInjSpeed1":
            data_name = "Peak Injection Speed"
        elif data_name == "tmTurnPosi":
            data_name = "Switch Over Pos"
        elif data_name == "tmCycleTime":
            data_name = "injectionTime"
        elif data_name == "tmShotCount":
            data_name = "counterShot"
        return data_name

    def reset_program_SIEMENS(self, nodeID_reset=None):
        if nodeID_reset == None:
            return False
        else:
            var_node = self.uaclient.get_node(str(nodeID_reset))
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
            time.sleep(0.1)
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))
            print("Reset SIEMENS successfully")
            return True

    def restart_python_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def shift_detect(number_of_shift=2):
        if number_of_shift == 3:
            first_shift_start = datetime.time(6,0,0,0)
            second_shift_start = datetime.time(14,0,0,0)
            third_shift_start = datetime.time(22,0,0,0)
            time_of_current_shift = datetime.datetime.now().time()
            if ((time_of_current_shift > first_shift_start) and (time_of_current_shift < second_shift_start)):
                return 1
            elif ((time_of_current_shift > second_shift_start) and (time_of_current_shift < third_shift_start)):
                return 2
            else:
                return 3
        elif number_of_shift == 2:
            first_shift_start = datetime.time(6,0,0,0)
            second_shift_start = datetime.time(18,0,0,0)
            time_of_current_shift = datetime.datetime.now().time()
            if ((time_of_current_shift > first_shift_start) and (time_of_current_shift < second_shift_start)):
                return 1
            else:
                return 2


class OPCUA_S7_1200_VTSauto(OPCUA_S7_1200_ThaiDuong):
    def __init__(self, ip_addr="192.168.1.1", port=4840, type_of_OS="raspberry"):
        super().__init__(ip_addr, port, type_of_OS)

    def write_data(self, ua_nodeid, data_name, data_value):
        var_node = self.uaclient.get_node(ua_nodeid)
        if data_name == "setpoint":
            var_node.set_value(ua.DataValue(ua.Variant(data_value, ua.VariantType.UInt16)))
        elif data_name == "startup":
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
            time.sleep(0.1)
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))
        elif data_name == "forward":
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
            time.sleep(0.1)
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))
        elif data_name == "reverse":
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
            time.sleep(0.1)
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))
        elif data_name == "stop":
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
            time.sleep(0.1)
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))
        else:
            var_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(data_value))

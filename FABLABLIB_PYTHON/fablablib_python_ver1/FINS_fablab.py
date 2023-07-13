import sys
import os
import time
import datetime
import fins.udp
from .convert_time_fablab import convertTime_fablab
from .RS485_fablab import RS485_heatController


class customed_variable_name:
    THAIDUONG_INTERNAL_VAR_NAME_LIST = [
    'CURING TIMER - No.1_2nd - Setup_value', 'CURING TIMER - No.2_2nd - Setup_value', 
    'MACHINE RUNNING TIMER - Setup_value', 'DAY OUTPUT - No.1 - Setup_value', 
    'DAY OUTPUT - No.2 - Setup_value', 'MAIN CYLINDER PRESSURE - No.1- Setup_value', 
    'MAIN CYLINDER PRESSURE - No.2- Setup_value', 'CURING TIMER - No.1_2nd - Real_value', 
    'CURING TIMER - No.2_2nd - Real_value', 'MACHINE RUNNING TIMER - Real_value',
    'DAY OUTPUT - No.1 - Real_value', 'DAY OUTPUT - No.2 - Real_value', 
    'MAIN CYLINDER PRESSURE - No.1- Real_value', 'MAIN CYLINDER PRESSURE - No.2- Real_value', 
    'UPPER MOLD TEMP ALARM - No.1', 'MAIN MOTOR OVER LOAD - No.1', 
    'LIFTING OVER & STOP - No.1', 'CENTER MOLD TEMP ALARM - No.1',
    'LOWER MOLD TEMP ALARM - No.1', 'UPPER MOLD TEMP ALARM - No.2', 
    'MAIN MOTOR OVER LOAD - No.2', 'LIFTING OVER & STOP - No.2', 
    'CENTER MOLD TEMP ALARM - No.2', 'LOWER MOLD TEMP ALARM - No.2', 
    'PLC CPU BATTERY LOW', 'Front Mold out Locating - No.1', 
    'Front Mold out Low speed - No.1', 'Back Mold out Low speed - No.1', 
    'Back Mold out Locating - No.1', 'Front Mold out Low speed - No.2', 
    'Front Mold out Locating - No.2', 'Back Mold out Low speed - No.2', 
    'Back Mold out Locating - No.2', 'CURING TIMER - No.1_1st - Real_value', 
    'CURING TIMER - No.2_1st - Real_value', 'CURING TIMER - No.1_1st - Setup_value', 'CURING TIMER - No.2_1st - Setup_value'
    ]

    THAIDUONG_INTERNAL_VAR_ADDR_LIST = [
    b'\x00\x3b\x00',  b'\x00\x45\x00',  b'\x00\x2c\x00',  b'\x02\x59\x00',  b'\x02\x5b\x00',  b'\x01\xf8\x00',  b'\x02\x0c\x00',
    b'\x08\x09\x00',  b'\x08\x13\x00',  b'\x00\x2a\x00',  b'\x08\x29\x00',  b'\x08\x2b\x00',  b'\x01\xf4\x00',  b'\x02\x08\x00',  
    b'\x00\x03\x0d',  b'\x00\x02\x0f',  b'\x00\x03\x0a',  b'\x00\x03\x0e',  b'\x00\x03\x0f',  b'\x00\x07\x0d',  b'\x00\x06\x0f', 
    b'\x00\x07\x0a',  b'\x00\x07\x0e',  b'\x00\x07\x0f',  b'\x0c\x92\x04',  b'\x00\x01\x06',  b'\x00\x02\x04',  b'\x00\x02\x0a',  
    b'\x00\x01\x0e',  b'\x00\x06\x04',  b'\x00\x05\x06',  b'\x00\x06\x0a',  b'\x00\x05\x0e',  b'\x08\x07\x00',  b'\x08\x11\x00',
    b'\x00\x39\x00',  b'\x00\x43\x00'   
    ]

    THAIDUONG_INTERNAL_VAR_NAME_LEFT_MACHINE_LIST = [
    'CURING TIMER - No.1_2nd - Setup_value', 'MACHINE RUNNING TIMER - Setup_value', 
    'DAY OUTPUT - No.1 - Setup_value', 'MAIN CYLINDER PRESSURE - No.1- Setup_value', 
    'CURING TIMER - No.1_2nd - Real_value', 'MACHINE RUNNING TIMER - Real_value',
    'DAY OUTPUT - No.1 - Real_value', 'MAIN CYLINDER PRESSURE - No.1- Real_value', 
    'UPPER MOLD TEMP ALARM - No.1', 'MAIN MOTOR OVER LOAD - No.1', 
    'LIFTING OVER & STOP - No.1', 'CENTER MOLD TEMP ALARM - No.1',
    'LOWER MOLD TEMP ALARM - No.1', 'PLC CPU BATTERY LOW', 
    'Front Mold out Locating - No.1', 'Front Mold out Low speed - No.1', 
    'Back Mold out Low speed - No.1', 'Back Mold out Locating - No.1', 
    'CURING TIMER - No.1_1st - Real_value', 'CURING TIMER - No.1_1st - Setup_value'
    ]

    THAIDUONG_INTERNAL_VAR_NAME_RIGHT_MACHINE_LIST = [
    'CURING TIMER - No.2_2nd - Setup_value', 'DAY OUTPUT - No.2 - Setup_value', 
    'MAIN CYLINDER PRESSURE - No.2- Setup_value', 'CURING TIMER - No.2_2nd - Real_value', 
    'DAY OUTPUT - No.2 - Real_value', 'MAIN CYLINDER PRESSURE - No.2- Real_value', 
    'UPPER MOLD TEMP ALARM - No.2', 'MAIN MOTOR OVER LOAD - No.2', 
    'LIFTING OVER & STOP - No.2', 'CENTER MOLD TEMP ALARM - No.2', 
    'LOWER MOLD TEMP ALARM - No.2', 'Front Mold out Low speed - No.2', 
    'Front Mold out Locating - No.2', 'Back Mold out Low speed - No.2', 
    'Back Mold out Locating - No.2', 'CURING TIMER - No.2_1st - Real_value', 'CURING TIMER - No.2_1st - Setup_value'
    ]


class FINS_ETHERNET:
    def __init__(
        self,
        ip_addr="192.168.250.1", # IP real: "192.168.0.11"
        dest_node_add=1,    # Node IP on OMRON
        srce_node_add=11,   # Node IP on laptop/raspberry
        EN_use_external_var_name_list=False,
        var_name_list=None,
        var_addr_list=None,
        var_name_left_machine_list=None,
        var_name_right_machine_list=None,
        type_of_OS="raspberry"  # "raspberry" or "laptop"
    ):
        self.ip_addr = ip_addr
        self.dest_node_add = dest_node_add
        self.srce_node_add = srce_node_add
        self.type_of_OS = type_of_OS
        self.EN_use_external_var_name_list = EN_use_external_var_name_list

        if EN_use_external_var_name_list:
            if (var_name_list is None or var_addr_list is None or var_name_left_machine_list is None or var_name_right_machine_list is None):
                raise Exception("Please add enough parameters if EN_use_internal_var_name_list is True")
            else:
                self.var_name_list = var_name_list
                self.var_addr_list = var_addr_list
                self.var_name_left_machine_list = var_name_left_machine_list
                self.var_name_right_machine_list = var_name_right_machine_list
        else:
            self.var_name_list = customed_variable_name.THAIDUONG_INTERNAL_VAR_NAME_LIST
            self.var_addr_list = customed_variable_name.THAIDUONG_INTERNAL_VAR_ADDR_LIST
            self.var_name_left_machine_list = customed_variable_name.THAIDUONG_INTERNAL_VAR_NAME_LEFT_MACHINE_LIST
            self.var_name_right_machine_list = customed_variable_name.THAIDUONG_INTERNAL_VAR_NAME_RIGHT_MACHINE_LIST

        self.var_dictionary = dict(zip(self.var_addr_list, self.var_name_list))

    def init(self):
        timeout_connect = 0
        while True:
            if self.type_of_OS == "laptop":
                res = os.system("ping -n 1 " + str(self.ip_addr) + " > nul")
            elif self.type_of_OS == "raspberry":
                res = os.system("ping -c 1 " + str(self.ip_addr) + " > /dev/null 2>&1")

            time.sleep(1)
            if res == 0:
                print("Connected to the FINS ETHERNET/IP")
                break
            else:
                print("No FINS ETHERNET/IP connection")
                if timeout_connect == 10:
                    timeout_connect = 0
                timeout_connect += 1
                print(timeout_connect)

        # Connect to FINS IP/ETHERNET
        self.fins_instance = fins.udp.UDPFinsConnection()
        self.fins_instance.connect(self.ip_addr)
        self.fins_instance.dest_node_add = self.dest_node_add
        self.fins_instance.srce_node_add = self.srce_node_add

    def fins_getData(self, data_type="DATA_MEMORY_WORD", data_addr=None):
        try:
            if (data_type == "DATA_MEMORY_WORD"):
                mem_area = self.fins_instance.memory_area_read(b'\x82',data_addr)
                fins_data_value = self.bcd_decode(mem_area[-2:],1)
                fins_data_name = self.config_var_name(self.var_dictionary[data_addr])
                machine_ID = self.config_deviecID(self.var_dictionary[data_addr])

            elif (data_type == "TIMER_WORD" or data_type == "COUNTER_WORD"):
                mem_area = self.fins_instance.memory_area_read(b'\x81',data_addr)
                fins_data_value = self.bcd_decode(mem_area[-2:],1)
                fins_data_name = self.config_var_name(self.var_dictionary[data_addr])
                machine_ID = self.config_deviecID(self.var_dictionary[data_addr])

            elif (data_type == "CIO_BIT"):
                mem_area = self.fins_instance.memory_area_read(b'\x00',data_addr)
                fins_data_value = self.bcd_decode(mem_area[-1:],0)
                fins_data_name = self.config_var_name(self.var_dictionary[data_addr])
                machine_ID = self.config_deviecID(self.var_dictionary[data_addr])

            return(fins_data_name, fins_data_value, machine_ID)
        except Exception as e:
            print("ERROR:", e)


class OMRON_FINS_IPEthernet_ThaiDuong(FINS_ETHERNET):
    def __init__(
        self,
        ip_addr="192.168.250.1", # IP real: "192.168.0.11"
        dest_node_add=1,    # Node IP on OMRON
        srce_node_add=11,   # Node IP on laptop/raspberry
        EN_use_external_var_name_list=False,
        var_name_list=None,
        var_addr_list=None,
        var_name_left_machine_list=None,
        var_name_right_machine_list=None,
        EN_use_UART=False,
        port_UART=None,
        type_of_OS="raspberry"  # "raspberry" or "laptop"
    ):
        super().__init__(
            ip_addr,dest_node_add,srce_node_add,EN_use_external_var_name_list,var_name_list,var_addr_list,var_name_left_machine_list,var_name_right_machine_list,type_of_OS
        )
        self.EN_use_UART = EN_use_UART
        self.port = port_UART

        if EN_use_UART:
            self.uart_rs485 = RS485_heatController(port=port_UART, type_of_OS=type_of_OS)

        self.shotCount = [0]*4
        self.injectionCycle_ls = [0]*4
        self.injectionTime_ls = [0]*4
        self.deviceID_ls = ["right"]*4
        self.init_get_cycleTime = True

    def read_temperature_value(self, type_value="PV", device_id=1):
        self.uart_rs485.read_temperature_value(type_value, device_id)

    def detect_heatController_isActive(self, ID_heatcontroller_list):
        self.uart_rs485.detect_heatController_isActive(ID_heatcontroller_list)

    def bcd_decode(self, data: bytes, decimals: int):
        res = 0
        for n, b in enumerate(reversed(data)):
            res += (b & 0x0F) * 10 ** (n * 2 - decimals)
            res += (b >> 4) * 10 ** (n * 2 + 1 - decimals)
        return res
    
    def fins_getData(self, data_type="Number", data_addr=None):
        try:
            if (data_type == "Number" or data_type == "Temperature"):
                mem_area = self.fins_instance.memory_area_read(b'\x82',data_addr)
                fins_data_value = self.bcd_decode(mem_area[-2:],1)
                fins_data_name = self.config_var_name(self.var_dictionary[data_addr])
                machine_ID = self.config_deviecID(self.var_dictionary[data_addr])

            elif (data_type == "Timer"):
                mem_area = self.fins_instance.memory_area_read(b'\x81',data_addr)
                fins_data_value = self.bcd_decode(mem_area[-2:],1)
                fins_data_name = self.config_var_name(self.var_dictionary[data_addr])
                machine_ID = self.config_deviecID(self.var_dictionary[data_addr])

            elif (data_type == "Bool"):
                mem_area = self.fins_instance.memory_area_read(b'\x00',data_addr)
                fins_data_value = self.bcd_decode(mem_area[-1:],0)
                fins_data_name = self.config_var_name(self.var_dictionary[data_addr])
                machine_ID = self.config_deviecID(self.var_dictionary[data_addr])

            return(fins_data_name, fins_data_value, machine_ID)
        except Exception as e:
            print("ERROR:", e)
    
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
    
    def resetProgramOMRON(self, bytes_addr_reset):
        try:
            self.fins_instance.memory_area_write(b'\x80', bytes_addr_reset, b'\x00\x1f', 1)
            time.sleep(0.1)
            self.fins_instance.memory_area_write(b'\x80', bytes_addr_reset, b'\x00\x00', 1)
            print("Reset OMRON successfully")
        except Exception as e:
            print(e)

    def restart_python_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
    
    def config_var_name(self, var_name):
        if var_name == 'Front Mold No.1 curingTime' or var_name == 'Front Mold No.2 curingTime':
            var_name = 'injectionTime'
        elif var_name == 'Front Mold No.1 CycleTime' or var_name == 'Front Mold No.2 CycleTime':
            var_name = 'injectionCycle'
        elif var_name == 'Front Mold No.1 shotCount' or var_name == 'Front Mold No.2 shotCount':
            var_name = 'counterShot'
        elif var_name == 'heatController-2-PV' or var_name == 'heatController-5-PV':
            var_name = 'temperature'
        elif var_name == 'MAIN CYLINDER PRESSURE - No.1- Real_value' or var_name == 'MAIN CYLINDER PRESSURE - No.2- Real_value':
            var_name = 'pressure'
        elif var_name == 'MAIN CYLINDER PRESSURE - No.1- Setup_value' or var_name == 'MAIN CYLINDER PRESSURE - No.2- Setup_value':
            var_name = 'pressure_SP'
        elif var_name == 'badProduct-1':
            var_name = 'badProduct-1'
        elif var_name == 'badProduct-2':
            var_name = 'badProduct-2'
        return var_name

    def config_deviecID(self, deviecID):
        if deviecID == 'Front Mold No.1 curingTime' or deviecID == 'Back Mold No.1 curingTime':
            deviecID = 1
        elif deviecID == 'Front Mold No.2 curingTime' or deviecID == 'Back Mold No.2 curingTime':
            deviecID = 2
        elif deviecID == 'Front Mold No.1 CycleTime' or deviecID == 'Back Mold No.1 CycleTime':
            deviecID = 1
        elif deviecID == 'Front Mold No.2 CycleTime' or deviecID == 'Back Mold No.2 CycleTime':
            deviecID = 2
        elif deviecID == 'Front Mold No.1 shotCount' or deviecID == 'Back Mold No.1 shotCount':
            deviecID = 1
        elif deviecID == 'Front Mold No.2 shotCount' or deviecID == 'Back Mold No.2 shotCount':
            deviecID = 2
        elif deviecID == 'heatController-1-PV' or deviecID == 'heatController-2-PV' or deviecID == 'heatController-3-PV':
            deviecID = 1
        elif deviecID == 'heatController-4-PV' or deviecID == 'heatController-5-PV' or deviecID == 'heatController-6-PV':
            deviecID = 2
        elif deviecID == 'heatController-1-SP' or deviecID == 'heatController-2-SP' or deviecID == 'heatController-3-SP':
            deviecID = 1
        elif deviecID == 'heatController-4-SP' or deviecID == 'heatController-5-SP' or deviecID == 'heatController-6-SP':
            deviecID = 2
        elif deviecID == 'MAIN CYLINDER PRESSURE - No.1- Real_value':
            deviecID = 1
        elif deviecID == 'MAIN CYLINDER PRESSURE - No.2- Real_value':
            deviecID = 2
        elif deviecID == 1 or deviecID == 2:
            deviecID = 1
        elif deviecID == 3 or deviecID == 4:
            deviecID = 2
        # elif (deviecID in INTERNAL_VAR_NAME_LEFT_MACHINE_LIST) == True:
        #     deviecID = 1
        # elif (deviecID in INTERNAL_VAR_NAME_RIGHT_MACHINE_LIST) == True:
        #     deviecID = 2
        if(deviecID==1):
            return 'left'
        elif(deviecID==2):
            return 'right'
        else:
            return 'right'
        
    def get_cycleTime(self, signal_addr, timer_addr, machine_pos="front_left"):
        # machine_pos = "front_left" || "back_left" || "front_right" || "back_right"
        #                   (1)             (2)             (3)             (4)
        if (self.init_get_cycleTime):
            match machine_pos:
                case "front_left":
                    self._machine_pos = 1
                case "back_left":
                    self._machine_pos = 2
                case "front_right":
                    self._machine_pos = 3
                case "back_right":
                    self._machine_pos = 4

            sign_name,self.prev_sign, self.deviceID_ls[self._machine_pos] = self.fins_getData("Bool", signal_addr)
            print(sign_name, ":", self.prev_sign)
            _,self.injectionTime,_ = self.fins_getData("Number", timer_addr)
            self.old_time = datetime.datetime.now().time()
            self.injectionTime_ls[self._machine_pos] = self.injectionTime
            self.time_limit = 5
            self.init_get_cycleTime = False
        try:
            sign_name,new_sign,_ = self.fins_getData("Bool", signal_addr)
            if new_sign != self.prev_sign:
                print(self.prev_sign, new_sign)
                print(sign_name, ":", new_sign)

                if self.prev_sign == 1 and new_sign == 0  :
                    new_time = datetime.datetime.now().time()
                    delta_time = convertTime_fablab.convert_time_to_milliseconds(new_time) - convertTime_fablab.convert_time_to_milliseconds(self.old_time)
                    print(delta_time, self.injectionTime)
                    if (delta_time < self.time_limit*1000):
                        return
                    if (delta_time - self.injectionTime*1000) > self.injectionTime*1000:
                            delta_time = self.injectionTime*1000*(1 + 0.35)
                    self.injectionCycle_ls[self._machine_pos] = delta_time/1000 # Khi dung voi SparkPlug
                    # self.injectionCycle_ls[self._machine_pos] = convertTime_fablab.convert_miliseconds_to_timeOfDay(abs(delta_time))
                    self.shotCount[self._machine_pos] += 1

                    self.old_time = new_time
                self.prev_sign = new_sign   
        except Exception as e: 
            print('Failed to get cycleTime!')
            print(e)
            time.sleep(1)

    def return_cycleTime_infor(self, _machine_pos="front_left"):
        match _machine_pos:
            case "front_left":
                machine_pos = 1
            case "back_left":
                machine_pos = 2
            case "front_right":
                machine_pos = 3
            case "back_right":
                machine_pos = 4
        
        cycleTime_infor = (self.deviceID_ls[machine_pos], 
                           self.injectionCycle_ls[machine_pos], 
                           self.injectionTime_ls[machine_pos], 
                           self.shotCount[machine_pos]
                        )

        return cycleTime_infor
    
    # Nếu giá trị timer bên trái, phải đều là None thì đưa nó vào vòng lặp đến khi khác None thì thôi 
    # Hoặc là cho một khoảng timeout nhất định. Qua khoảng thời gian đó thì xác nhận không có máy nào
    # đang ép        
    def update_curingTime(self, left_curingTime_addr_list, right_curingTime_addr_list):
        old_left_value = []
        old_right_value = []
        left_timer_addr_Active = None
        right_timer_addr_Active = None

        try:
            for timer_addr in left_curingTime_addr_list:
                _,timer_value,_ = self.fins_getData("Timer", timer_addr)
                old_left_value.append(timer_value)
            
            for timer_addr in right_curingTime_addr_list:
                _,timer_value,_ = self.fins_getData("Timer", timer_addr)
                old_right_value.append(timer_value)

            for data_bytes in left_curingTime_addr_list:
                new_left_value = self.fins_getData("Timer", data_bytes)
                if old_left_value[left_curingTime_addr_list.index(data_bytes)] != new_left_value:
                    left_timer_addr_Active = new_left_value
                    break

            for data_bytes in left_curingTime_addr_list:
                new_right_value = self.fins_getData("Timer", data_bytes)
                if old_right_value[right_curingTime_addr_list.index(data_bytes)] != new_right_value:
                    right_timer_addr_Active = new_right_value
                    break
        except Exception as e:
            print(e)
            return None, None

        return left_timer_addr_Active, right_timer_addr_Active
                
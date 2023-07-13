import threading
import time
from fablablib_python_ver1 import *

TYPE_OF_OS = "laptop"

lock = threading.Lock()
log = LOG_DATA(project="ThaiDuong_OMRON", type_of_OS=TYPE_OF_OS)

injectionTime_addr = b'\x00\x07\x00'
signal_addr = b'\x00\x05\x06'
bitReset = b'\x00\x00\x00'

#------------------ Name variable list ref --------------------
name_var_ref_list = [
'CURING TIMER - No.1_2nd - Setup_value', 'CURING TIMER - No.2_2nd - Setup_value', 'MACHINE RUNNING TIMER - Setup_value', 'DAY OUTPUT - No.1 - Setup_value', 'DAY OUTPUT - No.2 - Setup_value', 'MAIN CYLINDER PRESSURE - No.1- Setup_value', 'MAIN CYLINDER PRESSURE - No.2- Setup_value', 'CURING TIMER - No.1_2nd - Real_value', 'CURING TIMER - No.2_2nd - Real_value', 'MACHINE RUNNING TIMER - Real_value',
'DAY OUTPUT - No.1 - Real_value', 'DAY OUTPUT - No.2 - Real_value', 'MAIN CYLINDER PRESSURE - No.1- Real_value', 'MAIN CYLINDER PRESSURE - No.2- Real_value', 'UPPER MOLD TEMP ALARM - No.1', 'MAIN MOTOR OVER LOAD - No.1', 'LIFTING OVER & STOP - No.1', 'CENTER MOLD TEMP ALARM - No.1',
'LOWER MOLD TEMP ALARM - No.1', 'UPPER MOLD TEMP ALARM - No.2', 'MAIN MOTOR OVER LOAD - No.2', 'LIFTING OVER & STOP - No.2', 'CENTER MOLD TEMP ALARM - No.2', 'LOWER MOLD TEMP ALARM - No.2', 'PLC CPU BATTERY LOW', 'Front Mold out Locating - No.1', 'Front Mold out Low speed - No.1', 'Back Mold out Low speed - No.1', 'Back Mold out Locating - No.1', 
'Front Mold out Low speed - No.2', 'Front Mold out Locating - No.2', 'Back Mold out Low speed - No.2', 'Back Mold out Locating - No.2', 'CURING TIMER - No.1_1st - Real_value', 'CURING TIMER - No.2_1st - Real_value', 'CURING TIMER - No.1_1st - Setup_value', 'CURING TIMER - No.2_1st - Setup_value', 'temperature_SP', 'temperature', 'heatController-6-SP', 'heatController-6-PV', "injectionTime"
]

address_var_ref_list = [
b'\x00\x3b\x00',  b'\x00\x45\x00',  b'\x00\x2c\x00',  b'\x02\x59\x00',  b'\x02\x5b\x00',  b'\x01\xf8\x00',  b'\x02\x0c\x00',
b'\x08\x09\x00',  b'\x08\x13\x00',  b'\x00\x2a\x00',  b'\x08\x29\x00',  b'\x08\x2b\x00',  b'\x01\xf4\x00',  b'\x02\x08\x00',  
b'\x00\x03\x0d',  b'\x00\x02\x0f',  b'\x00\x03\x0a',  b'\x00\x03\x0e',  b'\x00\x03\x0f',  b'\x00\x07\x0d',  b'\x00\x06\x0f', 
b'\x00\x07\x0a',  b'\x00\x07\x0e',  b'\x00\x07\x0f',  b'\x0c\x92\x04',  b'\x00\x01\x06',  b'\x00\x02\x04',  b'\x00\x02\x0a',  
b'\x00\x01\x0e',  b'\x00\x06\x04',  b'\x00\x05\x06',  b'\x00\x06\x0a',  b'\x00\x05\x0e',  b'\x08\x07\x00',  b'\x08\x11\x00',
b'\x00\x39\x00',  b'\x00\x43\x00',  b'\x01\x90\x00',  b'\x02\x58\x00', b'\x01\xB8\x00', b'\x02\x1C\x00', b'\x00\x07\x00']

name_var_left_machine = [
'CURING TIMER - No.1_2nd - Setup_value', 'MACHINE RUNNING TIMER - Setup_value', 'DAY OUTPUT - No.1 - Setup_value', 'MAIN CYLINDER PRESSURE - No.1- Setup_value', 'CURING TIMER - No.1_2nd - Real_value', 'MACHINE RUNNING TIMER - Real_value',
'DAY OUTPUT - No.1 - Real_value', 'MAIN CYLINDER PRESSURE - No.1- Real_value', 'UPPER MOLD TEMP ALARM - No.1', 'MAIN MOTOR OVER LOAD - No.1', 'LIFTING OVER & STOP - No.1', 'CENTER MOLD TEMP ALARM - No.1',
'LOWER MOLD TEMP ALARM - No.1', 'PLC CPU BATTERY LOW', 'Front Mold out Locating - No.1', 'Front Mold out Low speed - No.1', 'Back Mold out Low speed - No.1', 'Back Mold out Locating - No.1', 
'CURING TIMER - No.1_1st - Real_value', 'CURING TIMER - No.1_1st - Setup_value'
]
name_var_right_machine = [
'CURING TIMER - No.2_2nd - Setup_value', 'DAY OUTPUT - No.2 - Setup_value', 'MAIN CYLINDER PRESSURE - No.2- Setup_value', 'CURING TIMER - No.2_2nd - Real_value', 
'DAY OUTPUT - No.2 - Real_value', 'MAIN CYLINDER PRESSURE - No.2- Real_value', 'UPPER MOLD TEMP ALARM - No.2', 'MAIN MOTOR OVER LOAD - No.2', 'LIFTING OVER & STOP - No.2', 'CENTER MOLD TEMP ALARM - No.2', 
'LOWER MOLD TEMP ALARM - No.2', 'Front Mold out Low speed - No.2', 'Front Mold out Locating - No.2', 'Back Mold out Low speed - No.2', 'Back Mold out Locating - No.2', 'CURING TIMER - No.2_1st - Real_value', 'CURING TIMER - No.2_1st - Setup_value',
'temperature_SP', 'temperature', 'heatController-6-SP', 'heatController-6-PV'
]
# Tạo dict gồm key: "address", value: "name of variable"
var_dictionary_ref = dict(zip(address_var_ref_list,name_var_ref_list)) 
#--------------------------------------------------------------------------
Setup_value_list =[
b'\x02\x0c\x00', b'\x01\x90\x00', b'\x01\xB8\x00'
]

Real_value_list = [
b'\x02\x08\x00', b'\x02\x58\x00', b'\x02\x1C\x00'
]

# Set variable name and initial value
old_value_SP = [n*-1 for n in range(len(address_var_ref_list))]
old_value_PV = [n*-1 for n in range(len(address_var_ref_list))]

#------------------------------------------------------------------------------------------------------------------------------
fins_client = OMRON_FINS_IPEthernet_ThaiDuong(
    ip_addr="192.168.250.1",
    EN_use_external_var_name_list=True,
    var_name_list=name_var_ref_list,
    var_addr_list=address_var_ref_list,
    var_name_left_machine_list=name_var_left_machine,
    var_name_right_machine_list=name_var_right_machine,
    type_of_OS=TYPE_OF_OS
)

mqtt_client = MQTT(
    client_id="test OMRON",
    general_topic="OMRON/P011-right/Metric/",
    project="ThaiDuong_OMRON",
    type_of_OS=TYPE_OF_OS
)

fins_client.init()
mqtt_client.init()

#------------------------------------------------------------------------------------------------------------------------------
def task_read_data_plc():
    count_err = 0
    while True:
        try:            
            for data_bytes in Setup_value_list:
                with lock:
                    data_name_SP, data_value_SP, deviceID_SP = fins_client.fins_getData(data_addr = data_bytes)
                    data_name_PV, data_value_PV, deviceID_PV = fins_client.fins_getData(data_addr = Real_value_list[Setup_value_list.index(data_bytes)])
                
                    if (data_value_SP != old_value_SP[Setup_value_list.index(data_bytes)]):
                        mqtt_client.publish_data(data_name_SP, data_value_SP, deviceID_SP)
                        log.common_form_csv(data_name_SP, data_value_SP, deviceID_SP)
                        old_value_SP[Setup_value_list.index(data_bytes)] = data_value_SP

                    if (data_value_PV != old_value_PV[Setup_value_list.index(data_bytes)]):
                        mqtt_client.publish_data(data_name_PV, data_value_PV, deviceID_PV)
                        log.common_form_csv(data_name_PV, data_value_PV, deviceID_PV)
                        old_value_PV[Setup_value_list.index(data_bytes)] = data_value_PV

                count_err = 0
                threading.Event().wait(0.1)
        except Exception as e:
            count_err += 1
            if count_err == 10:
                fins_client.restart_python_program()
            print("Connect to PLC OMRON Failed!")
            print("ERROR:", e)
            threading.Event().wait(1)

def task_count_cycleTime(signal_bytes, injectionTime_bytes, machine_pos):
    while True:
        with lock:
            fins_client.get_cycleTime(signal_bytes, injectionTime_bytes, machine_pos)
        threading.Event().wait(0.5)

time.sleep(1)
if __name__ == '__main__':
    old_injectionCycle = -1 
    old_shotCount = -1

    t1 = threading.Thread(target=task_read_data_plc)
    t2 = threading.Thread(target=task_count_cycleTime, args=(signal_addr, injectionTime_addr, "front_right"))

    t1.start()
    t2.start()
    
    count = 0
    while True:
        # count+=1
        # print(count)
        # if count == 100:
        #     count = 0
        #     fins_client.resetProgramOMRON(bitReset)

        deviceID, injectionCycle, injectionTime, shotCount = fins_client.return_cycleTime_infor("front_right")
        # print(deviceID, injectionCycle, injectionTime, shotCount)
        if old_injectionCycle != injectionCycle and old_shotCount != shotCount:
            with lock:
                mqtt_client.publish_data("shotCount", shotCount, deviceID)
                log.common_form_csv("shotCount", shotCount, deviceID)
                
                mqtt_client.publish_data("injectionCycle", injectionCycle, deviceID)
                log.common_form_csv("injectionCycle", injectionCycle, deviceID)

                mqtt_client.publish_data("injectionTime", injectionTime, deviceID)
                log.common_form_csv("injectionTime", injectionTime, deviceID)

            old_injectionCycle = injectionCycle
            old_shotCount = shotCount
        threading.Event().wait(1)
    t1.join()
    t2.join()

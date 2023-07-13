import threading
import time
from fablablib_python_ver1 import *

TYPE_OF_OS = "laptop"

lock = threading.Lock()
log = LOG_DATA(project="VTSauto", type_of_OS=TYPE_OF_OS)

var_list = [
    'ns=4;i=7', 'ns=4;i=6', 'ns=4;i=8', 'ns=4;i=14', 'ns=4;i=15', 'ns=4;i=16', 'ns=4;i=12', 'ns=4;i=13', 
    'ns=4;i=47', 'ns=4;i=46', 'ns=4;i=48', 'ns=4;i=49', 'ns=4;i=32', 'ns=4;i=33', 'ns=4;i=35', 'ns=4;i=34', 
    'ns=4;i=28', 'ns=4;i=25', 'ns=4;i=26', 'ns=4;i=27', 'ns=4;i=21', 'ns=4;i=22', 'ns=4;i=24', 'ns=4;i=23', 
    'ns=4;i=40', 'ns=4;i=41', 'ns=4;i=42', 'ns=4;i=39'
]
old_value = [n*-1 for n in range(0,len(var_list))]

data_setup_list = ['controlGreen',  'controlDCMotor', 'controlRed', 'controlYellow', 'startup', 'stop', 'forward', 'reverse', 'setpoint']
nodeID_data_setup_list = ['ns=4;i=46', 'ns=4;i=47', 'ns=4;i=48', 'ns=4;i=49', 'ns=4;i=12', 'ns=4;i=13', 'ns=4;i=14', 'ns=4;i=15', 'ns=4;i=16']

#------------------------- Setup MQTT and OPCUA client ----------------------------
ua_client = OPCUA_S7_1200_VTSauto(type_of_OS=TYPE_OF_OS)

mqtt_client = MQTT(
    client_id="test_VTSauto",
    project="VTSauto",
    general_topic="VTSauto/AR_project/IOT_pub/",
    list_subcribe_vts_topic=data_setup_list,
    list_nodeID_vts_topic=nodeID_data_setup_list,
    type_of_OS=TYPE_OF_OS
)
#-----------------------------------------------------------------------------------

ua_client.init()
mqtt_client.init()

#-----------------------------------------------------------------------------------
def task_get_data_from_PLC():
    count_err = 0
    while True:
        try:
            for ua_nodeid in var_list:
                if ua_nodeid in nodeID_data_setup_list:
                    continue
                data_name, data_value = ua_client.ua_getnodedata(ua_nodeid)    

                with lock:
                    if old_value[var_list.index(ua_nodeid)] != data_value:
                        mqtt_client.publish_data(data_name, data_value)
                        log.common_form_csv(data_name, data_value)
                        old_value[var_list.index(ua_nodeid)] = data_value

                count_err = 0    
                threading.Event().wait(0.01)
        except:
            count_err += 1
            if count_err == 10:
                ua_client.restart_python_program()
            print('Getting data from OPCUA UA is failed!')
            threading.Event().wait(1)

def task_write_configuration_to_PLC():
    global flag_list, nodeID_list, data_name_list, data_value_list

    flag_list = mqtt_client.return_flag_signal_list_from_IIOT_write()
    nodeID_list = mqtt_client.return_nodeID_list_with_respective_topic()
    data_name_list = mqtt_client.return_mqtt_name_list_from_IIOT_write()
    data_value_list = mqtt_client.return_mqtt_value_list_from_IIOT_write()

    print(flag_list)
    print(nodeID_list)
    print(data_name_list)
    print(data_value_list)

    while True:
        try:
            for flag_signal in flag_list:
                if flag_signal == 1:
                    data_nodeID = nodeID_list[flag_list.index(flag_signal)]
                    data_name = data_name_list[flag_list.index(flag_signal)]
                    data_value = data_value_list[flag_list.index(flag_signal)]

                    with lock:
                        ua_client.write_data(data_nodeID, data_name, data_value)

                    mqtt_client.return_flag_signal_list_from_IIOT_write(index_flag=flag_list.index(flag_signal))
                
                threading.Event().wait(0.1)
        except Exception as e:
            print(e)
            threading.Event().wait(1)


time.sleep(1)
if __name__ == "__main__":
    t2 = threading.Thread(target=task_get_data_from_PLC)
    t3 = threading.Thread(target=task_write_configuration_to_PLC)

    for ua_nodeid in var_list:
        data_name, data_value = ua_client.ua_getnodedata(ua_nodeid)
        mqtt_client.publish_data(data_name, data_value)
        log.common_form_csv(data_name, data_value)
        time.sleep(0.05)

    t2.start()
    t3.start()

    count = 0
    while True:
        count += 1
        time.sleep(1)
        if count == 10:
            count = 0
            print(flag_list)
            print(nodeID_list)
            print(data_name_list)
            print(data_value_list)

    t2.join()
    t3.join()
import threading
from fablablib_python_ver1 import *

TYPE_OF_OS = "laptop"

# --------------------- User variable --------------------------------------
lock = threading.Lock() # Called in thread to block the rest of threads
log = LOG_DATA(project="ThaiDuong_SIEMENS", type_of_OS=TYPE_OF_OS)

var_list = ["ns=4;i=9", "ns=4;i=10", "ns=4;i=8", "ns=4;i=15", "ns=4;i=7", "ns=4;i=16", "ns=4;i=14", "ns=4;i=12", "ns=4;i=11", "ns=4;i=13"]
old_value = [n * -1 for n in range(len(var_list))]

shotCount_var = "ns=4;i=12"
injTime_var = "ns=4;i=7"
bit_reset = "ns=4;i=17"

# Time of injection
injectionTime = 0
injectionCycle = 0

prev_sign = 0
# ---------------------------------------------------------------------------

uaclient = OPCUA_S7_1200_ThaiDuong(type_of_OS=TYPE_OF_OS)
mqttclient = MQTT(
    client_id="demo_raspi_HAITHIEN", 
    general_topic="HAITHIEN/I1/Metric/", 
    type_of_OS=TYPE_OF_OS
)

uaclient.init()
mqttclient.init()

# ------------------------------- MultiTasks ---------------------------------
def get_cycleTime(signal_id, injTime_id, name_cycleTime="injectionCycle"):
    global injectionTime, injectionCycle, prev_sign
    try:
        with lock:
            _, new_sign = uaclient.ua_getnodedata(signal_id)
            if (prev_sign != new_sign):  # Lúc này lấy thời điểm thay đổi giá trị của biến counterShot để làm mốc tính chu kỳ ép
                _, injTime_value = uaclient.ua_getnodedata(injTime_id)
                injectionCycle = injTime_value
                mqttclient.publish_data(name_cycleTime, injectionCycle)
                log.common_form_csv(name_cycleTime, injectionCycle)
            prev_sign = new_sign
        threading.Event().wait(0.01)

    except Exception as e:
        print(e)
        print("Failed to get cycleTime!")
        threading.Event().wait(0.5)

def task_get_PLC_data():
    global injectionTime
    count_err = 0
    while True:
        try:
            for ua_nodeid in var_list:
                get_cycleTime(shotCount_var, injTime_var)
                with lock:
                    data_name, data_value = uaclient.ua_getnodedata(ua_nodeid)
                    if old_value[var_list.index(ua_nodeid)] != data_value:
                        mqttclient.publish_data(data_name, data_value)
                        log.common_form_csv(data_name, data_value)
                        old_value[var_list.index(ua_nodeid)] = data_value
                        count_err = 0
                threading.Event().wait(0.01)

        except Exception as e:
            count_err += 1
            if count_err == 10:
                uaclient.restart_python_program()
            print(e)
            print("Getting data from OPCUA UA is failed!")
            threading.Event().wait(1)

# ----------------------------------------------------------------------------

# ----------------------------- Main code ------------------------------------
if __name__ == "__main__":
    t1 = threading.Thread(target=task_get_PLC_data)
    t1.start()
    t1.join()
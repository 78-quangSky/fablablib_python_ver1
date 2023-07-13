import time
from .json_payload_fablab import json_payload 
import paho.mqtt.client as mqtt
import json
import os

ID_MAY_EP_DO_CHOI_LEFT = [
"P001-left", "P002-left", "P003-left", "P004-left", "P005-left", "P006-left", 
"P007-left", "P008-left", "P009-left", "P010-left", "P011-left"
]

ID_MAY_EP_DO_CHOI_RIGHT = [
"P001-right", "P002-right", "P003-right", "P004-right", "P005-right", 
"P006-right", "P007-right", "P008-right", "P009-right", "P010-right", "P011-right"
]


class MQTT:
    def __init__(
        self,
        mqtt_broker="20.214.136.1",
        mqtt_port=1883,
        mqtt_KeepAliveINTERVAL=45,
        client_id="sample_id",
        username="user",
        password="password",
        general_topic="HAITHIEN/I1/Metric/",
        project="ThaiDuong_SIEMENS", # "ThaiDuong_SIEMENS" or "ThaiDuong_OMRON" or "VTSauto"
        list_subcribe_vts_topic=None,
        list_nodeID_vts_topic=None,
        file_csv_path="store_messages.txt",
        type_of_OS="raspberry" # "raspberry" or "laptop"
    ):
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_KeepAliveINTERVAL = mqtt_KeepAliveINTERVAL
        self.client_id = client_id
        self.username = username
        self.password = password
        self.general_topic = general_topic
        self.project = project
        self.file_csv_path = file_csv_path
        self.type_of_OS = type_of_OS
        self.list_nodeID_vts_topic = list_nodeID_vts_topic
        self.list_subcribe_vts_topic = list_subcribe_vts_topic

        if (self.list_nodeID_vts_topic is not None) and (self.list_subcribe_vts_topic is not None) and (self.project == "VTSauto"):
            self.temp_flag_list = [False]*len(self.list_subcribe_vts_topic)
            self.temp_mqtt_name_list = ["Null"]*len(self.list_subcribe_vts_topic)
            self.temp_mqtt_value_list = [0]*len(self.list_subcribe_vts_topic)
            self.temp_mqtt_timestamp_list = ["Null"]*len(self.list_subcribe_vts_topic)
            self.temp_nodeID_vts_topic = ["Null"]*len(self.list_subcribe_vts_topic)

        self.comman_from_mqtt = 1
        self.store_message_flag = 0
        self.topic_str = ""
        self.topic_field = None

        # if self.list_subcribe_vts_topic is not None:
        #     self.topic = "VTSauto/AR_project/IOT_pub/"

    def init(self):
        # Initiate Mqtt Client
        self.client = mqtt.Client(self.client_id)

        # if machine is TESTediately turned off --> last_will sends "Status: Off" to topic
        self.client.will_set(self.general_topic + "machineStatus", json_payload.generate_data_status("Off", 5), 1, 1)

        # if the broker requires username and password
        self.client.username_pw_set(self.username, self.password)

        # Register callback function
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        # Connect with MQTT Broker
        print("connecting to broker ", self.mqtt_broker)

        # Check connection to MQTT Broker
        try:
            self.client.connect(self.mqtt_broker, self.mqtt_port, self.mqtt_KeepAliveINTERVAL)
        except:
            print("Can't connect MQTT Broker!")

        self.client.loop_start()
        time.sleep(0.5)

        if self.project == "ThaiDuong_OMRON":
            if "right" in self.general_topic:
                self.publish(self.general_topic + "machineStatus", str(json_payload.generate_data_status("Run", 1)), 1, 1)
                self.publish(self.general_topic.replace("right", "left") + "machineStatus", str(json_payload.generate_data_status("Run", 1)), 1, 1)
            elif "left" in self.general_topic:
                self.publish(self.general_topic + "machineStatus", str(json_payload.generate_data_status("Run", 1)), 1, 1)
                self.publish(self.general_topic.replace("left", "right") + "machineStatus", str(json_payload.generate_data_status("Run", 1)), 1, 1)
        else:
            self.publish(self.general_topic + "machineStatus", str(json_payload.generate_data_status("Run", 1)), 1, 1)

    # Define MQTT call-back function
    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code " + str(rc))
        if self.project == "ThaiDuong_OMRON":
            if "right" in self.general_topic:
                self.publish(self.general_topic + "machineStatus", str(json_payload.generate_data_status("Run", 1)), 1, 1)
                self.publish(self.general_topic.replace("right", "left") + "machineStatus", str(json_payload.generate_data_status("Run", 1)), 1, 1)
            elif "left" in self.general_topic:
                self.publish(self.general_topic + "machineStatus", str(json_payload.generate_data_status("Run", 1)), 1, 1)
                self.publish(self.general_topic.replace("left", "right") + "machineStatus", str(json_payload.generate_data_status("Run", 1)), 1, 1)
        else:
            self.publish(self.general_topic + "machineStatus", str(json_payload.generate_data_status("Run", 1)), 1, 1)
            self.subscribe(self.general_topic.replace("Metric/", "CollectingData"))

        if self.list_subcribe_vts_topic == None:
            return
        else:
            for topic in self.list_subcribe_vts_topic:
                self.subscribe(self.general_topic.replace("IOT_pub", "IIOT_write") + str(topic))
        
        # try:
        #     with open(self.file_csv_path, 'r') as file:
        #         self.messages = file.read().splitlines()
        #         self.store_message_flag = 1
        # except FileNotFoundError:
        #     print("No stored messages to publish")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection from MQTT broker, storing messages...")

    def on_publish(self, client, userdata, mid):
        print("msg pulbished..")

    def on_message(self, client, userdata, msg):
        self.topic_str = str(msg.topic)
        self.topic_field = self.topic_str.split("/")

        if self.project == "ThaiDuong_SIEMENS":
            print('CollectingData ', msg.payload.decode('utf-8'))
            received_data = json.loads(msg.payload.decode('utf-8'))
            self.comman_from_mqtt = received_data['Command']
            if int(self.comman_from_mqtt) == 1 :
                print("Khong co yeu cau --> Hoat dong binh thuong!")
            else:
                print("Yeu cau thay khuon!")

        elif self.project == "ThaiDuong_OMRON":
            pass

        elif self.project == "VTSauto":
            if self.list_subcribe_vts_topic == None:
                return
            else:
                try:
                    received_data = json.loads(msg.payload.decode('utf-8').replace("[","").replace("]",""))
                    mqtt_name = received_data['name']
                    mqtt_value = received_data['value']
                    mqtt_timestamp = received_data['timestamp']

                    if mqtt_name == 'setpoint':
                        mqtt_value = int(mqtt_value)
                    else:
                        if mqtt_value == 'false':
                            mqtt_value = bool(False)
                        elif mqtt_value == 'true':
                            mqtt_value = bool(True)
                            
                except Exception as e:
                    print(e)

                if mqtt_name in self.list_subcribe_vts_topic:
                    self.temp_flag_list[self.list_subcribe_vts_topic.index(mqtt_name)] = True
                    self.temp_mqtt_name_list[self.list_subcribe_vts_topic.index(mqtt_name)] = mqtt_name
                    self.temp_mqtt_value_list[self.list_subcribe_vts_topic.index(mqtt_name)] = mqtt_value
                    self.temp_mqtt_timestamp_list[self.list_subcribe_vts_topic.index(mqtt_name)] = mqtt_timestamp
                    self.temp_nodeID_vts_topic[self.list_subcribe_vts_topic.index(mqtt_name)] = self.list_nodeID_vts_topic[self.list_subcribe_vts_topic.index(mqtt_name)]

    def return_comman_from_mqtt(self):
        return self.comman_from_mqtt
    
    def return_flag_signal_list_from_IIOT_write(self, index_flag=None):
        if index_flag is None:
            return self.temp_flag_list
        else:
            self.temp_flag_list[index_flag] = False
    
    def return_mqtt_name_list_from_IIOT_write(self):
        return self.temp_mqtt_name_list
    
    def return_mqtt_value_list_from_IIOT_write(self):
        return self.temp_mqtt_value_list

    def return_mqtt_timestamp_list_from_IIOT_write(self):
        return self.temp_mqtt_timestamp_list
    
    def return_nodeID_list_with_respective_topic(self):
        return self.temp_nodeID_vts_topic
    
    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        self.client.publish(topic, payload, qos, retain, properties)

    def publish_data(self, data_name, data_value, deviceID="left"):
        data = json_payload.generate_data_publish(data_name, data_value)
        if self.project == "ThaiDuong_OMRON":
            if "right" in self.general_topic:
                mqtt_topic = self.general_topic.replace("right", deviceID) + str(data_name)
            elif "left" in self.general_topic:
                mqtt_topic = self.general_topic.replace("left", deviceID) + str(data_name)
        else:
            mqtt_topic = self.general_topic + str(data_name)
        self.publish(mqtt_topic, data, 1, 1)
        print(data)

    # def publish_stored_data_from_flie_txt(self):
    #     if self.store_message_flag:
    #         for message in self.messages:
    #             print("Write stored_data: ", message)
    #             _message = json.loads(message.replace("\\","").replace("[","").replace("]",""))
    #             data_name = _message['name']
    #             self.publish(self.general_topic + "RESTORE/" + str(data_name), str(message.replace("\\","")), 1, 1)
    #             time.sleep(0.7)

    #         print('Complete publish stored messages!')
    #         self.store_message_flag = 0
    #         # Clear the file
    #         myfile = self.file_csv_path
    #         if os.path.isfile(myfile):
    #             os.remove(myfile)

    def subscribe(self, topic, qos=0, options=None, properties=None):
        self.client.subscribe(topic, qos, options, properties)

    def check_wifi_connection(self):
        if self.type_of_OS == "laptop":
            response = os.system("ping -n 1 google.com > nul")
        elif self.type_of_OS == "raspberry":
            response = os.system("ping -c 1 google.com > /dev/null 2>&1")

        if response == 0:
            return True
        else:
            return False


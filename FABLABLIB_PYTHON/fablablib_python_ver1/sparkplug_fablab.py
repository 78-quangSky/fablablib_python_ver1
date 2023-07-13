import time, random, datetime
import serial
from mqtt_spb_wrapper import *


class SparkPlug_MQTT:
    pass
"""
_DEBUG = True  # Enable debug messages
# listVarPub = ['temperature', 'injectionTime', 'injectionCycle', 'pressure']
# listVarPub = ['Nozzle Temp', 'injectionTime', 'injectionCycle', 'tmClpClsTime', 'tmClpOpnTime', 'tmChargeTime', 'Switch Over Pos', 'test_counterShot']
listVarPub = ['injectionTime', 'injectionCycle']
oldValue = [-0.5]*len(listVarPub)
oldTimestamp = [0]*len(listVarPub)

ser = serial.Serial(
    # port='/dev/serial0',    # module RS485 thường
    # port='/dev/ttyUSB0',    # module RS485 USB
    # port='COM7',
    baudrate=9600,
    timeout=0.050
)

#--------------------------------------------------------------------------------------------------------------------------------------
def callback_command(payload):
    print("DEVICE received CMD: %s" % (payload))


def callback_message(topic, payload):
    temp = str(topic)
    tokens = temp.split("/")
    print(tokens)
    if tokens[0] == "spBv1.0" and (tokens[2] == "NCMD" or tokens[2] == "DCMD" or tokens[2] == "NDATA" or tokens[2] == "DDATA") and tokens[3] == "Node2" and tokens[4] == "M1.2":
        print("Received MESSAGE: %s - %s" % (topic, payload["metrics"]))
        # for field in payload.get('metrics', []):
        #     print(field)
            
def convert_time_to_milliseconds(time_of_day = datetime.time(0,0,0,0)):
    time_as_timedelta = datetime.timedelta(hours=time_of_day.hour, minutes=time_of_day.minute, seconds=time_of_day.second)
    time_as_milliseconds = int(time_as_timedelta.total_seconds() * 1000)
    print("Time as milliseconds:", time_as_milliseconds)
    return (time_as_milliseconds)

def convert_miliseconds_to_timeOfDay(time_as_milliseconds):
    milliseconds = time_as_milliseconds
    time_as_timedelta = datetime.timedelta(milliseconds=milliseconds)
    hours, remainder = divmod(time_as_timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_of_day = datetime.time(hour=hours, minute=minutes, second=seconds)
    print("Time of day:", time_of_day)
    return time_of_day

#-----------------Read Data Serial-----------------
subFlag = 0
count_err = 0
def processData(data):
    data = data.replace("!", "")
    data = data.replace("#","")
    splitData = data.split("/")
    print(splitData)
    if splitData[0] == "PUB":
        dataName = splitData[1]
        dataValue = float(splitData[2],).__round__(10)
        timestamp = None
        try:
            timestamp_obj = datetime.datetime.strptime(splitData[3], "%Y-%m-%dT%H:%M:%S")
            timestamp = int(timestamp_obj.timestamp() * 1000)
        except Exception as e:
            global count_err
            count_err+=1
            print(count_err)
            print(e)

        if dataName in listVarPub:
            global oldValue, oldTimestamp
            if (dataValue != oldValue[listVarPub.index(dataName)]):
                oldValue[listVarPub.index(dataName)] = dataValue
                oldTimestamp[listVarPub.index(dataName)] = timestamp

                for dataPub in oldValue:
                    device.data.set_value(listVarPub[oldValue.index(dataPub)], dataPub, oldTimestamp[oldValue.index(dataPub)])
                device.publish_data()
                print("Publish successfully!")

mess = ""
def readSerail():
    bytesToRead = ser.in_waiting
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("utf-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end+1])
            if(end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]
#--------------------------------------------------------------------------------------------------------------------------------------

# Create the spB entity object
GroupId = "Group-01"
NodeId = "Node1"
DeviceId = "M1.1"

device = MqttSpbEntityDevice(GroupId, NodeId, DeviceId, _DEBUG)

device.on_message = callback_message  # Received messages
device.on_command = callback_command  # Callback for received commands

# Set the device Attributes, Data and Commands that will be sent on the DBIRTH message --------------------------
# Attributes
device.attribures.set_value("description", "Simple EoN Device node")
device.attribures.set_value("type", "Simulated-EoND-device")
device.attribures.set_value("version", "0.01")
# Data / Telemetry
device.data.set_value("value", 0)
# Commands
device.commands.set_value("rebirth", False)
# Connect to the broker --------------------------------------------
serverUrl = "20.214.136.1"
_connected = False
while not _connected:
    print("Trying to connect to broker...")
    _connected = device.connect(serverUrl, 1883, "user", "password")
    if not _connected:
        print("  Error, could not connect. Trying again in a few seconds ...")
        time.sleep(3)
# Send birth message
device.publish_birth()

# Send some telemetry values ---------------------------------------
while True:
    # Update the data value
    device.data.set_value("injectionTime", round(random.uniform(1.0, 10.0),3))
    device.data.set_value("injectionCycle", float(random.randint(10,20)))
    device.publish_data()
    time.sleep(1)
    # readSerail()

# Disconnect device -------------------------------------------------
# After disconnection the MQTT broker will send the entity DEATH message.
print("Disconnecting device")
device.disconnect()

print("Application finished !")
"""
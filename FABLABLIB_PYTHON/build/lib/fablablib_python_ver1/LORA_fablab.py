from serial import *
import datetime

'''
    The structure of framework to interface with labtop/microcontroller
* SOC + CMD + NAME + VALUE + TIMESTAMP + EOC
* Quy uoc:  SOC = "!" 
*           EOC = "#"
*    }      CMD = "PUB" || "SUB" || "RESTORED"
*    }      NAME = name of variable 
*    }      VALUE = value of variable
*    }      TIMESTAMP = timestamp of variable
'''

class LORA_serial(Serial):
    def __init__(self,
                 port=None,
                 baudrate=9600,
                 bytesize=EIGHTBITS,
                 parity=PARITY_NONE,
                 stopbits=STOPBITS_ONE,
                 timeout=None,
                 type_of_OS="raspberry"
                 ):
        super().__init__(port, baudrate, bytesize, parity, stopbits, timeout)

        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.type_of_OS = type_of_OS

        self.count_err = 0
        self.mess = ""

        if self.port is not None:
            self.port = port
        else:
            if self.type_of_OS == "laptop":
                port = "COM7"
            elif self.type_of_OS == "raspberry":
                # port = '/dev/serial0',    # module RS485 thường
                port = '/dev/ttyUSB0',    # module RS485 USB
        
        self.ser = Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)
    
    def generate_data_transfer(self, dataName, dataValue, dataTimestamp):
        SOC = "!"
        EOC = "#"
        CMD = "SUB"
        NAME = str(dataName) 
        VALUE = str(dataValue)
        TIMESTAMP = str(dataTimestamp)
        dataTrans = str(SOC + CMD + ":" + NAME + ":" + VALUE + ":" + TIMESTAMP + EOC)
        return (str(dataTrans))

    def processDataLora(self, cmd="PUB", data=None):
        dataName = None
        dataValue = None
        timestamp = None

        data = data.replace("!", "")
        data = data.replace("#","")
        splitData = data.split(":")
        print(splitData)
        if splitData[0] == cmd:
            dataName = splitData[1]
            dataValue = float(splitData[2]).__round__(5)
            try:
                timestamp_obj = datetime.datetime.strptime(splitData[3], "%Y-%m-%dT%H:%M:%S")
                timestamp = int(timestamp_obj.timestamp()*1000)
            except Exception as e:
                self.count_err += 1
                print(self.count_err)
                print(e)
            
            return dataName, dataValue, timestamp

    def lora_read_data(self):
        bytesToRead = self.ser.in_waiting
        if (bytesToRead > 0):
            self.mess = self.mess + self.ser.read(bytesToRead).decode()
            while ("#" in self.mess) and ("!" in self.mess):
                start = self.mess.find("!")
                end = self.mess.find("#")
                self.processDataLora(self.mess[start:end+1])
                if(end == len(self.mess)):
                    self.mess = ""
                else:
                    self.mess = self.mess[end+1:]

    def lora_send_data(self, dataName, dataValue, dataTimestamp):
        self.ser.write((self.generate_data_transfer(dataName, dataValue, dataTimestamp)).encode())
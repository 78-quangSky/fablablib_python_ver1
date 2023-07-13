from serial import *
import struct
import time


class RS485(Serial):
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

        if self.port is not None:
            self.port = port
        else:
            if self.type_of_OS == "laptop":
                port = "COM3"
            elif self.type_of_OS == "raspberry":
                # port = '/dev/serial0',    # module RS485 thường
                port = '/dev/ttyUSB0',    # module RS485 USB
        
        self.ser = Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout)

class RS485_heatController(RS485):
    def __init__(self,
                 port=None,
                 baudrate=9600,
                 bytesize=EIGHTBITS,
                 parity=PARITY_NONE,
                 stopbits=STOPBITS_ONE,
                 timeout=None,
                 type_of_OS="raspberry"
                 ):
        super().__init__(port, baudrate, bytesize, parity, stopbits, timeout, type_of_OS)
    
    def read_temperature_value(self, type_value, device_id):
        _temperature_name = 'heatController-' + str(device_id) + '-' + type_value
        # Read holding register function code
        function_code = 3
        # Start address for temperature PV/SP value
        if type_value == "PV":
            start_address = 0       # read process value
        elif type_value == "SP":
            start_address = 262     # read set point
        # Number of registers to read
        register_count = 2
        # Calculate Modbus RTU message
        message = bytearray([device_id, function_code, start_address >> 8, start_address & 0xff,
                            register_count >> 8, register_count & 0xff])
        # Calculate CRC
        crc = 0xFFFF
        for i in range(len(message)):
            crc = crc ^ message[i]
            for j in range(8):
                if (crc & 0x0001) != 0:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc = crc >> 1
        # Append CRC to message
        message.append(crc & 0xff)
        message.append(crc >> 8)
        # Write message to serial port
        self.ser.write(message)
        time.sleep(0.2)
        response = self.ser.read(9)
        # Check response length and validity of CRC
        if len(response) != 9:
            return None
        else:
            crc = 0xFFFF
            for i in range(len(response) - 2):
                crc = crc ^ response[i]
                for j in range(8):
                    if (crc & 0x0001) != 0:
                        crc = (crc >> 1) ^ 0xA001
                    else:
                        crc = crc >> 1
            # Check if calculated CRC matches the received CRC
            if crc != (response[-1] << 8 | response[-2]):
                return None
            else:
                # Return the temperature value in Celsius
                address, function_code, byte_count, temperature_value = struct.unpack('!BBBl', response[:7])
                temperature_name = self.config_var_name(_temperature_name)
                machine_ID = self.config_deviecID(self.var_dictionary[_temperature_name])
                return temperature_name, temperature_value/10, machine_ID
            
    def detect_heatController_isActive(self, ID_heatcontroller_list):
        for ID in ID_heatcontroller_list:
            check_ID = self.read_temperature_value(device_id=ID)
            if check_ID is None:
                ID_heatcontroller_list.remove(ID)

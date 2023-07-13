import json
import datetime
from .convert_time_fablab import convertTime_fablab

class json_payload:
    def generate_data_status(state, value):
        data = [{
                "name": "machineStatus",
                "value": value,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            }]
        return json.dumps(data)

    def generate_data_publish(data_name, data_value):
        data = [{
                "name": str(data_name),
                "value": data_value,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            }]
        return json.dumps(data)

    def generate_data_badProducts(count):
        data = [{
                    "name": "badProduct-1",
                    "value": count,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }]
        return (json.dumps(data))

    # Chuỗi JSON về tổng hợp thời gian làm việc trong một ca
    def generate_data_totalTime(_No_machine, _total_curingTime, _total_shotCount, _total_cycleTime, _CA, deviecID):   #Total information
        data = [{
                    "name": "totalTime",
                    "machinePosition": _No_machine,
                    "curingTime": convertTime_fablab.convert_miliseconds_to_timeOfDay(_total_curingTime).strftime("%H:%M:%S"),
                    "cycleTime": convertTime_fablab.convert_miliseconds_to_timeOfDay(_total_cycleTime).strftime("%H:%M:%S"),
                    "shotCount": _total_shotCount,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    "shiftNumber": _CA,
                    "deviceId": deviecID
        }]
        return (json.dumps(data)) 

    def generate_http_data_post_total(shiftNumber, CycleTotal, deviceID="I1"):
        data_dict = {
                    "name": "post HTTP",
                    "deviceId": deviceID,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "shiftNumber": shiftNumber,
                    "totalInjectionCycle": CycleTotal
        }
        return (json.dumps(data_dict))

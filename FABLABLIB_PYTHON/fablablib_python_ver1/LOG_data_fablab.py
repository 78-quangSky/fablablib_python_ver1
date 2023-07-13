import datetime


class LOG_DATA:
    def __init__(
        self,
        project="ThaiDuong_SIEMENS",     # "ThaiDuong_SIEMENS" or "ThaiDuong_OMRON" or "VTS_auto"
        mode_init_file="w+",    # self.mode_init_file or "a+" 
        type_of_OS="raspberry"
    ):
        self.project = project
        self.mode_init_file = mode_init_file
        self.type_of_OS = type_of_OS

        self.init_file_csv = True
        self.array_var = []

        if self.type_of_OS == "raspberry":
            self.folder_path = "/home/pi/"
        elif self.type_of_OS == "laptop":
            self.folder_path = ""

    def init_file_log_csv(self, data_name, deviceID):
        if self.init_file_csv:
            if self.project == "ThaiDuong_SIEMENS":
                with open(self.folder_path + "store_data_HAITAIN.csv", self.mode_init_file) as file:
                    file.write('{0},{1},{2}\n'.format('Name', 'Value', 'Timestamp'))
            
            elif self.project == "ThaiDuong_OMRON":
                with open(self.folder_path + "left_machine_store_data_PANSTONE.csv", self.mode_init_file) as file:
                    file.write('{0},{1},{2}\n'.format('Name', 'Value', 'Timestamp'))
                with open(self.folder_path + "right_machine_store_data_PANSTONE.csv", self.mode_init_file) as file:
                    file.write('{0},{1},{2}\n'.format('Name', 'Value', 'Timestamp'))

            elif self.project == "VTS_auto":
                with open(self.folder_path + "store_data_vali_VTSauto.csv", self.mode_init_file) as file:
                    file.write('{0},{1},{2}\n'.format('Name', 'Value', 'Timestamp'))
            self.init_file_csv = False
        
        if (data_name in self.array_var) == False:
            self.array_var.append(data_name)
            if self.project == "ThaiDuong_OMRON":
                with open(self.folder_path + "store_data/" + deviceID + "_machine/" + data_name + ".csv", "a+") as file:
                    file.write('{0},{1}\n'.format('Value','Timestamp'))
            else:
                with open(self.folder_path + "store_data/" + data_name + ".csv", self.mode_init_file) as file:
                    file.write('{0},{1}\n'.format('Value','Timestamp'))

    def common_form_csv(self, data_name, data_value, deviceID="left"):
        self.init_file_log_csv(data_name, deviceID)
        data_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        if self.project == "ThaiDuong_SIEMENS":
            with open(self.folder_path + "store_data_HAITAIN.csv", "a+") as file:
                file.write('{0},{1},{2}\n'.format(data_name, data_value, data_timestamp))
            with open(self.folder_path + "store_data/" + data_name + ".csv", "a+") as file:
                file.write('{0},{1}\n'.format(data_value, data_timestamp))
        
        elif self.project == "ThaiDuong_OMRON":
            with open(self.folder_path + deviceID + "_machine_store_data_PANSTONE.csv", "a+") as file:
                file.write('{0},{1},{2}\n'.format(data_name, data_value, data_timestamp))
            with open(self.folder_path + "store_data/" + deviceID + "_machine/" + data_name + ".csv", "a+") as file:
                file.write('{0},{1}\n'.format(data_value, data_timestamp))

        elif self.project == "VTS_auto":
            with open(self.folder_path + "store_data_vali_VTSauto.csv", "a+") as file:
                file.write('{0},{1},{2}\n'.format(data_name, data_value, data_timestamp))
            with open(self.folder_path + "store_data/" + data_name + ".csv", "a+") as file:
                file.write('{0},{1}\n'.format(data_value, data_timestamp))
    
    def common_form_txt(self, data_name, data_value):
        data_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        if self.project == "ThaiDuong_SIEMENS":
            with open(self.folder_path + "store_data_HAITAIN.txt", "a+") as file:
                file.write('{0},{1},{2}\n'.format(data_name, data_value, data_timestamp))
        
        elif self.project == "ThaiDuong_OMRON":
            with open(self.folder_path + "store_data_PANSTONE.txt", "a+") as file:
                file.write('{0},{1},{2}\n'.format(data_name, data_value, data_timestamp))

        elif self.project == "VTS_auto":
            with open(self.folder_path + "store_data_vali_VTSauto.txt", "a+") as file:
                file.write('{0},{1},{2}\n'.format(data_name, data_value, data_timestamp))
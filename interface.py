from sys_info import sys_info
import numpy as np
from messaging import send_message
import time
import datetime

class system_care:

    def __init__(self):
        # params settings
        self.__sys_info = sys_info()
        self.__battery_flag = 0
        self.__temperature_flag = 0
        self.__utilization_flag = 0
        self.__disk_flag = 0
        self.__memory_flag = 0

    def greetings(self):
        message = "How long did I sleep?, any way I'm awake now :)"
        with open('logs.txt', 'w') as f:
            f.write('{}' + message + '\n'.format(str(datetime.datetime.now())))
            f.close()

    def interface(self):
        # greet when system starts
        self.greetings()
        
        # checkers
        # get CPU temperature values
        cpu_temperatures = self.__sys_info.check_temperature()
        temp_list = list()
        for cpu in cpu_temperatures:
            temp_list.append(cpu.get('current_temp'))
        average_temperature = np.average(temp_list)

        # get CPU utilization values
        cpu_util = self.__sys_info.check_cpu_util()
        cpu_util = cpu_util.get('cpu_utilization')
        temp_list = list()
        for cpu in cpu_util:
            temp_list.append(cpu.get('percentage'))
        average_utilization = np.average(temp_list)

        # get memory consumption data
        memory = self.__sys_info.check_memory()
        memory = memory.get('results')

        # get disk consumption data
        disk = self.__sys_info.check_disk()
        disk = disk.get('results')

        while True:
            # notify if battery percentage is less than 50% and not on charge
            battery_info = self.__sys_info.check_battery()
            if not battery_info.get('power_plugged') and battery_info.get('percentage') < 30:
                if self.__battery_flag == 0:
                    subject = "Laptop Battery Running Down"
                    message = "Current Battery Percentage is {}%. "\
                    "Please connect to a power supply".format(battery_info.get('percentage'))
                    try:
                        send_message(subject=subject, message=message)
                        self.__battery_flag = 1
                    except Exception as e:
                        self.__battery_flag = 1
                        with open('logs.txt', 'w') as f:
                            f.write(str(e))
                            f.write('\n')
                            f.close()
                
            # notify if battery percentage is greater than 95% and on charge
            elif battery_info.get('power_plugged') and battery_info.get('percentage') > 95:
                if self.__battery_flag == 0:
                    subject = "Laptop Battery almost fully charged"
                    message = "Current Battery Percentage is {}%. "\
                    "Please disconnect from power supply".format(battery_info.get('percentage'))
                    try:
                        send_message(subject=subject, message=message)
                        self.__battery_flag = 1
                    except Exception as e:
                        self.__battery_flag = 1
                        with open('logs.txt', 'w') as f:
                            f.write(str(e))
                            f.write('\n')
                            f.close()

            else:
                battery_flag = 0

            # notify if average CPU temperature percentage > 85
            if average_temperature > 85:
                if self.__temperature_flag == 0:
                    # send the individual temperature of all CPUs
                    subject = "Average CPU temperature above {} Deg. Celc.".format(average_temperature)
                    message = ""
                    for cpu in cpu_temperatures:
                        message += "{} : {} Deg. Celc. ".format(cpu.get('label'), cpu.get('current_temp'))
                    try:
                        send_message(subject=subject, message=message)
                        self.__temperature_flag = 1
                    except Exception as e:
                        self.__temperature_flag = 1
                        with open('logs.txt', 'w') as f:
                            f.write(str(e))
                            f.write('\n')
                            f.close()
            
            else:
                self.__temperature_flag = 0

            # notify if cpu_utilization > 70%
            if average_utilization > 70:
                if self.__utilization_flag == 0:
                    # send individual utilization of all CPUs
                    subject = "(Warning) Average CPU temperature above {} %.".format(average_utilization)
                    message = ""
                    for cpu in cpu_util:
                        message += "{} : {} %.  ".format(cpu.get('label'), cpu.get('percentage'))
                    try:
                        send_message(subject=subject, message=message)
                        self.__utilization_flag = 1
                    except Exception as e:
                        self.__utilization_flag = 1
                        with open('logs.txt', 'w') as f:
                            f.write(str(e))
                            f.write('\n')
                            f.close()
            else:
                self.__utilization_flag = 0
            
            # notify if available memory < 100 MB
            if memory.get('available_memory') < 100:
                if self.__memory_flag == 0:
                    subject = "(Warning) Running Low on Virtual Memory"
                    message = "System only has {} MB of Virtual Memory at the " \
                    "moment. Consumed {} MB of memory".format(memory.get('available_memory'),memory.get('used_memory') )
                    try:
                        send_message(subject=subject, message=message)
                        self.__memory_flag = 1
                    except Exception as e:
                        self.__memory_flag = 1
                        with open('logs.txt', 'w') as f:
                            f.write(str(e))
                            f.write('\n')
                            f.close()
            else:
                self.__memory_flag = 0


            # notify if free disk space < 20GB
            if disk.get('disk_available') < 20000:
                if self.__disk_flag == 0:
                    subject = "(Warning) Running Low of Physical Storage"
                    message = "System only has {} MB of Physical Storage at the moment" \
                    ". Consumed {} MB of Storage. ({} %)".format(disk.get('disk_available'), disk.get('disk_used'), \
                    disk.get('disk_percent_usage'))
                    try:
                        send_message(subject=subject, message=message)
                        self.__disk_flag = 1
                    except Exception as e:
                        self.__disk_flag = 1
                        with open('logs.txt', 'w') as f:
                            f.write(str(e))
                            f.write('\n')
                            f.close()
            else:
                self.__disk_flag = 0

            time.sleep(10)

# kick start
system_care().interface()

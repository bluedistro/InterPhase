import psutil

class sys_info:

    def __init__(self):
        pass

    def check_cpu_util(self):
        # check cpu utilization as a percentage
        cpu_utilization = psutil.cpu_percent(interval=1, percpu=True)
        # get cpu stats
        cpu_stats = psutil.cpu_stats()
        # get cpu frequency
        cpu_freqs = psutil.cpu_freq(percpu=True)

        # properly handle cpu frequencies: returned in MHz
        cpu_freq_list = list()
        for i, cpu_freq in enumerate(cpu_freqs):
            cpu_freq_dict = dict()
            cpu_freq_dict.update({
                "label": "Core {}".format(i),
                "current_freq": cpu_freq.current,
                "min_freq": cpu_freq.min,
                "max_freq": cpu_freq.max
            })
            cpu_freq_list.append(cpu_freq_dict)

        # properly handle cpu utilization percentage returns
        cpu_util_list = list()
        for i, cpu in enumerate(cpu_utilization):
            cpu_util_dict = dict()
            cpu_util_dict.update({
                "label": "Core {}".format(i),
                "percentage": cpu 
            })
            cpu_util_list.append(cpu_util_dict)

        # handle other cpu information
        cpu_info = {
            "cpu_utilization": cpu_util_list,
            "cpu_frequency": cpu_freq_list,
            "context_switches": cpu_stats.ctx_switches,
            "interrupts": cpu_stats.interrupts,
            "soft_interrupts": cpu_stats.soft_interrupts,
            "system_calls": cpu_stats.syscalls
        }
        return cpu_info

    def check_memory(self):
        # get available memory
        memory = psutil.virtual_memory()
        div_standard = 1024 * 1024 # 1MB
        available_memory = memory.available // div_standard
        used_memory = memory.used // div_standard
        memory_info = {
            "header": "units in MB",
            "results":{
                "available_memory": available_memory,
                "used_memory": used_memory
            }
        }
        return memory_info

    def check_disk(self):
        # get disk usage
        disk = psutil.disk_usage('/')
        div_standard = 1024 * 1024 # 1MB
        disk_available = disk.free // div_standard
        disk_used = disk.used // div_standard
        disk_total = disk.total // div_standard
        disk_percent_usage = disk.percent
        disk_info = {
            "header": "units in MB",
            "results":{
            "disk_available": disk_available,
            "disk_total": disk_total,
            "disk_used": disk_used,
            "disk_percent_usage": disk_percent_usage,
            }
        }
        return disk_info

    def check_temperature(self):
        # get temperatures : returns a list of the coretemp
        temperatures = psutil.sensors_temperatures()
        # get the temperature of each of the cpus and return the information as a list of dict objects
        cpu_temps = temperatures.get('coretemp')
        cpu_temp_list = list()
        for item in cpu_temps:
            cpu_temp_dict = dict()
            cpu_temp_dict.update({
                                "label": item.label,
                                "current_temp": item.current,
                                "high": item.high,
                                "critical": item.critical
                                })
            cpu_temp_list.append(cpu_temp_dict)
        return cpu_temp_list

    def check_fan(self):
        # get the fans
        cpu_fan = psutil.sensors_fans()
        if len(cpu_fan) == 0:
            cpu_fan.update({"Status": "Fan Sensors are not supported by the Operating System"})
        return cpu_fan

    # helper method for battery uptime
    def sec2hours(self, secs):
        mm, ss = divmod(secs, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d" % (hh, mm, ss)

    def check_battery(self):
        battery = psutil.sensors_battery()
        if battery.power_plugged:
            percentage = round(battery.percent, 2)
            battery_info = {"percentage": percentage, "power_plugged": True}
        else:
            time_left = self.sec2hours(battery.secsleft)
            percentage = round(battery.percent, 2)
            battery_info = {"timeLeft": time_left, "percentage": percentage, "power_plugged":False}
        return battery_info


# print(check_disk())
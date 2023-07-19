import platform
import psutil
import cpuinfo

def get_platform_info():
    temp_dict = {}
    temp_dict['os'] = platform.system()
    temp_dict['os_detail'] = platform.platform()
    temp_dict['cpu_brand'] = cpuinfo.get_cpu_info()['brand_raw']
    temp_dict['cpu_arc'] = platform.machine()
    temp_dict['physical_cores'] = psutil.cpu_count(logical=False)
    temp_dict['logical_cores'] = psutil.cpu_count(logical=True)
    temp_dict['memory_mega_bytes'] = round(psutil.virtual_memory().total / (1024**2))

    return temp_dict

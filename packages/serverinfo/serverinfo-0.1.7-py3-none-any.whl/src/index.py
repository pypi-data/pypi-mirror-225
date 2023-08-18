import xmltodict
import subprocess
import platform
#import cpuinfo
import socket
import psutil
import re
import datetime
import sys

uname = platform.uname()

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def get_size(bytes, suffix="M"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return round(bytes,2) #f"{bytes:.2f}"#{unit}{suffix}"
        bytes /= factor


def getGPU(gpu):

	mem_total = int(gpu['fb_memory_usage']['total'].replace(" MiB",""))
	mem_free = int(gpu['fb_memory_usage']['free'].replace(" MiB",""))
	mem_use = mem_total - mem_free

	return {
		"name" : gpu['product_name'],
		"persist" : gpu["persistence_mode"],
		"mem_total" : mem_total,
		"mem_use" : mem_use,
		"mem_free" : mem_free,
		"mem_load" : round(mem_use * 100 / mem_total,2),
		"load" : int(gpu['utilization']['gpu_util'].replace(" %","")),
		"temp" : int(gpu['temperature']['gpu_temp'].replace(" C","")),
		"temp_max" : int(gpu['temperature']['gpu_temp_max_gpu_threshold'].replace(" C","")),
		"power" : float(gpu['power_readings']["power_draw"].replace(" W","")),
		#"power_setting" : float(gpu['power_readings']["enforced_power_limit"].replace(" W","")),
		"power_limit" : round(float(gpu['power_readings']["power_limit"].replace(" W",""))),
		"power_max" : round(float(gpu['power_readings']["max_power_limit"].replace(" W",""))),
		"gpu_clock" : int(gpu['clocks']['sm_clock'].replace(" MHz","")),
		"gpu_clock_max" : int(gpu['max_clocks']['sm_clock'].replace(" MHz","")),
		"mem_clock" : int(gpu['clocks']['mem_clock'].replace(" MHz","")),
		"mem_clock_max" : int(gpu['max_clocks']['mem_clock'].replace(" MHz","")),
	}

def getCPU():
	cpufreq = psutil.cpu_freq()
	svmem = psutil.virtual_memory()
	disk_total = 0
	disk_use = 0
	disk_free = 0
	disk_percent = 0

	partitions = psutil.disk_partitions()
	for partition in partitions:
	    try:
	        partition_usage = psutil.disk_usage(partition.mountpoint)
	    except PermissionError:
	        continue
	    disk_total = disk_total + get_size(partition_usage.total)
	    disk_use = disk_use + get_size(partition_usage.used)
	    disk_free = disk_free + get_size(partition_usage.free)
	    #disk_percent =  partition_usage.percent

	return {
		"cores" : psutil.cpu_count(logical=False),
		"threads" : psutil.cpu_count(logical=True),
		"cpu_max" : cpufreq.max/1000,
		"cpu_min" : cpufreq.min/1000,
		"cpu_current" : round(cpufreq.current,2),
		"cpu_load" : psutil.cpu_percent(),
		"mem_total" : get_size(svmem.total),
		"mem_use" : get_size(svmem.used),
		"mem_free" : get_size(svmem.available),
		"mem_load" : svmem.percent,
		"disk_total" : round(disk_total),
		"disk_use" : round(disk_use),
		"disk_free" : round(disk_free),
		"disk_load" : round(disk_use * 100 / disk_total,2)
	}
	
"""
	# get IO statistics since boot
	#disk_io = psutil.disk_io_counters()
	#print(f"Total read: {get_size(disk_io.read_bytes)}")
	#print(f"Total write: {get_size(disk_io.write_bytes)}")
	
	
	
	##get IO statistics since boot
	#net_io = psutil.net_io_counters()
	#print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
	#print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
"""
	#import socket


result = subprocess.check_output("nvidia-smi -x -q", shell=True)
info = xmltodict.parse(result)
gpus = info['nvidia_smi_log']['gpu']

infos = []

if isinstance(gpus, list):
	for gpu in gpus:
		infos.append(getGPU(gpu))
else:
	infos.append(getGPU(gpus))
"""
print({
	"os" : uname.system,
	"version" : uname.release.split('-')[0],
	"driver" : info['nvidia_smi_log']['driver_version'],
	"cuda" : float(info['nvidia_smi_log']["cuda_version"]),
	"python" : str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro),
	"ip" : getIP(),
	"cpu" : getCPU(),
	"gpu" : infos
})
"""
def getInfo():
	return {
		"os" : uname.system,
		"version" : uname.release.split('-')[0],
		"driver" : info['nvidia_smi_log']['driver_version'],
		"cuda" : float(info['nvidia_smi_log']["cuda_version"]),
		"python" : str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro),
		"ip" : getIP(),
		"cpu" : getCPU(),
		"gpu" : infos
	}
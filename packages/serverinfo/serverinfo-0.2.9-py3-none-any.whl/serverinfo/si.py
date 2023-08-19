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
    #for unit in ["", "K", "M", "G", "T", "P"]:
    #    if bytes < factor:
    #        return round(bytes,2) #f"{bytes:.2f}"#{unit}{suffix}"
    #    bytes /= factor
    return round( bytes / (1024 * 1024),2)

def __getGPU(gpu):
	mem_total = int(gpu['fb_memory_usage']['total'].replace(" MiB",""))
	mem_free = int(gpu['fb_memory_usage']['free'].replace(" MiB",""))
	mem_use = mem_total - mem_free
	power = None
	limit = None

	if gpu.get('power_readings'):
		power = gpu['power_readings']
	elif gpu.get('gpu_power_readings'):
		power = gpu[('gpu_power_readings')]

	if power.get("power_limit"):
		limit = power["power_limit"]
	elif power.get("current_power_limit"):
		limit = power["current_power_limit"]

	persist = False
	if gpu["persistence_mode"] == "Enabled":
		persist = True

	display = False
	if gpu["display_mode"] == "Enabled":
		display = True

	return {
		"name" : gpu['product_name'],
		"brand" : gpu['product_brand'],
		"arch" : gpu['product_architecture'],
		"persist" : persist,
		"display" : display,
		"total" : mem_total,
		"use" : mem_use,
		"free" : mem_free,
		"mem_load" : round(mem_use * 100 / mem_total,2),
		"gpu_load" : int(gpu['utilization']['gpu_util'].replace(" %","")),
		"fan_load" : int(gpu['fan_speed'].replace(" %","")),
		"temp" : int(gpu['temperature']['gpu_temp'].replace(" C","")),
		"temp_max" : int(gpu['temperature']['gpu_temp_max_gpu_threshold'].replace(" C","")),
		"power" : round(float(power["power_draw"].replace(" W",""))),
		"power_limit" : round(float(limit.replace(" W",""))),
		"power_max" : round(float(power["max_power_limit"].replace(" W",""))),
		"gpu_clock" : int(gpu['clocks']['video_clock'].replace(" MHz","")),
		"gpu_clock_max" : int(gpu['max_clocks']['video_clock'].replace(" MHz","")),
		"mem_clock" : int(gpu['clocks']['mem_clock'].replace(" MHz","")),
		"mem_clock_max" : int(gpu['max_clocks']['mem_clock'].replace(" MHz","")),
	}


def getGPU():
	result = None

	try :
		result = subprocess.check_output("nvidia-smi -x -q", shell=True).decode('UTF-8')
		#print(result,result.startswith("<?"))
		if result.startswith("<?"):
			info = xmltodict.parse(result)
			gpus = info['nvidia_smi_log']['gpu']

			infos = []

			if isinstance(gpus, list):
				for gpu in gpus:
					infos.append(__getGPU(gpu))
			else:
				infos.append(__getGPU(gpus))

			result = {
				"driver" : info['nvidia_smi_log']['driver_version'],
				"cuda" : float(info['nvidia_smi_log']["cuda_version"]),
				"count" : int(info['nvidia_smi_log']["attached_gpus"]),
				"list" : infos
			}
	except:
		result = {
			"driver" : 0,
			"cuda" : 0,
			"count" : 0,
			"list" : []
		}

	return result

#def setPower(power):
#	return subprocess.check_output("nvidia-smi -pl " + str(power), shell=True)

def getCPU():
	cpufreq = psutil.cpu_freq()

	return {
		"count" : psutil.cpu_count(logical=False),
		"threads" : psutil.cpu_count(logical=True),
		"max" : round(cpufreq.max),
		"min" : round(cpufreq.min),
		"current" : round(cpufreq.current),
		"load" : psutil.cpu_percent(),
	}

def getMem():
	mem = psutil.virtual_memory()
	return {
		"total" : get_size(mem.total),
		"use" : get_size(mem.used),
		"free" : get_size(mem.available),
		"load" : mem.percent,
	}

def getSwap():
	mem = psutil.swap_memory()
	return {
		"total" : get_size(mem.total),
		"use" : get_size(mem.used),
		"free" : get_size(mem.free),
		"load" : mem.percent,
	}


def getDisk():
	disks = []
	disk_total = 0
	disk_use = 0
	disk_free = 0

	partitions = psutil.disk_partitions()
	for partition in partitions:
		#print(partition.device, partition.mountpoint)
		try:
			partition_usage = psutil.disk_usage(partition.mountpoint)
		except PermissionError:
			continue

		total = get_size(partition_usage.total)
		use = get_size(partition_usage.used)
		free = get_size(partition_usage.free)

		disk_total = disk_total + total
		disk_use = disk_use + use
		disk_free = disk_free + free

		disks.append({
			"name" : partition.device,
			"mount" : partition.mountpoint,
			"total" : total,
			"use" : use,
			"free" : free,
			"load" : round(use / total  * 100)
		})

		#percent =  partition_usage.percent

	return {
		"count" : len(disks),
		"total" : round(disk_total),
		"use" : round(disk_use),
		"free" : round(disk_free),
		"load" : round(disk_use / disk_total * 100),
		"list" : disks
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
def getAll():
	return {
		"os" : uname.system,
		"version" : uname.release.split('-')[0],
		"ip" : getIP(),
		"arch" : uname.machine,
		"cpu" : getCPU(),
		"mem" : getMem(),
		"swap" : getSwap(),
		"disk" : getDisk(),
		"gpu" : getGPU(),
		"python" : str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro)
	}

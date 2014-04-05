#! /usr/bin/env python

import subprocess
import re

def getDevices():
	result = subprocess.check_output(["ls", "-1", "/Volumes"])
	deviceList = result.split("\n")[:-1];
	return deviceList

def getDeviceNode():
	NTFS_PATTERN = re.compile(r'File System Personality:  NTFS')
	NTFS_DEVICE_NODE_PATTERN = re.compile(r'.*Device Node:.*')
	deviceList = getDevices()
	deviceNodeDict = {}
	
	for deviceName in deviceList:
		diskPath = "/Volumes/" + deviceName
		try:
			diskInfo = subprocess.check_output(["diskutil", "info", diskPath]);
		except subprocess.CalledProcessError, e:
			print "diskutil stderr output:\n", e.output
		if NTFS_PATTERN.search(diskInfo):
			deviceNodeStr = NTFS_DEVICE_NODE_PATTERN.findall(diskInfo)
			deviceNode = deviceNodeStr[0].split()[2]
			deviceNodeDict[diskPath] = deviceNode
	return deviceNodeDict

def getDeviceNameByPath(diskPath):
	print array

def mountDevice(deviceNodeDict):
	if not deviceNodeDict:
		print "No ntfs filesystem device found..."
		return
	for diskPath in deviceNodeDict.keys():
		deviceNode = deviceNodeDict[diskPath]
		print subprocess.check_output(["hdiutil", "eject", diskPath]) 
		deviceName = diskPath.split("/")[-1]
		deviceNode = deviceNodeDict[diskPath]
		mountPath = "MYHD/" + deviceName + "-mounted"
		subprocess.call(["mkdir", "-p", mountPath])
		print "sudo mount_ntfs -o rw,nobrowse %s %s" % (deviceNode, mountPath)
		subprocess.check_output(["sudo", "mount_ntfs", "-o", "rw,nobrowse", deviceNode, mountPath])
		print "mount done...\n"

if __name__ == '__main__':
	deviceNodeDict = getDeviceNode()
	mountDevice(deviceNodeDict)

# Dummy script for automatically record without pressing the capture button (27s for each video cuz idk)

import binascii
import struct
import time
import usb.core
import usb.util

global_dev = None
global_out = None
global_in = None

#Hotfix to handle data received larger than 4080 bytes
#Very ineficient, but it will get the job done for now
def readData():
	size = int(struct.unpack("<L", global_in.read(4, timeout=0).tobytes())[0])

	data = [0] * size
	if size > 4080:
		i = 0
		while i < size:
			chunkSize = 4080
			if size - i < 4080:
				chunkSize = size - i
			x = global_in.read(chunkSize, timeout=0).tobytes()

			for j in range(len(x)):
				data[i] = x[j]
				i+=1
	else:
		x = global_in.read(size, timeout=0).tobytes()

		#Converts received data to integer array
		for i in range(size):
			data[i] = int(x[i])

	return data

#Sends string commands to the switch
#Uncomment return if using echoCommands
def sendCommand(content):
    global_out.write(struct.pack("<I", (len(content)+2)))
    global_out.write(content)
    #return readData()

#Using method from Goldleaf
def connect_switch():
    global global_dev
    global global_out
    global global_in
    global_dev = usb.core.find(idVendor=0x057E, idProduct=0x3000)
    if global_dev is not None:
        try:
            global_dev.set_configuration()
            intf = global_dev.get_active_configuration()[(0,0)]
            global_out = usb.util.find_descriptor(intf,custom_match=lambda e:usb.util.endpoint_direction(e.bEndpointAddress)==usb.util.ENDPOINT_OUT)
            global_in = usb.util.find_descriptor(intf,custom_match=lambda e:usb.util.endpoint_direction(e.bEndpointAddress)==usb.util.ENDPOINT_IN)
            return True
        except:
            return False
            pass
    else:
        return False

#To communicate with the user
def attemptConnection():
	isConnected = False
	while not isConnected:
		if connect_switch():
			print("Connected to Switch Successfully!")
			isConnected = True
		else:
			print("Failed to Connect to Switch!")
			print("Attempting to Reconnect in 5 Seconds...")
			time.sleep(5)


def main():
	attemptConnection()
	
	#Button commands to send
	sendCommand("press CAPTURE")
	time.sleep(1)

main()

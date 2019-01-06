import os
import re
import logging
from math import pow

class IP(object):
	def __init__(self, ipAddress, requirehosts = 0):
		self.__ipAddress = self.__setIPAddress__(ipAddress)
		self.__requireHosts = requirehosts
		self.__requireBit = self.__getBorrowBitValue()
		self.__network = ""
		self.__subnet =""
		self.__setAdditional__(self.__ipAddress)
		self.__gateway = self.__setGateway__()
		self.__broadcast = self.__setBroadcast__()

	def getIPAddress(self):
		return self.__ipAddress
	
	def getSubnet(self):
		return self.__subnet
	
	def getGateway(self):
		return self.__gateway
	
	def getNetwork(self):
		return self.__network
	
	def getBroadcast(self):
		return self.__broadcast

	def __setIPAddress__(self,ip):
		try:
			if(re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip)):
				if(self.inRange(ip)):
					return ip
				raise Exception ("One of the octet in {} exceed more than 255. Not a real IP Address.".format(self.__ipAddress))
			raise FormatError("Does not fit in the format of XXX.XXX.XXX.XXX")
		except Exception as error:
			logging.error(error)
	
	def __setGateway__(self):
		tempIP = re.split(('\.'),self.__network)
		tempIP[3] = int(tempIP[3]) + 1
		return ".".join(str(x) for x in tempIP) 
		
	#Setting Subnet/Gateway based off the first octet in the IP Address
	def __setAdditional__(self, ip):
		try:
			tempIP = re.split(('\.'),ip)
			subnet = ["0","0","0","0"]
			gateway = ["0","0","0","0"]
			
			#Type A IP Address
			if(int(tempIP[0]) <= 0 | int(tempIP[0]) <= 126):
				
				if(self.__requireBit > 8):
					octetWS = self.requireOctetRange()
					for i in range(octetWS):
						subnet[i] = 255
						gateway[i] = tempIP[i]
					subnet[octetWS] = self.__convertRequireToNetworkValue(self.__requireBit % 8)
					gateway[octetWS] = self.getOctetValue(tempIP[octetWS], subnet[octetWS])
				else:
					subnet[0] = "255"
					subnet[1] = self.__convertRequireToNetworkValue(self.__requireBit % 8)
					gateway[0] = tempIP[0]
					gateway[1] = self.getOctetValue(tempIP[1], subnet[1])
					
			#Type B IP Address
			elif(int(tempIP[0]) <= 128 | int(tempIP[0]) <= 191):
				if(self.__requireBit > 8):
					octetWS = self.requireOctetRange()
					for i in range(octetWS):
						subnet[i] = 255
						gateway[i] = tempIP[i]
					subnet[octetWS] = self.__convertRequireToNetworkValue(self.__requireBit % 8)
					gateway[octetWS] = self.getOctetValue(tempIP[3], subnet[octetWS])
					
				else:
					for i in range(2):
						subnet[i] = "255"
						gateway[i] = tempIP[i]
					subnet[2] = self.__convertRequireToNetworkValue(self.__requireBit % 8)
					gateway[2] = self.getOctetValue(tempIP[2], subnet[2])

					
			#Type C IP Address
			elif(int(tempIP[0]) <= 192 | int(tempIP[0]) <= 224):
				if(self.__requireBit > 1):
					octetWS = self.requireOctetRange()
					for i in range(octetWS):
						subnet[i] = 255
						gateway[i] = tempIP[i]
					subnet[octetWS] = self.__convertRequireToNetworkValue(self.__requireBit % 8)
					gateway[octetWS] = self.getOctetValue(tempIP[3], subnet[octetWS])
				else:
					for i in range(3):
						subnet[i] = "255"
						gateway[i] = tempIP[i]
					subnet[3] = self.__convertRequireToNetworkValue(self.__requireBit)
					gateway[3] = self.getOctetValue(tempIP[2], self.__requireBit)
			else:
				raise Exception("IP Address is in the experiment range.")
		except Exception as error:
			logging.warning(error)
		self.__subnet = ".".join(str(x) for x in subnet)
		self.__network = ".".join(str(x) for x in gateway)
		
	def __setBroadcast__(self):
		tempGateway = re.split(r'\.',self.__network)
		tempSubnet = re.split(r'\.',self.__subnet)
		broadcast = [0,0,0,0]
		
		for octet in range(len(tempGateway)):
			tempGatewayArray = self.decimaltoBinaryArray(tempGateway[octet])
			tempSubnetArray = self.decimaltoBinaryArray(tempSubnet[octet])
			broadcast[octet] = int("".join(str(x) for x in self.xnor(tempGatewayArray, tempSubnetArray)),2)
		return ".".join(str(x) for x in broadcast)
		
	#Each octet must be in the range of 0-255
	def inRange(self, ip):
		tempIP = re.split('\.',ip)
		for octet in range(len(tempIP)):
			if(int(tempIP[octet]) <= 0 | int(tempIP[octet]) > 255):
				return False
		return True
	
	def decimaltoBinaryArray(self,octet):
		octetArray = list(bin(int(octet))[2:].zfill(8))
		return octetArray
		
	def xnor(self,gateway, subnet):
		tempOctet = [0,0,0,0,0,0,0,0]
		for i in range(len(gateway)):
			if (gateway[i] == subnet[i]):
				tempOctet[i] = 1
		return tempOctet

	def andBinaryOperation(self,gateway,subnet):
		tempOctet = [0,0,0,0,0,0,0,0]
		for i in range(len(tempOctet)):
			if(gateway[i] == 1 & subnet[i] == 1):
				tempOctet[i] = 1
		return tempOctet
		
	#getOctetValue - Function returns after converting the bitwise & function of both integer but returns as a whole number.
	def getOctetValue(self,octet1, octet2):
		return int(octet1) & int(octet2)
	
	#getBorrowBitValue - function is to see how far of a bit it is require to borrow from the next class octet.
	def __getBorrowBitValue(self):
		if(self.__requireHosts != 0):
			#Cycling through the octets to see when the bit is bigger than the requiredHosts.
			for bit in range(1, 24):
				if(pow(2,bit) >= int(self.__requireHosts)):
					return bit
		return 0
		
	def __convertRequireToNetworkValue(self, value):
		comparisonList = ["128","192","224","240","248","252","254","255"]
		return comparisonList[value-1]
		
	def requireOctetRange(self):
		if(int(self.__requireBit) in range(1,8)):
			return 1
		elif(int(self.__requireBit) in range(9,16)):
			return 2
		else:
			return 3
			


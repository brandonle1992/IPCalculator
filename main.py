from IP import IP

def main():
	ip = input("Please type out the IP Address: ")
	subnetwork = input("Please enter the amount of subnetwork is required: ")
	
	test = IP(ip, subnetwork)
	print("Network : ",test.getNetwork())
	print("Subnet : ",test.getSubnet())
	print("Gateway : " ,test.getGateway())
	print("Broadcast : ", test.getBroadcast())
	
main()

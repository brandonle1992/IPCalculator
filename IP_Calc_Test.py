import unittest

from IP import IP

class IPTest(unittest.TestCase):
	def test_IP_Address(self):
		ip = "92.207.230.128"
		expected = "92.207.230.128"
		self.assertEqual(IP(ip,8).getIPAddress(), expected)
	def test_Subnet_Address(self):
		ip = "92.207.230.128"
		expected = "92.192.0.0"
		self.assertEqual(IP(ip,8).getNetwork(), expected)
	def test_Gateway_Address(self):
		ip = "92.207.230.128"
		expected = "92.223.255.255"
		self.assertEqual(IP(ip,8).getBroadcast(), expected)
	def test_leaking_type(self):
		ip = "10.69.241.37"
		network = "10.69.241.0"
		self.assertEqual(IP(ip,1048576).getNetwork(), network)


if __name__ == '__main__':
    unittest.main()

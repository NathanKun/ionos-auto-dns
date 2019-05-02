import requests
import socket
import script
import credentials

response = requests.get('https://api.ipify.org?format=json')
ip = response.json()['ip']

try:
	socket.inet_aton(ip)
	# legal
	session = script.login()
	script.changeARecord('catprogrammer.com', 'catserver.catprogrammer.com', ip, session)
	script.changeARecord('catprogrammer.com', 'dbkun.catserver.catprogrammer.com', ip, session)
	script.changeARecord('syzadele.com', 'syzadele.com', ip, session)
except socket.error:
	# not legal
	print('can not retrive a valid ip')
	print(response.content)


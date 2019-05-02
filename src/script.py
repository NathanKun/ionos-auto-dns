import sys
from bs4 import BeautifulSoup
import requests
import credentials


def changeARecord(domain: str, ip: str):
	# search
	print('searching...')
	response = session.get('https://my.ionos.fr/domain-dns-settings/catprogrammer.com?page.size=10&page.page=0&filter.host=' + domain + '&filter.search=A')

	bs = BeautifulSoup(response.text, 'html.parser')
	trs = bs.find('table', class_='content-table').tbody.find_all('tr', class_='enabled')
	
	for tr in trs:
		aTags = tr.find_all('a')
		if len(aTags) > 0:
			if aTags[0].string == 'A':
				record_id = tr.find_all('a')[2]['href'].split('/')[-1].split('?')[0]
				break;
	
	if 'record_id' not in locals():
		print('No A record found')
	else:
		# delete
		print('deleting ' + record_id + ' ...')
		session.post('https://my.ionos.fr/delete-dns-record/catprogrammer.com/' + record_id, {'__sendingdata': '1', 'delete.execute': 'true'})
	
	# add
	print('adding...')
	session.post('https://my.ionos.fr/add-dns-record/catprogrammer.com', {'__sendingdata': '1', 'record.forWwwSubdomain': 'true', 'record.type': 'A', 'record.host': domain.replace('.catprogrammer.com', ''), 'record.value': ip, 'record.ttl': '3600'})


def addTxtRecord(domain: str, textRecord: str):
	# add
	print('adding...')
	session.post('https://my.ionos.fr/add-dns-record/catprogrammer.com', {'__sendingdata': '1', 'record.forWwwSubdomain': 'true', 'record.type': 'TXT', 'record.host': domain.replace('.catprogrammer.com', ''), 'record.value': textRecord, 'record.ttl': '3600'})


def deleteTxtRecord(domain: str, textRecord: str):
	# search
	print('searching...')
	response = session.get('https://my.ionos.fr/domain-dns-settings/catprogrammer.com?page.size=10&page.page=0&filter.host=' + domain)
	
	bs = BeautifulSoup(response.text, 'html.parser')
	trs = bs.find('table', class_='content-table').tbody.find_all('tr', class_='enabled')
	
	for tr in trs:
		aTags = tr.find_all('a')
		if len(aTags) > 0:
			if aTags[0].string == 'TXT':
				record_id = tr.find_all('a')[2]['href'].split('/')[-1].split('?')[0]
				break;
	
	if 'record_id' not in locals():
		print('No TXT record found')
		sys.exit()
	
	# delete
	print('deleting ' + record_id + ' ...')
	session.post('https://my.ionos.fr/delete-dns-record/catprogrammer.com/' + record_id, {'__sendingdata': '1', 'delete.execute': 'true'})



# START
if len(sys.argv) != 4:
	print('Number of parameters not correct, must be 3: action {changeA, addTxt, deleteTxt}, domain, value')
	sys.exit()

script, p1, p2, p3 = sys.argv

if p1 != 'changeA' and p1 != 'addTxt' and p1 != 'deleteTxt':
	print('First parameter must be changeA, addTxt or deleteTxt')
	sys.exit()

print('Login...')
session = requests.session()  # 可以在多次访问中保留cookie
session.post('https://login.ionos.fr/', {'__lf':'Login', '__sendingdata': 1, 'oaologin.username': credentials.login, 'oaologin.password': credentials.password})

if p1 == 'changeA':
	print('changing A record of domain ' + p2 + ' to ' + p3)
	changeARecord(p2, p3)
elif p1 == 'addTxt':
	print('Adding TXT record to domain ' + p2 + ': ' + p3)
	addTxtRecord(p2, p3)
elif p1 == 'deleteTxt':
	print('Deleting TXT record to domain ' + p2 + ': ' + p3)
	deleteTxtRecord(p2, p3)

print('Finished')

	
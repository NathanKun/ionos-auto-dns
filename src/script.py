import sys
from bs4 import BeautifulSoup
import requests
import credentials


def login():
	print('Login...')
	session = requests.session()
	session.post('https://login.ionos.fr/', {'__lf':'Login', '__sendingdata': 1, 'oaologin.username': credentials.login, 'oaologin.password': credentials.password})
	return session

def changeARecord(root: str, domain: str, ip: str, session):
	# search
	url = 'https://my.ionos.fr/domain-dns-settings/' + root + '?page.size=10&page.page=0&filter.host=' + domain + '&filter.search=A'
	print('searching...')
	print(url)

	response = session.get(url)

	bs = BeautifulSoup(response.text, 'html.parser')
	trs = bs.find('table', class_='content-table').tbody.find_all('tr', class_='enabled')
	
	for tr in trs:
		aTags = tr.find_all('a')
		if len(aTags) > 0:
			if aTags[0].string == 'A':
				tdTags = tr.find_all('td')
				if domain.startswith(tdTags[1].string) and tdTags[2].string != ip:
					record_id = tr.find_all('a')[2]['href'].split('/')[-1].split('?')[0]
					break;
				elif domain.startswith(tdTags[1].string) and tdTags[2].string == ip:
					print('ip not changed')
					return
				elif tdTags[1].string == '@' and tdTags[2].string != ip:
					record_id = tr.find_all('a')[2]['href'].split('/')[-1].split('?')[0]
				elif tdTags[1].string == '@' and tdTags[2].string == ip:
					print('ip not changed')
					return
	
	if root == domain:
		print('updating domain ip ' + root)
		url = 'https://my.ionos.fr/edit-dns-record/' + root + '/' + record_id
		data = {'__sendingdata': '1', 'record.forWwwSubdomain': 'true', 'record.value': ip, 'record.ttl': '3600'}
		print(url)
		print(data)
		session.post(url, data)
	else:
		if 'record_id' not in locals():
			print('No A record found or domain not found')
		else:
			# delete
			print('deleting ' + record_id + ' ...')
			session.post('https://my.ionos.fr/delete-dns-record/' + root + '/' + record_id, {'__sendingdata': '1', 'delete.execute': 'true'})

		# add
		print('adding...')
		session.post('https://my.ionos.fr/add-dns-record/' + root, {'__sendingdata': '1', 'record.forWwwSubdomain': 'true', 'record.type': 'A', 'record.host': domain.replace('.' + root, ''), 'record.value': ip, 'record.ttl': '3600'})



def addTxtRecord(root: str, domain: str, textRecord: str):
	# add
	print('adding...')
	session.post('https://my.ionos.fr/add-dns-record/' + root, {'__sendingdata': '1', 'record.forWwwSubdomain': 'true', 'record.type': 'TXT', 'record.host': domain.replace('.' + root, ''), 'record.value': textRecord, 'record.ttl': '3600'})


def deleteTxtRecord(root: str, domain: str, textRecord: str):
	# search
	print('searching...')
	response = session.get('https://my.ionos.fr/domain-dns-settings/' + root + '?page.size=10&page.page=0&filter.host=' + domain)
	
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
	session.post('https://my.ionos.fr/delete-dns-record/' + root + '/' + record_id, {'__sendingdata': '1', 'delete.execute': 'true'})

if __name__ == '__main__' :
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

	if 'catprogrammer' in p2:
		root = 'catprogrammer.com'
	elif 'syzadele' in p2:
		root = 'syzadele.com'
	else:
		print('root of this domain is unknown: ' + p2)

	if p1 == 'changeA':
		print('changing A record of domain ' + p2 + ' to ' + p3)
		changeARecord(root, p2, p3, session)
	elif p1 == 'addTxt':
		print('Adding TXT record to domain ' + p2 + ': ' + p3)
		addTxtRecord(root, p2, p3)
	elif p1 == 'deleteTxt':
		print('Deleting TXT record to domain ' + p2 + ': ' + p3)
		deleteTxtRecord(root, p2, p3)

	print('Finished')


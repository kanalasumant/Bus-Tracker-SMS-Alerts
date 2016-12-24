from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#I use Twilio for SMS service
from twilio.rest import TwilioRestClient
import time

ACCOUNT_SID = "AC8a77e5606f86dfe67011bbd5a79115a1" 
AUTH_TOKEN = "92f76e07cd6d9c9cd6cca82865d8b9cd"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

'''
mySelect = Select(browser.find_element_by_id("routeSelector"))
mySelect.select_by_value("UT")

mySelect = Select(browser.find_element_by_id("stopSelector"))
s = [e for e in mySelect.options]

s[i].click()
t = browser.find_element_by_id("stopSelector")
t.text
'''
browser = webdriver.Chrome()
browser.get("http://bus-time.centro.org/bustime/eta/eta.jsp")
print('Select the appropriate number for your area: 1 --> {} , 2 --> {}, 3--> {}, 4--> {}, 5--> {}'.format('Oswego','Rome','Utica','Syracuse and SU','Auburn'))
area = input()
m = Select(browser.find_element_by_id('agencySelector'))
s = [e for e in m.options]
s[area].click()
time.sleep(2)

n = Select(browser.find_element_by_id('routeSelector'))
r = [e.text.encode() for e in n.options]
rf = [e for e in n.options]
print('Select the appropriate number for your route:')
for x,y in enumerate(r):
	print x+1,y

route = input()
rf[route-1].click()
time.sleep(2)

dir = Select(browser.find_element_by_id('directionSelector'))
t = [e.text.encode() for e in dir.options]
tf = [e for e in dir.options]
print('Select the appropriate direction to travel:')
for x,y in enumerate(t):
	print x+1,y

to = input()
tf[to-1].click()
time.sleep(2)

stop = Select(browser.find_element_by_id('stopSelector'))
u = [e.text.encode() for e in stop.options]
uf = [e for e in stop.options]
print('Select the appropriate direction to travel:')
for x,y in enumerate(u):
	print x+1,y

dest = input()
uf[dest-1].click()

wait = WebDriverWait(browser, 5)

while True:
	resp = wait.until(EC.presence_of_element_located((By.ID, 'time1')))
	#resp = browser.find_element_by_id('time1')
	j = resp.text.encode()
	if j == ' ': resp = wait.until(EC.presence_of_element_located((By.ID, 'noArrivals')))
	final = resp.text.encode()

	if j == ' ': client.messages.create(to = "+17327895282", from_ = "+18482307122", body = final)
	else:
		f = int(resp.text[:2].encode())
		if f<15: client.messages.create(to = "+17327895282", from_ = "+18482307122", body = "Hurry Up! The bus leaves in "+str(f)+ " minutes")
	time.sleep(10)
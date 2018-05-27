import requests
import time
import re


payload = {
    'login': '4144443',
    'password': 'Puriaso136531113355121',
}

url = 'https://zenitbet.com'

s = requests.sessions.Session()
s.headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
s.get(url)

r = s.post(url + "/login", data=payload)
if not '<a href="/logout" id="logout" target="_self">' in r.text:
    raise NameError("Invalid login or password")

s.get('https://zenitbet.com/live/view')

url = 'https://zenitbet.com/ajax/live/favourite/get_list/'+str(int(time.time()))

r = s.get(url)


sport = r.json()['result']['sport']['26']['league']
league = r.json()['result']['league']
games = r.json()['result']['games']
gamesId = []
res = ""


for i in sport:
	gamesId += league[str(i)]['games']

for g in gamesId:
	if (games[str(g)]['c_concat'][-4:] != ' угл'):

		res+= str(games[str(g)]['id']) + " " + games[str(g)]['c_concat'] + "\n"

with open('zenit_ids.txt', 'w') as f:
	f.write(res)



r = requests.get('http://sports.williamhill.com/bet/ru/betlive/9')

res = re.findall(r'\<span id=\"\d+\_mkt\_namespace\"\>.+\<\/span\>', str(r.text))

res = [i.replace('&nbsp;', ' ') for i in res]
res = [i.replace('<span id="', '') for i in res]
res = [i.replace('_mkt_namespace">', ' ') for i in res]
res = [i.replace('</span>', ' ') for i in res]
res = [re.sub(r'\ +', ' ', i) for i in res]

# <span id="12946408_mkt_namespace">Ozone &nbsp; v &nbsp;&nbsp;Hindustan</span>

with open('wh_ids.txt', 'w') as f:
	f.write("\n".join(res))
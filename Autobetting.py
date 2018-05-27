class Match():
    def __init__(self, id, zenit_id):
        self.id = id # wh id

        self.zenit_id = zenit_id

        self.homeBetData = {}
        self.awayBetData = {}
        self.betData = {}

        url = 'https://zenitbet.com'

        payload = {
            'login': '4144443',
            'password': 'Puriaso136531113355121',
        }

        self.s = requests.sessions.Session()
        self.s.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        self.s.get(url)
        
        r = self.s.post(url + "/login", data=payload)
        if not '<a href="/logout" id="logout" target="_self">' in r.text:
            raise NameError("Invalid login or password")

        self.s.get('https://zenitbet.com/live/view')

        self.getNewRoss()

    def getNewRoss(self):
        r = self.s.get('https://zenitbet.com/ajax/live/printer/js_line/'+str(int(time.time()))+'?ross=1&onlyview=0&all=0&print_mode=line&timezone=4&games='+str(self.getZenitId()))
        soup = bs(r.text, 'html5lib')
        tables = soup.find_all("table")

        for table in tables:
            trs = table.find_all("tr")
            for i in range(2, len(trs), 2):
                try:
                    ttt = trs[i].td.div.find_all('div')
                    for tt in ttt:
                        if '-й гол:' in str(tt):
                            ids = re.findall(r'(?<=b)\d+', str(tt))
                            if len(ids)<2:
                                self.getNewRoss()

                            self.setHomeBetData(ids[0])
                            self.setAwayBetData(ids[1])
                            return
                except Exception:
                    pass

    def getId(self):
        return self.id

    def getZenitId(self):
        return self.zenit_id

    def setZenitId(self, id):
        self.zenit_id = id

    def getZName(self):
        return self.zName

    def setHomeBetData(self, bid):
        r = self.s.post('https://zenitbet.com/ajax/live/bet/load', data={"bids[]":bid})
        gid = r.json()['result']['bets'][str(bid)]['gid']
        odd = r.json()['result']['bets'][str(bid)]['odd']
        d1 = r.json()['result']['bets'][str(bid)]['d1']
        d2 = r.json()['result']['bets'][str(bid)]['d2']
        cf = r.json()['result']['bets'][str(bid)]['cf']

        self.homeBetData = {
            'live': 1,
            'amount': 0,
            'type': 1,
            'system_type': "",
            'agree_cf': 1,
            'vip': 0,
            'promo_id':0,
            'odds['+str(gid)+'][gid]':gid,
            'odds['+str(gid)+'][id]':bid,
            'odds['+str(gid)+'][odd]':odd,
            'odds['+str(gid)+'][cf]':cf,
            'odds['+str(gid)+'][d1]':d1,
            'odds['+str(gid)+'][d2]':d2,
            'odds['+str(gid)+'][amount]': 5,
            'odds_order[]':gid,
        }

        print(r.json()['result']['dict']['odd'][str(odd)])

    def setAwayBetData(self, bid):
        r = self.s.post('https://zenitbet.com/ajax/live/bet/load', data={"bids[]":bid})
        gid = r.json()['result']['bets'][str(bid)]['gid']
        odd = r.json()['result']['bets'][str(bid)]['odd']
        d1 = r.json()['result']['bets'][str(bid)]['d1']
        d2 = r.json()['result']['bets'][str(bid)]['d2']
        cf = r.json()['result']['bets'][str(bid)]['cf']

        self.awayBetData = {
            'live': 1,
            'amount': 0,
            'type': 1,
            'system_type': "",
            'agree_cf': 1,
            'vip': 0,
            'promo_id':0,
            'odds['+str(gid)+'][gid]':gid,
            'odds['+str(gid)+'][id]':bid,
            'odds['+str(gid)+'][odd]':odd,
            'odds['+str(gid)+'][cf]':cf,
            'odds['+str(gid)+'][d1]':d1,
            'odds['+str(gid)+'][d2]':d2,
            'odds['+str(gid)+'][amount]': 5,
            'odds_order[]':gid,
        }

        print(r.json()['result']['dict']['odd'][str(odd)])

    def setBetData(self, bid):
        r = self.s.post('https://zenitbet.com/ajax/live/bet/load', data={"bids[]":bid})

        gid = r.json()['result']['bets'][str(bid)]['gid']
        odd = r.json()['result']['bets'][str(bid)]['odd']
        d1 = r.json()['result']['bets'][str(bid)]['d1']
        d2 = r.json()['result']['bets'][str(bid)]['d2']
        cf = r.json()['result']['bets'][str(bid)]['cf']

        self.betData = {
            'live': 1,
            'amount': 0,
            'type': 1,
            'system_type': "",
            'agree_cf': 1,
            'vip': 0,
            'promo_id':0,
            'odds['+str(gid)+'][gid]':gid,
            'odds['+str(gid)+'][id]':bid,
            'odds['+str(gid)+'][odd]':odd,
            'odds['+str(gid)+'][cf]':cf,
            'odds['+str(gid)+'][d1]':d1,
            'odds['+str(gid)+'][d2]':d2,
            'odds['+str(gid)+'][amount]': 5,
            'odds_order[]':gid,
        }

        print(r.json()['result']['dict']['odd'][str(odd)])
        
    def _doBet(self, data):
        r = self.s.post('https://zenitbet.com/ajax/dobet', data=data)
        print(r.json())

        # refresh data here
        self.getNewRoss()

        # print('pass')
        # pass

    def doHomeBet(self):
        self._doBet(self.homeBetData)

    def doAwayBet(self):
        self._doBet(self.awayBetData)

    def doBet(self):
        self._doBet(self.betData)


class Autobetting():
    def __init__(self):

        super(Autobetting, self).__init__()
        self.matches = []
        self.ws = websocket.WebSocket()

    def connectToWH(self):
        self.ws.connect("wss://whpush.williamhill.com/lsds/diffusion?ty=WB&v=9&ca=8&r=60000")
        self.ws.recv()
        for i in self.matches:
            self.ws.send("\x16scoreboards/v1/OB_EV" + str(i.getId()))
            self.ws.send("\x16scoreboards/v1/OB_EV" + str(i.getId()) + "/incidents")
         
        return self.ws  


    def addMatch(self, m):
        self.matches.append(m)
        self.ws.send("\x16scoreboards/v1/OB_EV" + str(m.getId()))
        self.ws.send("\x16scoreboards/v1/OB_EV" + str(m.getId()) + "/incidents")
        return True

    def getMatch(self, id):
        for i in self.matches:
            if i.getId() == id:
                return i
        return False

    def removeMatch(self, id=None, match=None):
        if match:
            if match in self.matches:
                self.matches.remove(match)
                return True
            else:
                return False

        elif id:
            match = self.getMatch(id)
            if match and match in self.matches:
                self.matches.remove(match)
                return True
            else:
                return False
        else:
            return False


def parseGoalByTeam(res):
    res = res.decode("utf8", errors="ignore")
    result = re.findall(r'G.?O.?A.?L[^_]', res)
  
    if len(result)>0 and len(res)<500 and len("".join(result))>=4:
        print(res)
        team = re.findall(r'(?<=teamType[^A-Z])[A-Z]+', res)
        for item in team:
            resTeam = re.findall(r'H.?O.?M.?E', item)
            if resTeam:
                return "HOME"
            resTeam = re.findall(r'A.?W.?A.?Y', item)
            if resTeam:
                return "AWAY"
    return None

def parseGoal(res):
    res = res.decode("utf8", errors="ignore")
    result = re.findall(r'G.?O.?A.?L[^_]', res)
  
    if len(result)>0 and len(res)<500 and len("".join(result))>=4:
        return True
    return None


if __name__ == '__main__':
    import websocket
    import re
    import requests
    import time
    from bs4 import BeautifulSoup as bs

    with open('input.txt', 'r') as f:
        string = f.read()
    arr = []

    for i in string.split('\n'):
        if len(i.split(" "))>1:
            arr.append(i.split(" "))

    sss = []

    for i in arr:
        match = Match(i[0], i[1])
        ab = Autobetting()
        ws = ab.connectToWH()
        ab.addMatch(match)

        sss.append([ws, match, ab])  
   

    print("Начинаю работу!\n")


    while True:
        for i in range(len(sss)):
            try:
                res = sss[i][0].recv()
                win = parseGoalByTeam(res)
                if win == "HOME":
                    sss[i][1].doHomeBet()
                if win == "AWAY":
                    sss[i][1].doAwayBet()


            except websocket._exceptions.WebSocketConnectionClosedException:
                sss[i][0] = sss[i][2].connectToWH()
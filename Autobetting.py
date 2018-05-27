class Match():
    def __init__(self, id, zenit_id):
        self.id = id # wh id

        self.zenit_id = zenit_id

        self.homeBetData = {}
        self.awayBetData = {}

        url = 'https://zenitbet.com'

        payload = {
            'login': LOGIN,
            'password': PASSWORD,
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

                            a = self.setHomeBetData(ids[0])

                            b = self.setAwayBetData(ids[1])

                            if not a or not b:
                                self.getNewRoss()


                            
                            return
                except Exception:
                    pass

    def getId(self):
        return self.id

    def getZenitId(self):
        return self.zenit_id

    def setZenitId(self, id):
        self.zenit_id = id


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
            'odds['+str(gid)+'][amount]': AMOUNT,
            'odds_order[]':gid,
        }

        print(r.json()['result']['dict']['odd'][str(odd)])
        return r.json()['result']['dict']['odd'][str(odd)]

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
            'odds['+str(gid)+'][amount]': AMOUNT,
            'odds_order[]':gid,
        }

        print(r.json()['result']['dict']['odd'][str(odd)])
        return r.json()['result']['dict']['odd'][str(odd)]

            
    def _doBet(self, data):
        r = self.s.post('https://zenitbet.com/ajax/dobet', data=data)
        print(r.json())

        # refresh data here
        self.homeBetData = {}
        self.awayBetData = {}

        print("Обновляю данные ставки для матча", str(self.getId()), str(self.getZenitId()))

        self.getNewRoss()


    def doHomeBet(self):
        self._doBet(self.homeBetData)

    def doAwayBet(self):
        self._doBet(self.awayBetData)



class Autobetting():
    def __init__(self):

        super(Autobetting, self).__init__()
        self.matches = []
        self.ws = websocket.WebSocket()

    def connectToWH(self):
        print("Reconnect...")
        self.ws.connect("wss://whpush.williamhill.com/lsds/diffusion?ty=WB&v=9&ca=8&r=60000")
        self.ws.recv()
        
        for i in self.matches:
            self.ws.send("\x16scoreboards/v1/OB_EV" + str(i.getId()) + "/incidents")
        
        print("Done!")
        return self.ws  


    def addMatch(self, m, new=False):
        self.matches.append(m)

        if new:
            self.ws.send("\x16scoreboards/v1/OB_EV" + str(m.getId()) + "/incidents")


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

    def startScanning(self):
        self.connectToWH()
        while 1:
            try:
                res = self.ws.recv()
                self.parse(res)

            except websocket._exceptions.WebSocketConnectionClosedException:
                self.connectToWH()


    def parse(self, res):
        res = str(res)
        t = re.findall(r'(?<=OB_EV\d{8}dtype.)[A-Z_\d]+', res)

        if len(t) == 0:
            return

        if 'STOP_GAME' in t:
            ids = re.findall(r'(?<=OB_EV)\d+', res)
            self.removeMatch(id=ids[0])
            return

        if t[0] == 'GOAL':

            ids = re.findall(r'(?<=OB_EV)\d+', res)
            team = re.findall(r'(?<=teamTyped)[A-Z]+', res)

            m = self.getMatch(ids[0])

            if team[0] == 'HOME':
                m.doHomeBet()
            if team[0] == 'AWAY':
                m.doAwayBet()
        

if __name__ == '__main__':
    import websocket
    import re
    import requests
    import time
    from bs4 import BeautifulSoup as bs

    AMOUNT = "5"
    LOGIN = "4144443"
    PASSWORD = "Puriaso136531113355121"



    with open('input.txt', 'r') as f:
        string = f.read()
    arr = []

    for i in string.split('\n'):
        if len(i.split(" "))>1:
            arr.append(i.split(" "))

    sss = []


    ab = Autobetting()

    for i in arr:
        match = Match(i[0], i[1])
        ab.addMatch(match)

   

    print("Начинаю работу!\n")
    ab.startScanning()


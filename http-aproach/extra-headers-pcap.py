from scapy.all import rdpcap, wrpcap, Ether, IP, TCP, Raw
from encoder import *

packets = rdpcap("../pcaps/pub/apt-installs.pcap")

modified_packets = []

l = 0

for pkt in packets:
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        payload = pkt[Raw].load

        if payload.startswith(b"GET") or payload.startswith(b"POST"):
            encoded_msg = space_encoding("nie mam juz kurwa sily")
            hidden_msg_payload = hide_in_spaces(payload.decode("utf-8"), encoded_msg)
            hidden_msg_payload = payload.decode("utf-8")
            if hidden_msg_payload.endswith("\r\n"):
                hidden_msg_payload = hidden_msg_payload[:-4]

            hidden_msg_payload += (
                "\nX-Hidden-Data: There is no hidden data in this extra headers\r\n"
            )
            hidden_msg_payload += (
                "X-Fake-Header: Artificial headers are not something strange\r\n"
            )
            hidden_msg_payload += "X-Ignore-This: Please move on this fake headers are not important at all\r\n"
            hidden_msg_payload += "X-Not-Important: Why are you still reading this\r\n"
            hidden_msg_payload += "X-Extra-Data: Some say space around the words is often more important the word themselves\r\n"
            hidden_msg_payload += "X-Testing-Purpose: If you are still here it means that you have lots of free time why don't you research whitespace-encoding topic for fun!\r\n"
            hidden_msg_payload += "\r\n"

            hidden_msg_payload.encode("utf-8")

            l += hidden_msg_payload.count(" ")

            pkt[Raw].load = hidden_msg_payload

            del pkt[Ether].len
            del pkt[IP].len
            del pkt[IP].chksum
            del pkt[TCP].chksum
            pkt.wirelen = len(pkt[Ether])

    modified_packets.append(pkt)

print(l)
# Write modified packets to new pcap file
wrpcap("output.pcap", modified_packets)

print("Modified pcap saved as output.pcap")

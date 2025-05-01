from encoder import *
from scapy.all import rdpcap, wrpcap, TCP, IP, Raw, Ether


def read_pkts(pcap_file):
    packets = rdpcap(pcap_file)
    return packets


def extract_http_requests(packets):
    http_requests = []

    for packet in packets:
        if IP in packet and TCP in packet:
            if packet[TCP].dport == 80:
                if packet[TCP].payload:
                    try:
                        http_payload = bytes(packet[TCP].payload).decode(
                            "utf-8", errors="ignore"
                        )
                        if http_payload.startswith("GET") or http_payload.startswith(
                            "POST"
                        ):
                            http_requests.append(packet)
                    except Exception as e:
                        print(f"Error decoding packet: {e}")

    return http_requests


def inject_extra_headers(packets, secret_msg):
    offsets = {}
    secret_pointer = 0

    for pkt in packets:
        if not (IP in pkt and TCP in pkt):
            continue

        tcp = pkt[TCP]
        ip = pkt[IP]

        flow_key = (ip.src, tcp.sport, ip.dst, tcp.dport)
        rev_key = (ip.dst, tcp.dport, ip.src, tcp.sport)

        if flow_key not in offsets:
            offsets[flow_key] = 0
        if rev_key not in offsets:
            offsets[rev_key] = 0

        seq_offset = offsets[flow_key]
        ack_offset = offsets[rev_key]
        tcp.seq += seq_offset
        tcp.ack += ack_offset

        if Raw in pkt and (
            pkt[Raw].load.startswith(b"GET") or pkt[Raw].load.startswith(b"POST")
        ):
            payload = pkt[Raw].load
            original_len = len(payload)
            payload = payload.decode("utf-8")

            http_requests = payload.split("\r\n\r\n")
            extra_headers = (
                "X-Hidden-Data: There is no hidden data in this extra headers\r\n"
                "X-Fake-Header: Artificial headers are not something strange\r\n"
                "X-Ignore-This: Please move on this fake headers are not important at all\r\n"
                "X-Not-Important: Why are you still reading this\r\n"
                "X-Extra-Data: Some say space around the words is often more important the word themselves\r\n"
                "X-Testing-Purpose: If you are still here it means that you have lots of free time why don't you research whitespace-encoding topic for fun!\r\n"
            )

            modified_requests = []
            for req in http_requests:
                req = req.strip()
                if req:
                    modified_request = req + "\r\n" + extra_headers + "\r\n"
                    modified_requests.append(modified_request)

            new_payload = "".join(modified_requests)
            new_payload, secret_index = hide_in_spaces(
                new_payload, secret_msg[secret_pointer:]
            )
            secret_pointer += secret_index + 1
            new_payload = new_payload.encode("utf-8")
            new_len = len(new_payload)

            pkt[Raw].load = new_payload
            offsets[flow_key] += new_len - original_len

            del pkt[Ether].len
            del pkt[IP].len
            del pkt[IP].chksum
            del pkt[TCP].chksum
            pkt.wirelen = len(pkt[Ether])

    return packets


def update_http_requests(http_requests):
    updated_requests = []
    for packet, request in http_requests:
        if "GET" in request or "POST" in request:
            encoded_msg = space_encoding("nie chce juz zyc")
            new_request = hide_in_spaces(request, encoded_msg)

            new_packet = packet.copy()
            new_packet[TCP].payload = new_request.encode("utf-8")

            updated_requests.append(new_packet)
    return updated_requests


def extract_http_payload(http_pkts):
    payloads = []
    for pkt in http_pkts:
        http_payload = bytes(pkt[TCP].payload).decode("utf-8", errors="ignore")
        payloads.append(http_payload)

    return payloads


def save_packets_to_pcap(packets, output_file):
    wrpcap(output_file, packets)

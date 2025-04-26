from scapy.all import rdpcap, TCP, IP


def extract_http_requests(pcap_file):
    # Read the packets from the PCAP file
    packets = rdpcap(pcap_file)

    http_requests = []

    for packet in packets:
        # Check if the packet has IP and TCP layers
        if IP in packet and TCP in packet:
            # Check if the packet contains HTTP data
            if packet[TCP].dport == 80:  # HTTP port
                # Check if the payload contains HTTP request
                if packet[TCP].payload:
                    # Decode the payload to get the HTTP request
                    try:
                        http_payload = bytes(packet[TCP].payload).decode(
                            "utf-8", errors="ignore"
                        )
                        if http_payload.startswith("GET") or http_payload.startswith(
                            "POST"
                        ):
                            http_requests.append(http_payload)
                    except Exception as e:
                        print(f"Error decoding packet: {e}")

    return http_requests


if __name__ == "__main__":
    pcap_file = (
        "./pcaps/pub/apt-install-python.pcap"  # Replace with your PCAP file path
    )
    http_requests = extract_http_requests(pcap_file)

    # Print the extracted HTTP requests
    for request in http_requests:
        print(request.count(" "))

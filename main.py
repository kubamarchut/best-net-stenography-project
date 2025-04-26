from scapy.all import rdpcap


def read_packets_from_file(filename):
    packets = rdpcap(filename)

    for i, packet in enumerate(packets[:5]):
        print(f"Packet #{i+1}:")
        print(packet.summary())
        print(packet.show(dump=True))  # Pretty detailed view
        print("=" * 50)


if __name__ == "__main__":
    filename = "pcaps/pub/apt-install-python.pcap"
    read_packets_from_file(filename)

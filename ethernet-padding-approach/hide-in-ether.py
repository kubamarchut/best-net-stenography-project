from scapy.all import rdpcap, wrpcap, Raw, Ether


def read_secret_from_file(filename):
    with open(filename, "r") as secret_file:
        text = secret_file.read()
        return text.encode()


def hide_data_in_padding(original_pcap, output_pcap, hidden_data: bytes):
    packets = rdpcap(original_pcap)
    modified_packets = []
    msg_pointer = 0

    for pkt in packets:
        if Ether not in pkt:
            continue

        pkt_len = len(pkt)
        min_eth_frame_len = 64

        if pkt_len < min_eth_frame_len:
            pad_len = min_eth_frame_len - pkt_len

            pad_bytes = (
                b"@"
                + hidden_data[msg_pointer : msg_pointer + (pad_len - 2)]
                + b"#"
                + b"\x00" * max(0, pad_len - len(hidden_data))
            )
            pkt = pkt / Raw(load=pad_bytes)
            msg_pointer += pad_len - 2
            pkt.wirelen = len(pkt[Ether])

        modified_packets.append(pkt)

    wrpcap(output_pcap, modified_packets)
    print(f"Modified PCAP saved as {output_pcap}")


# Example usage
secret_text = read_secret_from_file("../original_text/Sofokles-Antygona.txt")
hide_data_in_padding(
    "../pcaps/pub/apt-installs.pcap", "modified_with_hidden.pcap", secret_text
)

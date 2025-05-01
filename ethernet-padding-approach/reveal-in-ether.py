from scapy.all import rdpcap, Raw, Ether
import re


def extract_hidden_padding(pcap_file):
    retrieved_text = []
    retrieved_bytes = bytearray()
    packets = rdpcap(pcap_file)
    for i, pkt in enumerate(packets):
        if Ether not in pkt:
            continue

        if len(pkt[Ether]) == 64:
            payload = bytes(pkt[Ether])
            data = payload.rstrip(b"\x00")

            if data:
                decoded_data = data
                pattern = b"@([^@!]*)!"

                # Search for the pattern
                match = re.search(pattern, decoded_data)

                # Check if a match was found and print the result
                if match:
                    last_fragment = match.group(1)
                    retrieved_bytes += last_fragment

    return retrieved_bytes, retrieved_bytes.decode(errors="ignore")


retrieved_text = extract_hidden_padding("modified_with_hidden.pcap")

with open("retrieved.txt", "w", encoding="utf-8") as retrieved_file:
    retrieved_file.write(retrieved_text[1])

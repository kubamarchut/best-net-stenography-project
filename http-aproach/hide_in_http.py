from read_file import read_secret_from_file
from encoder import space_encoding
from http_editor import (
    read_pkts,
    extract_http_requests,
    inject_extra_headers,
    save_packets_to_pcap,
)

if __name__ == "__main__":
    secret_file = "../original_text/Sofokles-Antygona.txt"
    secret_text = read_secret_from_file(secret_file)

    print("secret text:", secret_text.decode()[:35].replace("\n", " "))

    encoded_text = space_encoding(str(secret_text)[2:-1])
    number_of_segment = len(encoded_text)

    print("number of segments:", number_of_segment)

    input_pcap_file = "../pcaps/pub/apt-installs.pcap"
    output_pcap_file = "./apt-installs-eh.pcap"
    packets = read_pkts(input_pcap_file)
    http_reqs = extract_http_requests(packets)

    print("http requests:", len(http_reqs))

    http_with_extra_headers = inject_extra_headers(packets, encoded_text)

    save_packets_to_pcap(http_with_extra_headers, output_pcap_file)

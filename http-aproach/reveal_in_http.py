from http_editor import read_pkts, extract_http_requests, extract_http_payload
from decoder import get_whitespace_between_words, space_decoding

if __name__ == "__main__":
    pcap_file = "./apt-installs-eh.pcap"
    packets = read_pkts(pcap_file)
    http_reqs = extract_http_requests(packets)

    print("http requests:", len(http_reqs))
    payloads = extract_http_payload(http_reqs)

    payload = "".join(payloads)
    spaces = get_whitespace_between_words(payload)
    revealed_msg = (
        space_decoding(spaces)
        .encode("utf-8")
        .decode("unicode_escape", errors="ignore")
        .encode("latin1")
        .decode("utf-8")
    )

    print(revealed_msg)

    """for payload in payloads:
        spaces = get_whitespace_between_words(payload)
        revealed_msg = (
            space_decoding(spaces)
            .encode("utf-8")
            .decode("unicode_escape")
            .encode("latin1")
            .decode("utf-8")
        )

        print(revealed_msg)"""

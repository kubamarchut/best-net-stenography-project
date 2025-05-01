import re

ZERO_REP = "  "
ONE_REP = "   "


def get_whitespace_between_words(text):
    spaces = re.findall(r" +", text)
    return spaces


def space_decoding(encoded_msg):
    binary_string = ""

    for space in encoded_msg:
        if space == ZERO_REP:
            binary_string += "0"
        elif space == ONE_REP:
            binary_string += "1"

    decoded_message = []

    for i in range(0, len(binary_string), 8):
        byte = binary_string[i : i + 8]
        if len(byte) == 8:
            ascii_value = int(byte, 2)
            decoded_message.append(chr(ascii_value))

    return "".join(decoded_message)

ZERO_REP = "  "
ONE_REP = "   "


def split_string(s, n):
    if n <= 0:
        raise ValueError("n must be a positive integer")

    length = len(s)
    k = length // n
    m = length % n

    parts = []
    start = 0
    for i in range(n):
        end = start + k + (1 if i < m else 0)
        parts.append(s[start:end])
        start = end

    return parts


def hide_in_spaces(text, hidden_msg):
    spaces_n = text.count(" ")

    text_with_hidden_msg = []
    for i in range(spaces_n):
        text_with_hidden_msg.append(text.split(" ")[i])
        if i < len(hidden_msg):
            text_with_hidden_msg.append(hidden_msg[i])

    text_with_hidden_msg.append(text.split(" ")[-1])
    print(i)
    return "".join(text_with_hidden_msg), i


def space_encoding(text):
    encoded_msg = []
    for char in text:
        ascii_value = ord(char)
        binary_rep = bin(ascii_value)[2:]
        for bit in binary_rep.zfill(8):
            if bit == "0":
                encoded_msg.append(ZERO_REP)
            else:
                encoded_msg.append(ONE_REP)

    return encoded_msg


if __name__ == "__main__":
    encoded_msg = space_encoding("life")

    print("encoded msg:", "\t".join(encoded_msg).split("\t"), len(encoded_msg))

    original_text = "Lorem Ipsum to typ tekstu zastępczego powszechnie używanego w branży projektowej i wydawniczej do wypełnienia przestrzeni na stronie."

    hidden_msg = hide_in_spaces(original_text, encoded_msg)

    print(hidden_msg)

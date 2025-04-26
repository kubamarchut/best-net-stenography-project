def split_string(s, n):
    if n <= 0:
        raise ValueError("n must be a positive integer")

    length = len(s)
    k = length // n  # Length of each part
    m = length % n  # Remainder (number of parts that need an extra character)

    parts = []
    start = 0
    for i in range(n):
        end = start + k + (1 if i < m else 0)  # Add 1 if there are remaining characters
        parts.append(s[start:end])
        start = end  # Update start for the next part

    return parts


def hide_in_spaces(text, hidden_msg):
    spaces_n = text.count(" ")
    hidden_msg = "\t".join(hidden_msg)

    parts = split_string(hidden_msg, spaces_n)

    msg_with_hidden_msg = []
    for i in range(spaces_n):
        msg_with_hidden_msg.append(text.split(" ")[i])
        msg_with_hidden_msg.append(parts[i])

    msg_with_hidden_msg.append(text.split(" ")[-1])

    return "".join(msg_with_hidden_msg)


def space_encoding(text):
    encoded_msg = []
    for char in text:
        ascii_value = ord(char)
        binary_string = format(ascii_value, "08b")
        for digit in binary_string:
            if digit == "0":
                encoded_msg.append(" ")
            else:
                encoded_msg.append("  ")

    return encoded_msg


if __name__ == "__main__":
    encoded_msg = space_encoding("life")

    print("encoded msg:", "\t".join(encoded_msg).split("\t"), len(encoded_msg))

    original_text = "Lorem Ipsum to typ tekstu zastępczego powszechnie używanego w branży projektowej i wydawniczej do wypełnienia przestrzeni na stronie."

    hidden_msg = hide_in_spaces(original_text, encoded_msg)

    print(hidden_msg)

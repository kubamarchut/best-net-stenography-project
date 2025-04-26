def hide_in_spaces(text, hidden_msg):
    spaces_n = text.count(" ")
    print(spaces_n)


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
    encoded_msg = space_encoding("nie lubie kuby")

    print("encoded msg:", encoded_msg, len(encoded_msg))

    original_text = "Lorem Ipsum to typ tekstu zastępczego powszechnie używanego w branży projektowej i wydawniczej do wypełnienia przestrzeni na stronie."

    hide_in_spaces(original_text, encoded_msg)

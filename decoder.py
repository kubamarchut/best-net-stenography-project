def get_whitespace_between_words(text):
    # Initialize a list to hold the whitespace segments
    whitespace_segments = []

    # Split the text into words
    words = text.split()

    # Initialize the start index for the first word
    start_index = 0

    # Iterate through the words to find the whitespace between them
    for word in words:
        # Find the index of the current word in the original text
        word_index = text.find(word, start_index)

        # If this is not the first word, get the whitespace before it
        if start_index != 0:
            whitespace = text[start_index:word_index]
            whitespace_segments.append(whitespace)

        # Update the start index for the next iteration
        start_index = word_index + len(word)

    return whitespace_segments


def space_decoding(encoded_msg):
    # Initialize an empty string to hold the binary representation
    binary_string = ""

    # Iterate through the encoded message
    for space in encoded_msg:
        if space == " ":
            binary_string += "0"  # Single space represents '0'
        elif space == "  ":
            binary_string += "1"  # Double space represents '1'

    # Now we need to convert the binary string to characters
    decoded_message = []

    # Process the binary string in chunks of 8 (1 byte)
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i : i + 8]
        if len(byte) == 8:  # Ensure we have a full byte
            ascii_value = int(byte, 2)  # Convert binary to decimal
            decoded_message.append(chr(ascii_value))  # Convert to character

    return "".join(decoded_message)


if __name__ == "__main__":
    from encoder import *

    encoded_msg = space_encoding("BEST")

    original_text = "Lorem Ipsum to typ tekstu zastępczego powszechnie używanego w branży projektowej i wydawniczej do wypełnienia przestrzeni na stronie."

    hidden_msg = hide_in_spaces(original_text, encoded_msg)

    print(hidden_msg)

    whitespaces = get_whitespace_between_words(hidden_msg)

    hidden_msg_2 = "".join(whitespaces).split("\t")
    decoded_msg = space_decoding(hidden_msg_2)

    print(decoded_msg)

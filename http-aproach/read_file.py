def read_secret_from_file(filename):
    with open(filename, "r") as secret_file:
        text = secret_file.read()
        return text.encode("utf-8")

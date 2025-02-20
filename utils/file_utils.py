def read_file(path):
    # Open and read the file
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    # Print content
    # print(content)
    return content
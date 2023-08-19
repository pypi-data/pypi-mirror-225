def read_file(file):
    try:
        with open(file, encoding="utf8") as f:
            text = f.read()
    except:
        text = ""
    return text

def write_file(file, text):
    with open(file, "w", encoding="utf8") as f:
        f.write(text)

def read_binary_file(file):
    try:
        with open(file, "rb") as f:
            bytes_value = f.read()
    except:
        bytes_value = None
    return bytes_value
    
def write_binary_file(file, bytes_value):
    with open(file, "wb") as f:
        f.write(bytes_value)

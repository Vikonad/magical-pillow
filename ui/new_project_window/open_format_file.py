from json import load

def open_file():
    with open("config/formats.json") as data:
        data = load(data)
    return data

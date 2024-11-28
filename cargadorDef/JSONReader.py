import json
from json import JSONDecodeError

def get_data():
    try:
        f = open('data.json')
        data = json.load(f)
        return data
    except JSONDecodeError:
        data = get_data()
        return data
    


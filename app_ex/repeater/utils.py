import requests


def random_number(max_, min_, num):
    data = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": "ddcdd8bd-09a0-44e9-bb09-cb49010a80ba",
            "n": num,
            "min": min_,
            "max": max_,
            "replacement": True,
            "base": 10
        },
        "id": 1
    }
    r = requests.post(url="https://api.random.org/json-rpc/1/invoke", json=data)
    return r.json()["result"]["random"]["data"]


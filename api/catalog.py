import json


def execute():
    with open("catalog_catalog.json", "r") as w:
        json_data = json.load(w)
    return json_data

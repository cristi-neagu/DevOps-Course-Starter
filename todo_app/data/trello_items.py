import os
import json
import requests

def get_items():
    url = f'https://api.trello.com/1/boards/{os.environ.get("TRELLO_BOARD")}/lists'
    headers = {"Accept": "application/json"}
    query = {'cards': 'open', 'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}

    response = requests.request("GET", url, headers=headers, params=query, timeout=10)

    lists = json.loads(response.text)
    items = []

    for cList in lists:
        if cList['name'] == 'To Do':
            for card in cList['cards']:
                items.append({'id': card['idShort'], 'status': 'Not Started', 'title': card['name']})
        if cList['name'] == 'Doing':
            for card in cList['cards']:
                items.append({'id': card['idShort'], 'status': 'Started', 'title': card['name']})

    return items

def get_item(id):
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)

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

def add_item(title):
    # First need to get the ID of the lists
    url = f'https://api.trello.com/1/boards/{os.environ.get("TRELLO_BOARD")}/lists'
    headers = {"Accept": "application/json"}
    query = {'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}

    response = requests.request("GET", url, headers=headers, params=query, timeout=10)
    lists = {entry['name']: entry['id'] for entry in json.loads(response.text)}

    # Now add the new item to the To Do list
    url = "https://api.trello.com/1/cards"

    headers = {"Accept": "application/json"}
    query = {'idList': lists['To Do'], 'name': title,
             'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}

    response = requests.request("POST", url, headers=headers, params=query, timeout=10)
    newCard = json.loads(response.text)

    return {'id': newCard['id'], 'status': 'Not Started', 'title': newCard['name']}

def save_item(item):
    url = f'https://api.trello.com/1/boards/{os.environ.get("TRELLO_BOARD")}/lists'
    headers = {"Accept": "application/json"}
    query = {'cards': 'open', 'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}

    response = requests.request("GET", url, headers=headers, params=query, timeout=10)

    lists = json.loads(response.text)
    listIDs = {entry['name']: entry['id'] for entry in lists}
    cards = []
    for cList in lists:
        for card in cList['cards']:
            cards.append(card)
    cardID = -1
    for card in cards:
        if card['idShort'] == item['id']:
            cardID = card['id']

    if cardID == -1:
        return item

    url = f'https://api.trello.com/1/cards/{cardID}'
    headers = {"Accept": "application/json"}
    query = {'name': item['title'], 'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}
    query['idList'] = listIDs['Doing'] if item['status'] == 'Started' else listIDs['To Do']

    response = requests.request("PUT", url, headers=headers, params=query, timeout=10)
    return item

def delete_item(id):
    url = f'https://api.trello.com/1/boards/{os.environ.get("TRELLO_BOARD")}/lists'
    headers = {"Accept": "application/json"}
    query = {'cards': 'open', 'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}

    response = requests.request("GET", url, headers=headers, params=query, timeout=10)

    lists = json.loads(response.text)
    cards = []
    for cList in lists:
        for card in cList['cards']:
            cards.append(card)
    cardID = -1
    for card in cards:
        if card['idShort'] == int(id):
            cardID = card['id']

    if cardID == -1:
        return

    url = f'https://api.trello.com/1/cards/{cardID}'
    headers = {"Accept": "application/json"}
    query = {'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}

    response = requests.request("DELETE", url, headers=headers, params=query, timeout=10)
    print('done')

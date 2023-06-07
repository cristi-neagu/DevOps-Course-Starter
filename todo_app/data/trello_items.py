import os
import json
import requests
from todo_app.data.ToDoItem import TDItem

def getItems():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    url = f'https://api.trello.com/1/boards/{os.environ.get("TRELLO_BOARD")}/lists'
    headers = {"Accept": "application/json"}
    query = {'cards': 'open', 'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}

    response = requests.request("GET", url, headers=headers, params=query, timeout=10)

    lists = json.loads(response.text)
    items = []

    # For now let's just add all items sorted according to status and then by ID
    # If needed, we can sort by ID later
    for cList in lists:
        if cList['name'] not in ['To Do', 'Doing']:
            continue
        for card in cList['cards']:
            items.append(TDItem.fromTrelloCards(card, cList))

    return items

def getItem(itemID):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = getItems()
    return next((item for item in items if item.id == int(itemID)), None)

def addItem(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    # First need to get the ID of the lists
    url = f'https://api.trello.com/1/boards/{os.environ.get("TRELLO_BOARD")}/lists'
    headers = {"Accept": "application/json"}
    query = {'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}

    response = requests.request("GET", url, headers=headers, params=query, timeout=10)
    lists = {entry['name']: entry['id'] for entry in json.loads(response.text)}

    # Now add the new item to the To Do list
    # Can also check in the future if the item is Doing, and choose the appropriate list
    url = "https://api.trello.com/1/cards"

    headers = {"Accept": "application/json"}
    query = {'idList': lists['To Do'], 'name': title,
             'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}

    response = requests.request("POST", url, headers=headers, params=query, timeout=10)
    newCard = json.loads(response.text)

    return {'id': newCard['id'], 'status': 'To Do', 'title': newCard['name']}

def saveItem(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
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
        if card['idShort'] == item.id:
            cardID = card['id']

    if cardID == -1:
        return item

    url = f'https://api.trello.com/1/cards/{cardID}'
    headers = {"Accept": "application/json"}
    query = {'name': item.name, 'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}
    query['idList'] = listIDs['Doing'] if item.status == 'Doing' else listIDs['To Do']

    response = requests.request("PUT", url, headers=headers, params=query, timeout=10)
    return item

def deleteItem(itemID):
    """
    Deletes and existing item in the session. If no existing item matches the ID of the specified item, nothing is deleted.

    Args:
        id: The ID of the item to delete.
    """
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
        if card['idShort'] == int(itemID):
            cardID = card['id']

    if cardID == -1:
        return

    url = f'https://api.trello.com/1/cards/{cardID}'
    headers = {"Accept": "application/json"}
    query = {'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}

    response = requests.request("DELETE", url, headers=headers, params=query, timeout=10)
    print('done')

def completeItem(itemID):
    """
    Marks an item as complete and moves it to the Done list. If no existing item matches the ID of the specified item, nothing is deleted.

    Args:
        id: The ID of the item to mark as complete.
    """
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
        if card['idShort'] == int(itemID):
            cardID = card['id']

    if cardID == -1:
        return

    url = f'https://api.trello.com/1/cards/{cardID}'
    headers = {"Accept": "application/json"}
    query = {'idList': listIDs['Done'], 'key': os.environ.get("TRELLO_KEY"), 'token': os.environ.get("TRELLO_TOKEN")}

    response = requests.request("PUT", url, headers=headers, params=query, timeout=10)
    return itemID

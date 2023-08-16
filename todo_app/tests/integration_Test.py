import pytest
import requests
import os
import json
from dotenv import load_dotenv, find_dotenv
from todo_app import app

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    filePath = find_dotenv('.env.testing')
    load_dotenv(filePath, override=True)

    # Create the new app.
    testApp = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with testApp.test_client() as client:
        yield client

def testIndexPage(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', stub)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()

class StubResponse():
    def __init__(self, fakeResponseData):
        self.fakeResponseData = fakeResponseData
        self.text = json.dumps(self.fakeResponseData)

    def json(self):
        return self.fakeResponseData

def stub(reqType, url, **kwargs):
    # Not sure why this isn't working...
    # test_board_id = os.environ.get('TRELLO_BOARD_ID')
    testBoardID = 'TestTrelloBoard'
    if url == f'https://api.trello.com/1/boards/{testBoardID}/lists':
        fakeResponseData = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'Test card', 'idShort': '0'}]
            }]
        return StubResponse(fakeResponseData)
    raise Exception(f'Integration test did not expect URL "{url}"')

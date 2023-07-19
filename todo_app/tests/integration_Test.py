import pytest
import requests
import os
from dotenv import load_dotenv, find_dotenv
from todo_app import app

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    testApp = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with testApp.test_client() as testClient:
        yield testClient

def testIndexPage(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', stub)
    response = client.get('/')

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

def stub(url, params={}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'Test card'}]
            }]
        return StubResponse(fake_response_data)
    raise Exception(f'Integration test did not expect URL "{url}"')

import os
import pytest
import dotenv

from mouse_book_2_client import client as _client


dotenv.load_dotenv()

try:
    API_BASE = os.environ['API_BASE']
except KeyError:
    raise Exception('API_BASE environment variable not set.')

@pytest.fixture
def client():
    return _client.Client(API_BASE, "")

MOUSE_RECORD = {
    "id": 1,
    "labtracks_id": 999999,
    "age": 80 * 60 * 60 * 24,  # ms
    "state": "tissue cyte",
    "status": 0,  # 0 = not started, 1 = started, 2 = finished
    "created_at": 100000,
    "updated_at": 100000,
}

@pytest.mark.order(1)
def test_post(client):
    response = client.post('/items', data=MOUSE_RECORD)
    assert response.status_code == 201


@pytest.mark.order(2)
def test_get(client):
    response = client.get('/books')
    assert response.status_code == 200


# @pytest.mark.order(3)
# def test_update(client):
#     response = client.update('/books/1', data={'title': 'Updated Book'})
#     assert response.status_code == 200


# @pytest.mark.order(4)
# def test_delete(client):
#     response = client.delete('/books/1')
#     assert response.status_code == 204
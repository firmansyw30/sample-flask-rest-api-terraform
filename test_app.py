# test_app.py
from flask.testing import FlaskClient
import pytest
import json
from app import app, books

@pytest.fixture(autouse=True)
def clear_books():
    # Ensure fresh state for each test
    books.clear()
    yield
    books.clear()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client: FlaskClient):
    res = client.get('/')
    assert res.status_code == 200
    assert res.is_json
    assert res.get_json() == {"message": "Welcome to Flask API"}

def test_get_books_empty(client: FlaskClient):
    res = client.get('/books')
    assert res.status_code == 200
    assert res.is_json
    assert res.get_json() == {"books": []}

def test_create_book_valid(client: FlaskClient):
    payload = {"title": "1984", "author": "George Orwell"}
    res = client.post('/books', json=payload)
    assert res.status_code == 201
    assert res.is_json
    body = res.get_json()
    assert body["id"] == 0
    assert body["title"] == payload["title"]
    assert body["author"] == payload["author"]
    # Ensure storage mutated
    assert len(books) == 1
    assert books[0]["id"] == 0

def test_create_book_invalid_json(client: FlaskClient):
    # send invalid JSON body
    res = client.post('/books', data="not-json", content_type='application/json')
    assert res.status_code == 400
    assert res.is_json
    assert res.get_json() == {"message": "Invalid JSON input"}

def test_get_book_by_id(client: FlaskClient):
    # create then retrieve
    client.post('/books', json={"title": "Dune", "author": "Frank Herbert"})
    res = client.get('/books/0')
    assert res.status_code == 200
    assert res.is_json
    assert res.get_json() == {"book": {"id": 0, "title": "Dune", "author": "Frank Herbert"}}

def test_get_book_not_found(client: FlaskClient):
    res = client.get('/books/999')
    assert res.status_code == 404
    assert res.is_json
    assert res.get_json() == {"message": "Book not found"}

def test_update_book(client: FlaskClient):
    client.post('/books', json={"title": "Old", "author": "Author"})
    res = client.put('/books/0', json={"title": "New Title", "author": "New Author"})
    assert res.status_code == 200
    assert res.is_json
    assert res.get_json() == {"book": {"id": 0, "title": "New Title", "author": "New Author"}}
    assert books[0]["title"] == "New Title"

def test_update_book_not_found(client: FlaskClient):
    res = client.put('/books/999', json={"title": "X"})
    assert res.status_code == 404
    assert res.is_json
    assert res.get_json() == {"message": "Book not found"}

def test_delete_book(client: FlaskClient):
    client.post('/books', json={"title": "A", "author": "AA"})
    client.post('/books', json={"title": "B", "author": "BB"})
    assert len(books) == 2
    res = client.delete('/books/0')
    assert res.status_code == 200
    assert res.is_json
    assert res.get_json() == {"message": "Book deleted"}
    assert len(books) == 1
    assert books[0]["id"] == 1

def test_404_error_handler(client: FlaskClient):
    res = client.get('/this-route-does-not-exist')
    assert res.status_code == 404
    assert res.is_json
    assert res.get_json() == {"message": "Route not found"}

def test_500_error_handler(client: FlaskClient):
    # dynamically add a route that raises to trigger the 500 error handler
    def boom():
        raise RuntimeError("boom")

    app.add_url_rule('/cause500', 'cause500', boom)
    try:
        res = client.get('/cause500')
        assert res.status_code == 500
        assert res.is_json
        assert res.get_json() == {"message": "Internal server error"}
    finally:
        # remove the rule to avoid side effects for other tests
        app.view_functions.pop('cause500', None)
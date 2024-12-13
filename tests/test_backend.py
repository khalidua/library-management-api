import pytest
from flask import Flask
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_books(client):
    response = client.get('/library/Books')
    assert response.status_code == 200
    assert b"Bayn al-Qasrayn" in response.data  # Ensure the response contains a book title

def test_get_book_by_isbn(client):
    response = client.get('/library/Books/9781')
    assert response.status_code == 200
    assert b"Bayn al-Qasrayn" in response.data  # Ensure the correct book is returned

def test_add_book(client):
    new_book = {
        "Title": "New Book",
        "Author": "New Author",
        "Published Year": "2024"
    }
    response = client.post('/library/Books', json=new_book)
    assert response.status_code == 201
    assert b"New Book" in response.data 
    assert b"New Author" in response.data  

def test_update_book(client):
    updated_data = {
        "Title": "Updated Book Title",
        "Author": "Updated Author",
        "Published Year": "2025"
    }
    response = client.put('/library/Books/9781', json=updated_data)
    assert response.status_code == 200
    assert b"Updated Book Title" in response.data
    assert b"Updated Author" in response.data


def test_delete_book(client):
    response = client.delete('/library/Books/9781')
    assert response.status_code == 200
    assert b"Book got deleted" in response.data 

def test_search_books_by_author(client):
    response = client.get('/library/search?Author=Naguib Mahfouz')
    assert response.status_code == 200
    assert b"Bayn al-Qasrayn" in response.data

def test_search_books_by_year(client):
    response = client.get('/library/search?Published%20Year=2002')
    assert response.status_code == 200
    assert b"Imarat Yaqubian" in response.data

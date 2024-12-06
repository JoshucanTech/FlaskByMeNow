from flask_jwt_extended import create_access_token

def test_get_books(client):
    """
    Test fetching books.
    """
    response = client.get('/api/books/all')
    assert response.status_code == 401  # Should fail without authentication



def test_get_books(client):
    """
    Test fetching books.
    """
    response = client.get('/api/books')
    assert response.status_code == 200  # Should succed without authentication



def test_add_book(client):
    """
    Test adding a new book.
    """
    # Create a user and get a token
    client.post('/api/register', json={
        "username": "testuser",
        "password": "testpass"
    })
    response = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    token = response.json['access_token']

    # Add a book
    response = client.post('/api/books', json={
        "title": "Test Book",
        "author": "Test Author"
    }, headers={"Authorization": f"Bearer {token}"})  # Use the token for authentication

    # Check that the book was added successfully
    assert response.status_code == 201  # HTTP status 201 Created
    assert "id" in response.json  # The response should contain the book ID
    assert response.json["title"] == "Test Book"  # Check the title
    assert response.json["author"] == "Test Author"  # Check the author

def test_update_book(client):
    """
    Test updating a book.
    """
    # First, add a book
    response = client.post('/api/register', json={
        "username": "testuser",
        "password": "testpass"
    })
    response = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    token = response.json['access_token']

    add_response = client.post('/api/books', json={
        "title": "Test Book",
        "author": "Test Author"
    }, headers={"Authorization": f"Bearer {token}"})
    
    book_id = add_response.json["id"]  # Get the ID of the newly added book

    # Now update the book
    response = client.put(f'/api/books/{book_id}', json={
        "title": "Updated Test Book"
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200  # HTTP status 200 OK
    assert response.json["title"] == "Updated Test Book"  # Check updated title

def test_delete_book(client):
    """
    Test deleting a book.
    """
    # First, add a book
    response = client.post('/api/register', json={
        "username": "testuser",
        "password": "testpass"
    })
    response = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    token = response.json['access_token']

    add_response = client.post('/api/books', json={
        "title": "Test Book",
        "author": "Test Author"
    }, headers={"Authorization": f"Bearer {token}"})
    
    book_id = add_response.json["id"]  # Get the ID of the newly added book

    # Now delete the book
    response = client.delete(f'/api/books/{book_id}', headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200  # HTTP status 200 OK
    assert response.json["message"] == "Book deleted"  # Check delete confirmation

def test_register_user(client):
    """
    Test user registration.
    """
    response = client.post('/api/register', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 201
    assert response.json['message'] == "User registered"

def test_login_user(client):
    """
    Test user login and token generation.
    """
    # Register a user first
    client.post('/api/register', json={
        "username": "testuser",
        "password": "testpass"
    })

    # Login the user
    response = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json

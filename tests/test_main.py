def test_users_requires_login(client):
    response = client.get('/users', follow_redirects=True)
    assert b'Login' in response.data

def login(client, username, password):
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

def test_users_authenticated(client, sample_users):
    login(client, 'dj', 'password')
    response = client.get('/users')
    assert b'dj' in response.data
    assert b'admin' in response.data

def test_get_user(client, sample_users):
    login(client, 'dj', 'password')
    response = client.get('/user/1')
    assert b'admin' in response.data
    assert b'Logged in as dj' in response.data
    response = client.get('/user/2')
    assert b'dj' in response.data
    assert b'admin ' not in response.data

def test_update_user(client, sample_users):
    login(client, 'dj', 'password')
    response = client.get('/user/2')
    assert b'Edit Profile' in response.data
    response = client.post('/user/2', data={'username': 'dj42'})
    assert b'User updated successfully' in response.data
    assert b'dj42' in response.data
    response = client.post('/user/2', data={'username': 'dj'})
    assert b'User updated successfully' in response.data
    assert b'dj42' not in response.data
    assert b'dj' in response.data

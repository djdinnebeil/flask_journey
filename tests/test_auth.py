def test_register(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpass'
    }, follow_redirects=True)
    assert b'Login' in response.data or b'Profile' in response.data

def test_login_valid(client, sample_users):
    response = client.post('/login', data={
        'username': 'dj',
        'password': 'password'
    }, follow_redirects=True)
    assert b'dj' in response.data

def test_login_invalid(client):
    response = client.post('/login', data={
        'username': 'wrong',
        'password': 'nope'
    })
    assert b'Invalid username or password' in response.data

def test_user_already_exists(client, sample_users):
    client.post('/login', data={
        'username': 'dj',
        'password': 'password'
    } )
    response = client.post('/user/2', data={
        'username': 'admin',
    })
    assert b'Username already taken' in response.data

def test_register_user_already_exists(client, sample_users):
    response = client.post('/register', data={
        'username': 'dj',
        'password': 'password'
    }, follow_redirects=True)
    assert b'Username already taken' in response.data

def test_login_invalid_password(client, sample_users):
    response = client.post('/login', data={
        'username': 'dj',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b'Invalid username or password' in response.data
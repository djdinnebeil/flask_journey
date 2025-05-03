def test_ban_requires_admin(client, sample_users):
    # Log in as regular user
    client.post('/login', data={'username': 'dj', 'password': 'password'})
    response = client.get('/admin/ban/1', follow_redirects=True)
    assert b'You do not have permission' in response.data or b'Login' in response.data

def test_admin_can_ban(client, sample_users):
    client.post('/login', data={'username': 'admin', 'password': 'admin'})
    response = client.get('/admin/ban/2')
    assert b'User has been banned' in response.data

def test_admin_dashboard(client, sample_users):
    client.post('/login', data={'username': 'admin', 'password': 'admin'})
    response = client.get('/admin/dashboard')
    assert b'Welcome to the Admin Dashboard' in response.data
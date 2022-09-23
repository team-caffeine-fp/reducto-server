import json

def test_home(api):
    resp = api.get('/')
    assert resp.status == '200 OK'
    assert b'hello, welcome to reducto server' in resp.data

def test_users(api):
    resp = api.get('/users/')
    assert resp.status == '200 OK'
    assert b'showing all users' in resp.data

def test_dashboard(api):
    resp = api.get('/dashboard/')
    assert resp.status == '200 OK'
    assert b'the month' in resp.data

def test_login(api):
    resp = api.post('/login/')
    assert resp.status == '200 OK'
    assert b'thanks for logging in' in resp.data

def test_register(api):
    form_data = {'username': 'regtest', 'bname': 'regbusiness'}
    resp = api.post('/register/', data=form_data)
    assert resp.status == '200 OK'
    assert b'Thanks for registering' in resp.data

def test_form(api):
    form_data = {'username': "test", 'category': 'travel flights', 'co2': 5000}
    resp = api.put('/form/', data=form_data)
    assert resp.status == '200 OK'
    assert b'User updated' in resp.data
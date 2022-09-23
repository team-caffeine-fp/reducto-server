import json

def test_home(api):
    resp = api.get('/')
    assert resp.status == '200 OK'

def test_users(api):
    resp = api.get('/users/')
    assert resp.status == '200 OK'

def test_dashboard(api):
    resp = api.get('/dashboard/')
    assert resp.status == '200 OK'

def test_login(api):
    resp = api.post('/login/')
    assert resp.status == '200 OK'

def test_register(api):
    form_data = {'username': 'regtest', 'bname': 'regbusiness'}
    resp = api.post('/register/', data=form_data)
    assert resp.status == '200 OK'

def test_form(api):
    form_data = {'username': "test", 'category': 'travel flights', 'co2': 5000}
    resp = api.put('/form/', data=form_data)
    assert resp.status == '200 OK'
from werkzeug.security import check_password_hash

def test_unauthorized(client):
	user_id = client.application.config['user_id']

	response = client.get(f'/users/{str(user_id)}')

	assert response.status_code == 401
	assert b'error' in response.data
	assert b'Invalid credentials.' in response.data


def test_readsuccess(client):
	response = client.post('/auth/login', json={
		'username': 'edis',
		'password': 'edis'
	})

	token = response.json['token']
	user_id = client.application.config['user_id']

	response = client.get(f'/users/{str(user_id)}', headers={
		'Authorization': f'Bearer {token}'
	})

	assert response.status_code == 200
	assert b'username' in response.data
	assert b'businessname' in response.data
	assert b'email' in response.data
	assert b'edis' in response.data


def test_updateusername(client):
	response = client.post('/users', json={
		'username': 'mike',
		'password': 'mike',
		'businessname': 'Mike Mercieca',
		'email': 'mikemercieca@example.com'
	})

	response = client.post('/auth/login', json={
		'username': 'edis',
		'password': 'edis'
	})

	token = response.json['token']
	user_id = client.application.config['user_id']

	response = client.put(f'/users/{str(user_id)}', headers={
		'Authorization': f'Bearer {token}'
	}, json={
		'username': 'mike'
	})

	assert response.status_code == 400
	assert b'error' in response.data
	assert b'Username already exists.' in response.data


def test_updatesuccess(client):
	response = client.post('/auth/login', json={
		'username': 'edis',
		'password': 'edis'
	})

	token = response.json['token']
	user_id = client.application.config['user_id']

	response = client.put(f'/users/{str(user_id)}', headers={
		'Authorization': f'Bearer {token}'
	}, json={
		'name': 'Emin Edis',
		'password': 'emin'
	})

	assert response.status_code == 200
	assert b'name' in response.data
	assert b'Emin Edis' in response.data
	assert b'password' in response.data
	assert check_password_hash(response.json['password'], 'emin')


def test_deletesuccess(client):
	response = client.post('/users', json={
		'username': 'ionna',
		'password': 'ionna',
		'businessname': 'Ionna',
		'email': 'ionna@example.com'
	})
	user_id = response.json['_id']

	response = client.post('/auth/login', json={
		'username': 'ionna',
		'password': 'ionna'
	})

	token = response.json['token']

	response = client.delete(f'/users/{str(user_id)}', headers={
		'Authorization': f'Bearer {token}'
	})

	assert response.status_code == 200


def test_deletefail(client):
	response = client.post('/users', json={
		'username': 'ionna',
		'password': 'ionna',
		'businessname': 'Ionna',
		'email': 'ionna@example.com'
	})
	user_id = response.json['_id']

	response = client.post('/auth/login', json={
		'username': 'ionna',
		'password': 'ionna'
	})

	token = response.json['token']

	response = client.delete(f'/users/{str(user_id)}', headers={
		'Authorization': f'Bearer {token}'
	})

	assert response.status_code == 200

	response = client.delete(f'/users/{str(user_id)}', headers={
		'Authorization': f'Bearer {token}'
	})

	assert response.status_code == 401
	assert b'error' in response.data
	assert b'Invalid credentials.' in response.data


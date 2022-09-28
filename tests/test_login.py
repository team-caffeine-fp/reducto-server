def test_badrequest(client):
	response = client.post('/auth/login',
		json={}
	)

	assert response.status_code == 400
	assert b'error' in response.data
	assert b'Missing fields.' in response.data


def test_baduser(client):
	response = client.post('/auth/login',
		json={
			'username': 'asdf',
			'password': 'edis'
		}
	)

	assert response.status_code == 400
	assert b'error' in response.data
	assert b'Username does not exist.' in response.data


def test_badpassword(client):
	response = client.post('/auth/login',
		json={
			'username': 'edis',
			'password': 'asdf'
		}
	)

	assert response.status_code == 400
	assert b'error' in response.data
	assert b'Password is incorrect.' in response.data


def test_success(client):
	response = client.post('/auth/login',
		json={
			'username': 'edis',
			'password': 'edis'
		}
	)

	assert response.status_code == 200
	assert b'token' in response.data


def test_logoutsuccess(client):
	response = client.post('/auth/login',
		json={
			'username': 'edis',
			'password': 'edis'
		}
	)

	print(response.data)

	assert response.status_code == 200
	assert b'token' in response.data

	token = response.json['token']

	response = client.post('/auth/logout',
		headers={
			'Authorization': f'Bearer {token}'
		}
	)

	print(response.data)

	assert response.status_code == 200



def test_logoutfail(client):
	response = client.post('/auth/login',
		json={
			'username': 'edis',
			'password': 'edis'
		}
	)

	assert response.status_code == 200
	assert b'token' in response.data

	token = response.json['token']

	response = client.post('/auth/logout',
		headers={
			'Authorization': f'Bearer {token}'
		}
	)

	assert response.status_code == 200

	response = client.post('/auth/logout',
		headers={
			'Authorization': f'Bearer {token}'
		}
	)

	assert response.status_code == 401

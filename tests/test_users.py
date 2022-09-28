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


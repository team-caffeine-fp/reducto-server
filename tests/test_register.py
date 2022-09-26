def test_badrequest(client):
	response = client.post('/users',
		json={}
	)

	assert response.status_code == 400
	assert b'error' in response.data
	assert b'Missing fields.' in response.data


def test_userexists(client):
	response = client.post('/users',
		json={
			'username': 'edis',
			'password': 'edis',
			'businessname': 'edis',
			'email': 'edis@hotmail.com'
		}
	)

	assert response.status_code == 400
	assert b'error' in response.data
	assert b'Username already exists.' in response.data

def test_success(client):
	response = client.post('/users',
		json={
			'username': 'jason',
			'password': 'jason',
			'businessname': 'Jason Brooks',
			'email': 'jasonbrooks@example.com'
		}
	)

	assert response.status_code == 200
	assert b'username' in response.data
	assert b'businessname' in response.data
	assert b'email' in response.data
	assert b'jason' in response.data




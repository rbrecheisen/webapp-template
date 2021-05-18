import requests


def test_user_can_create_user_account():
    result = requests.post('http://127.0.0.1:8000/users/', json={'user': 'ralph', 'password': 'foobar'})
    assert result.status_code == 201
    # Check that creating user that already exists returns 403
    result = requests.post('http://127.0.0.1:8000/users/', json={'user': 'ralph', 'password': 'foobar'})
    assert result.status_code == 403


def test_user_can_login():
    result = requests.post('http://127.0.0.1:8000/tokens/', json={'user': 'ralph', 'password': 'foobar'})
    assert result.status_code == 201
    assert 'token' in result.json().keys()

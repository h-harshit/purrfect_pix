import os
import sys
from fastapi.testclient import TestClient

# appending parent dir path to sys.path to make import from parent dir possible
current_path = os.path.dirname(__file__)
parent_dir_path = os.path.abspath(os.path.join(current_path, '..'))
sys.path.append(parent_dir_path)

from main import app

client = TestClient(app)

def test_signup():
	test_signup_payload = {
		"username": "testuser",
		"email": "test@user.com",
		"password": "testpassword"
	}

	signup_response = client.post("/api/v1/auth/signup", data=test_signup_payload)
	assert signup_response.status_code == 200
	assert signup_response.json()["created_user"]["username"] == "testuser"
	assert signup_response.json()["created_user"]["email"] == "test@user.com"

def login():
	test_user_payload = {"username": "testuser", "password": "testpassword"}
	auth_response = client.post("/api/v1/auth/login", data=test_user_payload)
	token = auth_response.json()["access_token"]
	return auth_response, token

def test_login():
	auth_response, token = login()
	assert auth_response.status_code == 200
	assert token is not None

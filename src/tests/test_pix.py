import os
import sys
import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient
from test_auth import login
from config import config

# appending parent dir path to sys.path to make import from parent dir possible
current_path = os.path.dirname(__file__)
parent_dir_path = os.path.abspath(os.path.join(current_path, '..'))
sys.path.append(parent_dir_path)

from main import app
from data_client import get_mongo_collection

client = TestClient(app)

def get_one_img_id():
	mongo_pics_collection = get_mongo_collection(
		config.DB_NAME, config.PICS_COLLECTION_NAME)
	
	img_result = mongo_pics_collection.find_one()
	img_id = img_result["img_id"]
	return img_id

@pytest.mark.serial
def test_upload_pic():
	auth_response, auth_token = login()
	assert auth_response.status_code == 200
	headers = {
		"Authorization": f"Bearer {auth_token}"
	}

	filename = "./tests/pics/cat.png"

	with open(filename, "rb") as img_file:
		upload_response = client.post("/api/v1/pix/file/upload",
			files={"file":("cat.png", img_file, "image/png")}, headers=headers)
	
	assert upload_response.status_code == 200
	assert upload_response.json()["msg"] == "Upload Successful"
	assert upload_response.json()["file_name"] == "cat.png"

@pytest.mark.serial
def test_download_pic():
	auth_response, auth_token = login()
	assert auth_response.status_code == 200
	headers = {
		"Authorization": f"Bearer {auth_token}"
	}

	img_id = get_one_img_id()
	print(img_id)

	response = client.get(f"/api/v1/pix/file/download/{img_id}", headers=headers)

	assert response.status_code == 200
	assert "image/jpeg" in response.headers["content-type"] or \
			"image/png" in response.headers["content-type"] or \
			"image/webp" in response.headers["content-type"]

@pytest.mark.serial
def test_delete_pic():
	auth_response, auth_token = login()
	assert auth_response.status_code == 200
	headers = {
		"Authorization": f"Bearer {auth_token}"
	}

	img_id = get_one_img_id()

	response = client.delete(f"/api/v1/pix/file/delete/{img_id}", headers=headers)

	assert response.status_code == 200
	assert response.json()["msg"] == "Deleted Successfully"
	assert response.json()["img_id"] == img_id

@pytest.mark.serial
def test_update_pic():
	auth_response, auth_token = login()
	assert auth_response.status_code == 200
	headers = {
		"Authorization": f"Bearer {auth_token}"
	}

	filename = "./tests/pics/update_cat.webp"
	img_id = get_one_img_id()

	with open(filename, "rb") as img_file:
		update_response = client.patch(f"/api/v1/pix/file/update/{img_id}",
			files={"file":("update_cat.webp", img_file, "image/webp")}, headers=headers)

	assert update_response.status_code == 200
	assert update_response.json()["msg"] == "Updated Successfully"
	assert update_response.json()["img_id"] == img_id

	



	




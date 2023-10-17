
import os.path
from PIL import Image
from io import BytesIO
from uuid import uuid4
from data_client import get_container_client
from fastapi import status, HTTPException, UploadFile
from datetime import datetime
from data_client import get_mongo_collection, get_container_client
from .serializers import NewPicsMetadataSerializer, PicsMetadataSerializer, PicsMetadataListSerializer
from config import config
from typing import Union
import time
from pymongo.collection import ReturnDocument

# picking default credentials
container_client = get_container_client()

mongo_pics_collection = get_mongo_collection(
	config.DB_NAME, config.PICS_COLLECTION_NAME)


def validate_file_content(file: UploadFile) -> bool:
	content_type = file.content_type
	valid_content_types = ['image/jpeg', 'image/png', 'image/webp']
	if content_type not in valid_content_types:
		raise HTTPException(
			status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
			detail = "Invalid upload type! Only jpg, png and webp files are supported"
		)

def get_image_bytes_data(file):
	img = Image.open(file.file)
	img_bytes = BytesIO()
	img.save(img_bytes, format="JPEG")
	img_bytes.seek(0)
	img_data = img_bytes.read()
	return img_data

def create_adls_file_name(filename: str, username: str) -> str:
	unique_id = str(int(time.time()))
	img_id = f"{username}_{unique_id}"
	_, file_ext = os.path.splitext(filename)
	adls_filename = f"{img_id}{file_ext}"
	return img_id, adls_filename

def upload_pics_to_adls(file_name, img_data, overwrite=True):
	try:
		blob_client = container_client.get_blob_client(file_name)
		res = blob_client.upload_blob(img_data, overwrite=overwrite)
		return res
	except Exception as err:
		raise HTTPException(
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail = f"Image upload unsuccessful"
		)

def get_img_file_from_adls(adls_filename: str):
	blob_client = container_client.get_blob_client(adls_filename)
	file_stream = blob_client.download_blob().readall()
	return file_stream

def delete_img_on_adls(adls_filename: str):
	try:
		blob_client = container_client.get_blob_client(adls_filename)
		blob_client.delete_blob()
	except Exception as err:
		raise HTTPException(
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail = f"Image deletion unsuccessful"
		)


def upload_pics_metadata(
	username: str,
	file_path: str,
	filename: str,
	img_id: str,
	created_at: Union[datetime, None]=None,
	updated_at: Union[datetime, None]=None,
	deleted_at: Union[datetime, None]=None
):
	metadata_dict = {
		'username': username,
		'file_path': file_path,
		'filename': filename,
		'img_id': img_id,
	}

	try:
		new_pic = NewPicsMetadataSerializer(metadata_dict)
		result = mongo_pics_collection.insert_one(new_pic)
		inserted_id = result.inserted_id

		uploaded_pic_dict = mongo_pics_collection.find_one({'_id': inserted_id})
		uploaded_pic = PicsMetadataSerializer(uploaded_pic_dict)
		
		return uploaded_pic

	except Exception as err:
		raise HTTPException(
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail = f"Image meta data upload unsuccessful"
		)

def get_pics_metadata_list(username: str):
	result = mongo_pics_collection.find({'username': username})
	img_list = PicsMetadataListSerializer(result)
	return img_list

def get_img_metadata(username: str, img_id:str):
	query_filter = {
		"username": username,
		"img_id": img_id
	}

	result = mongo_pics_collection.find_one(query_filter)
	return result

def delete_img_metadata(username: str, img_id: str):
	query_filter = {
		"username": username,
		"img_id": img_id
	}

	deleted_img = mongo_pics_collection.find_one_and_delete(query_filter)
	return deleted_img

def update_img_metadata(username: str, img_id: str, filename: str, adls_filename: str):
	filter_query = {
		"username": username,
		"img_id": img_id
	}

	update_payload = {
		"file_path": adls_filename,
		"filename": filename,
		"updated_at": datetime.now()
	}

	try:
		updated_pic = mongo_pics_collection.find_one_and_update(
			filter_query, {'$set': update_payload}, return_document=ReturnDocument.AFTER)
		return updated_pic
	except Exception as err:
		raise HTTPException(
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail = f"Image meta data update unsuccessful"
		)

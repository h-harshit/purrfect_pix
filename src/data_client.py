from config import config
from pymongo.database import Database
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def get_mongo_client(
	mongo_uri:str = config.MONGO_URI,
	server_api: ServerApi = ServerApi(config.SERVER_API_VERSION)
) -> MongoClient:
	mongo_client = MongoClient(mongo_uri)
	return mongo_client


def get_mongo_db(db_name: str) -> Database:
	mongo_client = get_mongo_client(config.MONGO_URI)
	return mongo_client[db_name]

def get_mongo_collection(db_name: str, collection: str) -> Collection:
	mongo_db = get_mongo_db(db_name)
	return mongo_db[collection]


def get_blob_service_client(
	storage_account_name: str=config.STORAGE_ACCOUNT_NAME,
	storage_account_key: str=config.STORAGE_ACCOUNT_KEY,
	container_name: str=config.CONTAINER_NAME
):
	blob_service_client = BlobServiceClient(
		account_url=f"https://{storage_account_name}.blob.core.windows.net",
		credential=storage_account_key,
	)

	return blob_service_client


def get_container_client(
	storage_account_name: str=config.STORAGE_ACCOUNT_NAME,
	storage_account_key: str=config.STORAGE_ACCOUNT_KEY,
	container_name: str=config.CONTAINER_NAME
):
	blob_service_client = get_blob_service_client(
		storage_account_name,
		storage_account_key,
		container_name
	)
	container_client = blob_service_client.get_container_client(container_name)

	return container_client
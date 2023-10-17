import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
	DB_NAME: str = os.environ["DB_NAME"]
	USER_COLLECTION_NAME: str = os.environ["USER_COLLECTION_NAME"]
	PICS_COLLECTION_NAME: str = os.environ["PICS_COLLECTION_NAME"]
	MONGO_URI: str = os.environ["MONGO_URI"]
	SERVER_API_VERSION: str = os.environ["SERVER_API_VERSION"]

	# secure secret key generated using openssl
	SECRET_KEY: str = os.environ["SECRET_KEY"]
	ALGORITHM: str = os.environ["ALGORITHM"]
	ACCESS_TOKEN_EXPIRES_MINUTES: int = int(os.environ["ACCESS_TOKEN_EXPIRES_MINUTES"])

	STORAGE_ACCOUNT_NAME: str = os.environ["STORAGE_ACCOUNT_NAME"]
	STORAGE_ACCOUNT_KEY: str = os.environ["STORAGE_ACCOUNT_KEY"]
	CONTAINER_NAME: str = os.environ["CONTAINER_NAME"]

	TOKEN_URL: str = os.environ["TOKEN_URL"]

config = Settings()

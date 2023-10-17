from jose import jwt
from typing import Union
from config import config
from .schemas import User, UserInDB
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pymongo.collection import Collection
from fastapi import status, HTTPException
from data_client import get_mongo_collection
from .serializers import UserSerializer, NewUserSerializer


mongo_user_collection = get_mongo_collection(
	config.DB_NAME, config.USER_COLLECTION_NAME)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) -> bool:
	return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
	return pwd_context.hash(password)

def get_user(username: str) -> Union[UserInDB, None]:	
	query_filter = {
		"username": username
	}

	user = mongo_user_collection.find_one(query_filter)
	if user is not None:
		user_dict = user
		return UserInDB(**user_dict)

def create_access_token(data:dict, expires_delta: Union[timedelta, None] = None) -> str:
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRES_MINUTES)
	to_encode.update({"exp":expire})
	encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm = config.ALGORITHM)
	return encoded_jwt

def register_user_in_db(
	username: str,
	password: str,
	email: str
) -> dict:

	user_dict = {
		'username': username,
		'password': password,
		'email': email
	}

	try:
		new_user = NewUserSerializer(user_dict)
		result = mongo_user_collection.insert_one(new_user)
		inserted_id = result.inserted_id
	except Exception as err:
		raise HTTPException(
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail = "User registration not successfull"
		)

	created_user_dict = mongo_user_collection.find_one({'_id': inserted_id})
	created_user = UserSerializer(created_user_dict)
	
	
	return created_user

def authenticate_user(username:str, password:str) -> UserInDB:
	user = get_user(username)
	if not user:
		return False
	if not verify_password(password, user.password):
		return False
	return user




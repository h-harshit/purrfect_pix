from datetime import datetime
from pydantic import BaseModel
from typing import Union, List
from bson.objectid import ObjectId

class User(BaseModel):
	username: str
	email: Union[str, None] = None
	created_at: datetime = datetime.now() 
	updated_at: Union[datetime, None] = datetime.now()
	deleted_at: Union[datetime, None] = None

	class Config:
		from_attributes = True
		arbitrary_types_allowed = True
		json_encoders = {ObjectId: str}

class UserInDB(User):
	password: str

class NewUser(BaseModel):
	status_code: int
	created_user: User

class AuthToken(BaseModel):
	access_token: str
	token_type: str

class AuthTokenData(BaseModel):
	username: Union[str, None] = None
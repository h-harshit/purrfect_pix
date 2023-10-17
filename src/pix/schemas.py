from pydantic import BaseModel
from typing import Union, List
from bson.objectid import ObjectId
from datetime import datetime

class Status(BaseModel):
	msg: str
	status_code:int
	img_id:str
	file_name: str

class PicsMetaData(BaseModel):
	username: str
	file_path: str
	img_id: str
	created_at: Union[datetime, None]=None
	updated_at: Union[datetime, None]=None
	deleted_at: Union[datetime, None]=None

	class Config:
		from_attributes = True
		arbitrary_types_allowed = True
		json_encoders = {ObjectId: str}

class ListPics(BaseModel):
	status_code: int
	username: str
	images: List[dict] = []
from datetime import datetime

def UserSerializer(user) -> dict:
	return {
		"username": user["username"],
		"email": user["email"],
		"created_at": user["created_at"],
		"updated_at": user["updated_at"],
		"deleted_at": user["deleted_at"]
  	}

def NewUserSerializer(user) -> dict:
	# avoiding circular imports
	from .utils import get_password_hash

	created_at = datetime.now()
	return {
		"username": user["username"],
		"email": user["email"],
		"password": get_password_hash(user["password"]),
		"created_at": created_at,
		"updated_at": created_at,
		"deleted_at": None
	}
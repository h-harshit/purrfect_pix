from config import config
from datetime import timedelta
from .schemas import NewUser, AuthToken
from fastapi import APIRouter, HTTPException, status, Depends
from .dependencies import OAuth2SignupRequestForm, OAuth2PasswordRequestForm
from .utils import get_user, register_user_in_db, authenticate_user, create_access_token

router = APIRouter()

@router.post("/signup", response_model=NewUser)
async def signup(form_data: OAuth2SignupRequestForm = Depends()):
	username = form_data.username
	email = form_data.email
	password = form_data.password

	user_exists = get_user(username)
	if user_exists:
		raise HTTPException(
			status_code = status.HTTP_409_CONFLICT,
			detail = "User already exists!"
		)
	
	new_user = register_user_in_db(username, password, email)

	response =  { 
		"status_code":status.HTTP_201_CREATED,
		"created_user": new_user
	}

	return NewUser(**response)

@router.post("/login", response_model=AuthToken)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
	# formdata should contain 'username' and 'password' as per OAuth2 specification
	user = authenticate_user(form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code = status.HTTP_401_UNAUTHORIZED,
			detail = "Incorrect username or password",
			headers = {"WWW-Authenticate": "Bearer"}
		)

	access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRES_MINUTES)
	access_token = create_access_token(
		data={"sub":user.username}, expires_delta = access_token_expires
	)

	response =  {"access_token": access_token, "token_type": "bearer"}
	return AuthToken(**response)



from config import config
from .utils import get_user
from typing import Annotated
from jose import JWTError, jwt
from fastapi.param_functions import Form
from .schemas import User, AuthTokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import  HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

class OAuth2SignupRequestForm:
	'''This is a custom dependency class similar to 
	
	OAuth2PasswordRequestForm to create following form
	request params in the endpoint:

	username: username string,
	email: email string
	password: password string
	'''

	def __init__(
		self,
		*,
		username:Annotated[str, Form()],
		email: Annotated[str, Form()],
		password: Annotated[str, Form()]
	):
		self.username = username
		self.email = email
		self.password = password



oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.TOKEN_URL)

async def get_current_user(token: str = Depends(oauth2_scheme)):
	credentials_exception = HTTPException(
		status_code = status.HTTP_401_UNAUTHORIZED,
		detail = "Could not validate credentials",
		headers = {"WWW-Authenticate": "Bearer"}
	)
	try:
		payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
		# JWT specification has "sub" as Subject (in this case username) of the token
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception
		token_data = AuthTokenData(username=username)
	except JWTError:
		raise credentials_exception
  
	user = get_user(username = token_data.username)
	if user is None:
		raise credentials_exception
	return user






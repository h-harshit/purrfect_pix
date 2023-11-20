import json
from io import BytesIO
from auth.schemas import User
from .schemas import Status, ListPics
from auth.dependencies import get_current_user
from .utils import *
from fastapi import UploadFile, APIRouter
from fastapi.responses import StreamingResponse
from fastapi import  HTTPException, status, Depends


router = APIRouter()

@router.post("/file/upload", response_model=Status)
async def upload_pic(file: UploadFile, current_user: User = Depends(get_current_user)):
	'''Upload a cat pic

	- **Args**:<br>
		- **file**: cat image file with jpg, png or webp content
	
	- **Returns**:<br>
		- **msg**: "Upload Successful"<br>
		- **status_code**: Status code<br>
		- **img_id**: unique image id for uploaded image<br>
		- **file_name**: file name for uploaded image<br>

	'''
	# file content should include jpg, png or webp
	validate_file_content(file)

	filename = file.filename
	img_id, adls_filename = create_adls_file_name(filename, current_user.username)
	
	img_data = get_image_bytes_data(file)

	# upload file as a blob to Azure Data Lake Storage Gen2
	adls_res = upload_pics_to_adls(adls_filename, img_data)

	if adls_res is None:
		raise HTTPException(
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail = f"Image upload unsuccessful"
		)
		
	# upload metadata related to uploaded file to mongodb
	uploaded_pic = upload_pics_metadata(
		current_user.username,
		adls_filename,
		filename,
		img_id,
	)
		
	response = {
		"status_code": status.HTTP_201_CREATED,
		"msg": "Upload Successful",
		"img_id": img_id,
		"file_name": filename
	}

	return Status(**response)

@router.get("/file/download/{img_id}")
async def download_pic(img_id: str, current_user: User = Depends(get_current_user)):
	'''Download a cat pic.

	- **Args**:<br>
		- **img_id**: image id for which image is to be downloaded

	- **Returns**: <br>
		- Streaming File Response
	'''
	img_metadata = get_img_metadata(current_user.username, img_id)
	if img_metadata is None:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = f"No image with img_id: {img_id} found"
		)

	adls_filename = img_metadata["file_path"]
	file_stream = get_img_file_from_adls(adls_filename)
	# StreamingResponse for dynamically generated file responses
	return StreamingResponse(BytesIO(file_stream), media_type="image/jpeg")
		

@router.delete("/file/delete/{img_id}", response_model=Status)
async def delete_pic(img_id: str, current_user: User = Depends(get_current_user)):
	'''Delete a cat pic

	- **Args**:<br>
		- **img_id**: image id of the file to be deleted
	
	- **Returns**:<br>
		- **msg**: "Deleted Successfully"<br>
		- **status_code**: Status code<br>
		- **img_id**: unique image id for deleted image<br>
		- **file_name**: file name for deleted image<br>

	'''
	result = delete_img_metadata(current_user.username, img_id)
	if result is None:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = f"No image with img_id: {img_id} found"
		)

	adls_filename = result["file_path"]
	delete_img_on_adls(adls_filename)

	response = {
		"status_code": status.HTTP_200_OK,
		"msg": "Deleted Successfully",
		"img_id": img_id,
		"file_name": result["filename"]
	}

	return Status(**response)

@router.patch("/file/update/{img_id}", response_model=Status)
async def update_pic(img_id: str, file: UploadFile, current_user: User = Depends(get_current_user)):
	'''Update a cat pic

	- **Args**:<br>
		- **img_id**: image id of the file to be updated
	
	- **Returns**:<br>
		- **msg**: "Updated Successfully"<br>
		- **status_code**: Status code<br>
		- **img_id**: unique image id for updated image<br>
		- **file_name**: file name for updated image<br>

	'''
	validate_file_content(file)
	filename = file.filename

	img_metadata = get_img_metadata(current_user.username, img_id)
	if img_metadata is None:
		raise HTTPException(
			status_code = status.HTTP_400_BAD_REQUEST,
			detail = f"No image with img_id: {img_id} found"
		)
	
	adls_filename = img_metadata["file_path"]
	result = update_img_metadata(current_user.username, img_id, filename, adls_filename)
	
	img_data = get_image_bytes_data(file)
	# updating images in adls in place with same filepath
	adls_res = upload_pics_to_adls(adls_filename, img_data, overwrite=True)

	if adls_res is None:
		raise HTTPException(
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail = f"Image update unsuccessful"
		)
	
	response =  {
		"status_code": status.HTTP_200_OK,
		"msg": "Updated Successfully",
		"img_id": img_id,
		"file_name": filename
	}

	return Status(**response)

@router.get("/file/list", response_model=ListPics)
async def get_images_list(current_user: User = Depends(get_current_user)):
	'''Get image list for the user

	- **Returns**:<br>
		- **status_code**: status_code,<br>
		- **username**: username,<br>
		- List[
				{
					"username": username,
					"img_id": image id,
					"filename": filename
				}
			]
	'''
	username = current_user.username
	list_images = get_pics_metadata_list(username)

	response = {
		"status_code": status.HTTP_200_OK,
		"username": username,
		"images": list_images
	}

	return ListPics(**response)









	


	
	
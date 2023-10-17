from datetime import datetime
from typing import List

def NewPicsMetadataSerializer(pics_metadata) -> dict:
	created_at = datetime.now()
	return {
		"username": pics_metadata["username"],
		"file_path": pics_metadata["file_path"],
		"filename": pics_metadata["filename"],
		"img_id": pics_metadata["img_id"],
		"created_at": created_at,
		"updated_at": created_at,
		"deleted_at": None
	}

def PicsMetadataSerializer(pics_metadata) -> dict:
	created_at = datetime.now()
	return {
		"username": pics_metadata["username"],
		"img_id": pics_metadata["img_id"],
		"filename": pics_metadata["filename"]
	}

def PicsMetadataListSerializer(pics_metadata_list) -> List[dict]:
	return [PicsMetadataSerializer(metadata) for metadata in pics_metadata_list]


import base64
import uuid
from typing import Dict, List
from datetime import datetime

from app.schemas.permission import PermissionIn, PermissionOut
from app.services.permission import PermissionService
from fastapi import APIRouter, Depends, status, File, UploadFile
import os
from sqlalchemy.ext.asyncio import AsyncSession
import shutil
from app.db import get_session

router = APIRouter(tags=["Permission"], prefix="/permission")


@router.post("/create_permission", status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission_data: PermissionIn,
    session: AsyncSession = Depends(get_session),
):
    return await PermissionService.create_permissions(permission_data, session)

@router.get("/get_permission_by_id/{permission_id}", status_code=status.HTTP_200_OK)
async def get_permission_by_id(
    permission_id: int,
    session: AsyncSession = Depends(get_session),
) -> PermissionOut:
    return await PermissionService.get_permissions_by_id(permission_id, session)


@router.get("/get_all", status_code=status.HTTP_200_OK)
async def get_all_permissions(session: AsyncSession = Depends(get_session)) -> list[PermissionOut]:
    return await PermissionService.get_all_permissions(session)


@router.delete("/delete_by_id/{permission_id}", status_code=status.HTTP_200_OK)
async def delete_permission_by_id(
    permission_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await PermissionService.delete_permission_by_id(permission_id, session)



@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    upload_dir = os.path.join(os.getcwd(), "uploads")
    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # get the destination path
    dest = os.path.join(upload_dir, file.filename)
    print(dest)

    # copy the file contents
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}


def get_file_info(path: str, filename: str) -> Dict[str, str]:
    """
    Get information about a file
    """
    file_path = os.path.join(path, filename)
    file_info = os.stat(file_path)

    # Get file extension
    file_ext = os.path.splitext(filename)[1]
    if file_ext == '':
        file_ext = 'unknown'
        
    base64_string = ''
    
    with open(file_path, "rb") as file:
        base64_bytes = base64.b64encode(file.read())
        base64_string = base64_bytes.decode('utf-8')
    

    return {
        "filename": filename,
        "last_modified": datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        "extension": file_ext,
        "base64_string": base64_string
    }


@router.get("/files/")
async def get_files_tree() -> Dict[str, List[Dict[str, str]]]:
    base_path = './uploads'
    files_tree = {}
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            files_tree[folder] = [get_file_info(folder_path, f) for f in os.listdir(folder_path)]
    return files_tree

@router.post("/files/")
async def create_upload_file(file: UploadFile, permission_data: PermissionIn):
    try:
        # Create a directory named with today's date
        date_today = datetime.now().strftime('%Y-%m-%d')
        directory = f'./uploads/{date_today}'

        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the file with the date and time included in the filename
        date_time_now = datetime.now().strftime('%H%M%S%f')
        filename = f"{date_time_now}_{file.filename}"
        file_location = f"{directory}/{filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
            
        return {"info": f"file '{filename}' saved at {directory}"}
        
    except Exception as e:
        return {"error": str(e)}

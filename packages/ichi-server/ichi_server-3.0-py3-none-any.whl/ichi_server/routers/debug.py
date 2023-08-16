# ichi Server: An ichi server written in Python
# Copyright (C) 2022-present aveeryy

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import re
import os
from hashlib import sha1
from uuid import uuid4

from fastapi import APIRouter, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy import func
from sqlmodel import Session, select

from ichi_server.dependencies import check_password_requirements
from ichi_server.manager import captchas, database_engine
from ichi_server.models.account import User, UserProfile, AccountImageTypes
from ichi_server.models.misc import CAPTCHASolution
from ichi_server.routers.account import base_paths

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.post(
    "/test_captcha_solution",
    responses={200: {"description": "CAPTCHA solution was valid"}},
    tags=["CAPTCHA"],
)
async def test_captcha_solution(_: CAPTCHASolution):
    """
    Returns True if the CAPTCHA solution is correct,
    raises a ValidationError otherwise.

    Revokes the CAPTCHA identifier afterwards.
    """
    return True


@router.get("/get_solved_captcha", tags=["CAPTCHA"])
async def get_solved_captcha():
    captcha_id = str(uuid4())
    captchas[captcha_id] = "DEBUG01"
    return {"identifier": captcha_id, "solution": "DEBUG01"}


@router.put("/modify_user_profile", tags=["Profile"])
async def modify_user_profile(username: str, new_data: UserProfile):
    username = username.lower()

    with Session(database_engine) as session:
        statement = select(User).where(func.lower(User.username) == username.lower())
        user_db = session.exec(statement).first()
        if not user_db:
            # Should not happen, but better safe than sorry
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "error_code": "non_existant_user",
                    "error_msg": f"There's no user with username {username}",
                },
            )
        for field in new_data.__annotations__:
            setattr(user_db, field, getattr(new_data, field))
        session.add(user_db)
        session.commit()
    return {"error": False}


@router.post(
    "/set_profile_picture",
    responses={
        200: {
            "content": {"application/json": {}},
            "description": "The picture hash and image type",
        },
        415: {
            "content": {"application/json": {}},
            "description": "The uploaded image's file format is not supported",
        },
    },
    tags=["Profile"],
)
async def force_set_profile_picture(
    username: str, image: UploadFile, image_type: AccountImageTypes
):
    """Sets \<username\>'s profile picture to the uploaded photo"""
    VALID_TYPES = {
        b"\x89PNG": "png",
        b"\xff\xd8\xff": "jpeg",
        b"RIFF.{4}WEBP": "webp",
        b"BM": "bmp",
    }
    raw_image = await image.read()
    magic_number = raw_image[0:12]
    uploaded_type = None
    for type_magic_num, file_type in VALID_TYPES.items():
        if re.match(type_magic_num, magic_number):
            uploaded_type = file_type
    if uploaded_type is None:
        raise HTTPException(
            status_code=415,
            detail={
                "error": True,
                "error_code": "invalid_file_type",
                "error_msg": "The uploaded image does not have one of the following formats: %s"
                % (", ".join(VALID_TYPES.values())),
            },
        )

    with open(f"{base_paths[image_type]}/{username}.image", "wb") as fp:
        fp.write(raw_image)

    image_hash = sha1(raw_image).hexdigest()

    with open(f"{base_paths[image_type]}/{username}.json", "w") as fp:
        json.dump({"hash": image_hash, "type": uploaded_type}, fp)

    return {"error": False, "hash": image_hash, "type": uploaded_type}


@router.delete(
    "/delete_profile_picture",
    responses={
        200: {
            "content": {"application/json": {}},
            "description": "The user's profile picture has been successfully deleted",
        },
        404: {
            "content": {"application/json": {}},
            "description": "The user has no profile picture set or does not exist",
        },
    },
    tags=["Profile"],
)
async def delete_profile_picture(username: str, image_type: AccountImageTypes):
    """Delete \<username\>'s profile picture"""
    path = f"{base_paths[image_type]}/{username}"

    if not os.path.exists(f"{path}.image"):
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "error_code": "non_existant_image",
            },
        )

    os.remove(f"{path}.image")
    os.remove(f"{path}.json")

    return {"error": False}


@router.post("/check_password_requirements", tags=["Authentication"])
async def check_pass_requirements(password: str):
    return check_password_requirements(password)

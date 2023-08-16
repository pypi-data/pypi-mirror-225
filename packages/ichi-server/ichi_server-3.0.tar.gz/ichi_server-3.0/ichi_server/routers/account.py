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
import os
import re
import time
from hashlib import sha1
from uuid import uuid4

from fastapi import APIRouter, Depends, Request, UploadFile, HTTPException
from fastapi.responses import FileResponse
from ichi_auth import AuthJWT
from sqlalchemy import func
from sqlmodel import Session, select

from ichi_server.dependencies import (
    check_password_requirements,
    generate_recovery_codes,
    get_token_data,
    hash_password,
    settings,
    verify_password,
)
from ichi_server.manager import (
    connection_manager,
    database_engine,
    get_authenticated_user,
)
from ichi_server.models.account import (
    User,
    UserBase,
    UserMinimal,
    UserProfile,
    UserRegister,
    UserLogin,
    UserRecover,
    UserPassword,
    UserChangePassword,
    ichiSession,
    InvalidUsername,
    AccountImageTypes,
)
from ichi_server.models.exceptions import GenericErrorSchema, InvalidPassword

router = APIRouter(prefix="/user")


base_paths = {
    "picture": settings.profile_picture_storage_path,
    "banner": settings.profile_banners_storage_path,
}


@router.get(
    "",
    responses={
        200: {
            "content": {"application/json": {}},
            "model": UserBase,
            "description": "The account public data",
        },
        401: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "The session is invalid",
        },
    },
    summary="Get the authenticated user's profile information",
    tags=["Profile"],
)
async def get_authed_user_profile(Authorize: AuthJWT = Depends()) -> UserBase:
    Authorize.jwt_required()
    session_identifier = Authorize.get_jwt_subject()
    result = get_authenticated_user(session_identifier, ignore_active_sessions=True)
    if type(result) is not User:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": result[0], "error_msg": result[1]},
        )
    return UserBase(**dict(result))


@router.put(
    "",
    summary="Modify the authenticated user's profile information",
    tags=["Profile"],
)
async def modify_user_profile(new_data: UserProfile, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    session_identifier = Authorize.get_jwt_subject()
    with Session(database_engine) as session:
        statement = select(ichiSession).where(
            ichiSession.session_id == session_identifier
        )
        user_session = session.exec(statement).first()
        if not user_session:
            # Should not happen, but better safe than sorry
            raise HTTPException(
                status_code=401,
                detail={
                    "error": True,
                    "error_code": "invalid_session",
                    "error_msg": "The session has expired or has been revoked",
                },
            )
        user_db = user_session.user
        for field in new_data.__annotations__:
            setattr(user_db, field, getattr(new_data, field))
            if user_db.username in connection_manager.clients:
                # Update the live user if they are online
                setattr(
                    connection_manager.clients[user_db.username],
                    field,
                    getattr(new_data, field),
                )
        if user_db.username in connection_manager.clients:
            for room in connection_manager.clients[user_db.username].rooms:
                await room._broadcast(
                    {
                        "type": "profile_updated",
                        "player": user_db.username,
                        "profile": UserMinimal(**user_db.dict()).dict(),
                    }
                )
        session.add(user_db)
        session.commit()
    return {"error": False}


@router.get(
    "s/{username}",
    responses={
        200: {
            "content": {"application/json": {}},
            "model": UserBase,
            "description": "The account public data",
        },
        404: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "The specified user does not exist",
        },
    },
    summary="Get an user's profile information",
    tags=["Profile"],
)
async def get_user_profile(username: str) -> UserBase:
    if not re.match(r"^\w{1,32}$", username):
        raise InvalidUsername
    with Session(database_engine) as session:
        statement = select(User).where(func.lower(User.username) == username.lower())
        user_db = session.exec(statement).first()
        if not user_db:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "error_code": "non_existant_user",
                    "error_msg": f"There's no user with username {username}",
                },
            )
        return UserBase(**dict(user_db))


@router.post(
    "/register",
    responses={
        200: {
            "content": {"application/json": {}},
            "description": "The account has been created, response contains auth tokens and account recovery codes",
        },
        409: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "The username is already in use",
        },
        418: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "Registration is disabled",
        },
    },
    summary="Create an account",
    tags=["Authentication"],
)
async def register(
    user: UserRegister, request: Request, Authorize: AuthJWT = Depends()
):
    if not settings.enable_registration:
        raise HTTPException(
            status_code=418,
            detail={
                "error": True,
                "error_code": "feature_disabled",
                "error_msg": "Registration is disabled",
            },
        )

    with Session(database_engine) as session:
        statement = select(User).where(
            func.lower(User.username) == user.username.lower()
        )
        possible_user = session.exec(statement).first()
        if possible_user is not None:
            raise HTTPException(
                status_code=409,
                detail={"error": True, "error_code": "username_already_in_use"},
            )
        unmet_password_requirements = check_password_requirements(user.password)
        if unmet_password_requirements:
            raise InvalidPassword(unmet_requirements=unmet_password_requirements)
        recovery_codes = generate_recovery_codes()
        new_user = User(
            username=user.username,
            display_name=user.username
            if user.display_name is None or not user.display_name.strip()
            else user.display_name,
            password=hash_password(user.password),
            recovery_codes=json.dumps([hash_password(code) for code in recovery_codes]),
        )
        existing_user = session.exec(select(User)).first()
        if existing_user is None:
            # Make the first user a superadmin
            new_user.admin_state = 2
        session.add(new_user)
        session_id = str(uuid4())
        access_token = Authorize.create_access_token(subject=session_id, fresh=True)
        refresh_token = Authorize.create_refresh_token(subject=session_id)
        user_session = ichiSession(
            session_id=session_id,
            user=new_user,
            ip_address=request.headers[
                "x-forwarded-for" if "x-forwarded-for" in request.headers else "host"
            ],
            user_agent=request.headers["user-agent"],
            expiry_time=get_token_data(refresh_token, 1, "exp"),
            last_conn=int(time.time()),
        )
        session.add(user_session)
        session.commit()

    return {
        "error": False,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "recovery_codes": recovery_codes,
    }


@router.post(
    "/login",
    responses={
        200: {
            "content": {"application/json": {}},
            "description": "Successful login",
        },
        401: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "The user does not exist or the password is incorrect",
        },
    },
    summary="Log in to an account",
    tags=["Authentication"],
)
async def login(user: UserLogin, request: Request, Authorize: AuthJWT = Depends()):
    with Session(database_engine) as session:
        statement = select(User).where(
            func.lower(User.username) == user.username.lower()
        )
        user_db = session.exec(statement).first()
        if user_db is None or not verify_password(user.password, user_db.password):
            raise HTTPException(
                status_code=401,
                detail={
                    "error": True,
                    "error_code": "incorrect_credentials",
                    "error_msg": "Incorrect username or password",
                },
            )
        session_id = str(uuid4())
        access_token = Authorize.create_access_token(subject=session_id, fresh=True)
        refresh_token = Authorize.create_refresh_token(subject=session_id)
        user_session = ichiSession(
            session_id=session_id,
            user=user_db,
            ip_address=request.headers[
                "x-forwarded-for" if "x-forwarded-for" in request.headers else "host"
            ],
            user_agent=request.headers["user-agent"],
            expiry_time=get_token_data(refresh_token, 1, "exp"),
            last_conn=int(time.time()),
        )
        session.add(user_session)
        session.commit()

        return {"access_token": access_token, "refresh_token": refresh_token}


@router.post(
    "/change_password",
    responses={
        200: {
            "content": {"application/json": {}},
            "description": "The password has been updated",
        },
        401: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "The user does not exist",
        },
    },
    summary="Change an authenticated user's password",
    tags=["Authentication"],
)
async def change_password(
    passwd: UserChangePassword,
    revoke_other_sessions: bool = False,
    Authorize: AuthJWT = Depends(),
):
    Authorize.fresh_jwt_required()
    session_identifier = Authorize.get_jwt_subject()
    with Session(database_engine) as database_session:
        statement = select(ichiSession).where(
            ichiSession.session_id == session_identifier
        )
        user_session = database_session.exec(statement).first()
        if not user_session:
            # Should not happen, but better safe than sorry
            raise HTTPException(
                status_code=401,
                detail={
                    "error": True,
                    "error_code": "invalid_session",
                    "error_msg": "The session has expired or has been revoked",
                },
            )

        user_db = user_session.user
        user_db.password = hash_password(passwd.password)
        database_session.add(user_db)
        if revoke_other_sessions:
            sessions = database_session.exec(
                select(ichiSession).where(ichiSession.user == user_db)
            )
            for session_to_revoke in sessions:
                if session_to_revoke.session_id == session_identifier:
                    continue
                database_session.delete(session_to_revoke)
        database_session.commit()
    return {"error": False}


@router.post(
    "/recover",
    summary="Reset an user's password using one of their recovery codes",
    tags=["Authentication"],
)
async def recover_account(
    user: UserRecover, request: Request, Authorize: AuthJWT = Depends()
):
    with Session(database_engine) as session:
        statement = select(User).where(
            func.lower(User.username) == user.username.lower()
        )
        user_db = session.exec(statement).first()
        if user_db is None:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": True,
                    "error_code": "incorrect_credentials",
                    "error_msg": "Incorrect username or recovery code",
                },
            )

        recovery_codes = json.loads(user_db.recovery_codes)
        for code in recovery_codes.copy():
            if verify_password(user.recovery_code, code):
                del recovery_codes[recovery_codes.index(code)]
                with Session(database_engine) as session:
                    user_db = session.exec(statement).first()
                    user_db.password = hash_password(user.password)
                    user_db.recovery_codes = json.dumps(recovery_codes)
                    session.add(user_db)
                    session_id = str(uuid4())
                    access_token = Authorize.create_access_token(
                        subject=session_id, fresh=True
                    )
                    refresh_token = Authorize.create_refresh_token(subject=session_id)
                    user_session = ichiSession(
                        session_id=session_id,
                        user=user_db,
                        ip_address=request.headers[
                            "x-forwarded-for"
                            if "x-forwarded-for" in request.headers
                            else "host"
                        ],
                        user_agent=request.headers["user-agent"],
                        expiry_time=get_token_data(refresh_token, 1, "exp"),
                        last_conn=int(time.time()),
                    )
                    session.add(user_session)
                    session.commit()

                return {
                    "error": False,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
        raise HTTPException(
            status_code=401,
            detail={
                "error": True,
                "error_code": "incorrect_credentials",
                "error_msg": "Incorrect username or recovery code",
            },
        )


@router.delete(
    "/delete_account",
    summary="Deletes the authenticated user's account and all it's data",
    tags=["Authentication"],
)
async def delete_account(Authorize: AuthJWT = Depends()):
    Authorize.fresh_jwt_required()

    token = Authorize.get_jwt_subject()

    with Session(database_engine) as session:
        statement = select(ichiSession).where(ichiSession.session_id == token)
        user_session = session.exec(statement).first()
        if not user_session:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": True,
                    "error_code": "invalid_session",
                    "error_msg": "The session has expired or has been revoked",
                },
            )
        username = user_session.username
        sessions_statement = select(ichiSession).where(
            ichiSession.user == user_session.user
        )
        for session_to_revoke in session.exec(sessions_statement):
            session.delete(session_to_revoke)
        session.delete(user_session.user)
        session.commit()
    for i in ("picture", "banner"):
        if os.path.exists(f"{base_paths[i]}/{username}.image"):
            os.remove(f"{base_paths[i]}/{username}.image")
        if os.path.exists(f"{base_paths[i]}/{username}.json"):
            os.remove(f"{base_paths[i]}/{username}.json")
    return {"error": False}


@router.post(
    "/session/refresh",
    summary="Get a non-fresh access token for the current session",
    tags=["Authentication"],
)
async def refresh_session(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    session_identifier = Authorize.get_jwt_subject()
    result = get_authenticated_user(session_identifier, ignore_active_sessions=True)
    if type(result) is not User:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": result[0], "error_msg": result[1]},
        )
    access_token = Authorize.create_access_token(subject=session_identifier)
    return {"access_token": access_token}


@router.post(
    "/session/elevate",
    summary="Get a fresh access token for the current session, required for some account operations",
    tags=["Authentication"],
)
async def get_fresh_token(form: UserPassword, Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    session_identifier = Authorize.get_jwt_subject()
    result = get_authenticated_user(session_identifier, ignore_active_sessions=True)
    if type(result) is not User:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": result[0], "error_msg": result[1]},
        )
    if not verify_password(form.password, result.password):
        raise HTTPException(
            status_code=401,
            detail={
                "error": True,
                "error_code": "incorrect_credentials",
                "error_msg": "Incorrect password",
            },
        )
    access_token = Authorize.create_access_token(subject=session_identifier, fresh=True)
    return {"access_token": access_token}


@router.delete(
    "/session/{session_identifier_to_revoke}",
    summary="Revoke a session",
    tags=["Authentication"],
)
async def revoke_session(
    session_identifier_to_revoke: str, Authorize: AuthJWT = Depends()
):
    Authorize.fresh_jwt_required()

    session_identifier = Authorize.get_jwt_subject()
    with Session(database_engine) as session:
        statement = select(ichiSession).where(
            ichiSession.session_id == session_identifier
        )
        user_session = session.exec(statement).first()
        if not user_session:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": True,
                    "error_code": "invalid_session",
                    "error_msg": "The session has expired or has been revoked",
                },
            )

        session_statement = select(ichiSession).where(
            ichiSession.session_id == session_identifier_to_revoke
        )
        session_to_revoke = session.exec(session_statement).first()
        if not session_to_revoke:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "error_code": "non_existant_session",
                    "error_msg": "The requested session does not exist",
                },
            )
        session.delete(session_to_revoke)
        session.commit()
    return {"error": False}


@router.get(
    "/sessions",
    summary="Get the authenticated user's sessions",
    tags=["Authentication"],
)
async def get_sessions(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    session_identifier = Authorize.get_jwt_subject()
    with Session(database_engine) as session:
        statement = select(ichiSession).where(
            ichiSession.session_id == session_identifier
        )
        user_session = session.exec(statement).first()
        if not user_session:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": True,
                    "error_code": "invalid_session",
                    "error_msg": "The session has expired or has been revoked",
                },
            )
        sessions_statement = select(ichiSession).where(
            ichiSession.username == user_session.username
        )
        sessions = session.exec(sessions_statement)
        return {
            "error": False,
            "sessions": list(sessions),
            "current_session": session_identifier,
        }


def _verify_image_type_state(image_type: str):
    if (
        image_type == "picture"
        and not settings.enable_profile_pictures
        or image_type == "banner"
        and not settings.enable_profile_banners
    ):
        raise HTTPException(
            status_code=418,
            detail={
                "error": True,
                "error_code": "feature_disabled",
                "error_msg": f"Profile {image_type}s are disabled",
            },
        )


@router.get(
    "s/{username}/image",
    response_class=FileResponse,
    responses={
        200: {
            "content": {"image/*": {}},
            "description": "The user's profile picture or banner",
        },
        404: {
            "content": {"application/json": {}},
            "description": "The user has no profile picture or banner set or does not exist",
        },
        418: {
            "content": {"application/json": {}},
            "description": "Profile pictures or banners are disabled",
        },
    },
    summary="Get an user's profile picture or banner",
    tags=["Profile"],
)
async def get_profile_picture(username: str, image_type: AccountImageTypes):
    _verify_image_type_state(image_type)
    path = f"{base_paths[image_type]}/{username.lower()}.image"
    if not os.path.exists(path):
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "error_code": "non_existant_image",
                "error_message": f"The user does not exist or does not have a profile {image_type} set",
            },
        )
    metadata = await get_profile_picture_metadata(username, image_type)
    return FileResponse(path, headers={"Content-Type": f"image/{metadata['type']}"})


@router.get(
    "s/{username}/image/metadata",
    responses={
        200: {
            "content": {"image/*": {}},
            "description": "The user's profile picture or banner's metadata",
        },
        404: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "The user has no profile picture or banner set or does not exist",
        },
        418: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "Profile pictures or banners are disabled",
        },
    },
    summary="Get an user's profile picture or banner's hash and file type",
    tags=["Profile"],
)
async def get_profile_picture_metadata(username: str, image_type: AccountImageTypes):
    _verify_image_type_state(image_type)
    path = f"{base_paths[image_type]}/{username.lower()}.json"
    if not os.path.exists(path):
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "error_code": "non_existant_image",
                "error_message": f"The user does not exist or does not have a profile {image_type} set",
            },
        )
    with open(path, "r") as fp:
        metadata = fp.read()
    return json.loads(metadata)


@router.post(
    "/image",
    responses={
        200: {
            "content": {"application/json": {}},
            "description": "The image's hash and image type",
        },
        413: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "The uploaded image exceeds the maximum size configured",
        },
        415: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "The uploaded image's file format is not supported",
        },
        418: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "Profile pictures or banners are disabled",
        },
    },
    summary="Set the authenticated user's profile picture or banner",
    tags=["Profile"],
)
async def upload_profile_image(
    image: UploadFile, image_type: AccountImageTypes, Authorize: AuthJWT = Depends()
):
    _verify_image_type_state(image_type)
    if image.size > settings.profile_images_maximum_size:
        raise HTTPException(
            status_code=413,
            detail={"error": True, "error_code": "image_exceeds_maximum_size"},
        )
    Authorize.jwt_required()
    session_identifier = Authorize.get_jwt_subject()
    result = get_authenticated_user(session_identifier, ignore_active_sessions=True)
    if type(result) is not User:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": result[0], "error_msg": result[1]},
        )
    # Verify that the image has a valid type by checking it's magic number
    VALID_TYPES = {
        b"\x89PNG": "png",
        b"\xff\xd8\xff": "jpeg",
        b"RIFF.{4}WEBP": "webp",
        b"BM": "bmp",
    }
    raw_image = await image.read(settings.profile_images_maximum_size)
    magic_number = raw_image[:12]
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
    with open(f"{base_paths[image_type]}/{result.username.lower()}.image", "wb") as fp:
        fp.write(raw_image)
    image_hash = sha1(raw_image).hexdigest()
    with open(f"{base_paths[image_type]}/{result.username.lower()}.json", "w") as fp:
        json.dump({"hash": image_hash, "type": uploaded_type}, fp)
    if result.username in connection_manager.clients:
        for room in connection_manager.clients[result.username].rooms:
            await room._broadcast(
                {
                    "type": "profile_image_updated",
                    "player": result.username,
                    "image_type": image_type,
                }
            )
    return {"error": False, "hash": image_hash, "type": uploaded_type}


@router.delete(
    "/image",
    responses={
        200: {
            "content": {"application/json": {}},
            "description": "The user's profile picture has been successfully deleted",
        },
        404: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "The user has no profile picture set or does not exist",
        },
        418: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "Profile pictures are disabled",
        },
    },
    summary="Delete the authenticated user's profile picture or banner",
    tags=["Profile"],
)
async def delete_profile_image(
    image_type: AccountImageTypes, Authorize: AuthJWT = Depends()
):
    """Delete the user's profile picture, requires an access token"""
    _verify_image_type_state(image_type)
    Authorize.jwt_required()
    session_identifier = Authorize.get_jwt_subject()
    result = get_authenticated_user(session_identifier, ignore_active_sessions=True)
    if type(result) is not User:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": result[0], "error_msg": result[1]},
        )
    path = f"{base_paths[image_type]}/{result.username.lower()}"
    if not os.path.exists(f"{path}.image"):
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "error_code": "non_existant_image",
                "error_message": f"You have no profile {image_type} set",
            },
        )
    os.remove(f"{path}.image")
    os.remove(f"{path}.json")
    if result.username in connection_manager.clients:
        for room in connection_manager.clients[result.username].rooms:
            await room._broadcast(
                {
                    "type": "profile_image_removed",
                    "player": result.username,
                    "image_type": image_type,
                }
            )
    return {"error": False}

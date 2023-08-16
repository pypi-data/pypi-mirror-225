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

from hashlib import sha1
import json
import re
import os
from time import time
from typing import Any

from fastapi import WebSocket
from sqlmodel import SQLModel, Field, create_engine, Session, select

from ichi_server.dependencies import (
    RESOURCES_PATH,
    _h,
    generate_recovery_codes,
    hash_password,
    settings,
)
from ichi_server.models.account import User, ichiSession
from ichi_server.models.client import AuthedClientRef

_ALEMBIC_NAME_REGEX = r"^\d{4}_\d{2}_\d{2}_\d{4}-(\w{12})"
game_mode_images_metadata = {}


class _AlembicVersion(SQLModel, table=True):
    __tablename__ = "alembic_version"
    version_num: str = Field(primary_key=True)


def _insert_last_migration_into_new_database() -> None:
    with Session(database_engine) as session:
        result = session.exec(select(_AlembicVersion)).first()
        if result == None:
            session.add(_AlembicVersion(version_num=_get_last_alembic_migration()))
            session.commit()


def _get_last_alembic_migration() -> str:
    versions = list(os.scandir(f"{os.path.dirname(__file__)}/migrations/versions"))
    index = -1
    for _ in versions:
        version = versions[index]
        if version.is_file():
            return re.match(_ALEMBIC_NAME_REGEX, version.name).group(1)
        index -= 1


class ConnectionManager:
    def __init__(self):
        self.clients: dict[str, AuthedClientRef] = {}

    async def connect(self, client: WebSocket, client_type: str = "game"):
        await client.accept()

    def disconnect(self, client: AuthedClientRef):
        if client.username in self.clients:
            del self.clients[client.username]

    async def broadcast(self, message: dict):
        """Sends a message to all the authenticated game clients"""
        for client in self.clients.values():
            await client.send_event(message)


def create_database_and_tables():
    print(f"{_h('sqlmodel')} Updating database tables")
    SQLModel.metadata.create_all(database_engine)
    _insert_last_migration_into_new_database()
    with Session(database_engine) as session:
        existing_admin_user = session.exec(
            select(User).where(User.username == "admin")
        ).first()
        if existing_admin_user is not None:
            return
        administration_password = os.environ.get("ICHI_ADMINISTRATION_PASSWORD", "")
        while not administration_password:
            administration_password = input("Insert a password for the admin user: ")
        recovery_codes = generate_recovery_codes()
        print(
            "Recovery codes for administration account: %s" % " ".join(recovery_codes)
        )
        admin_user = User(
            username="admin",
            display_name="Admin account",
            password=hash_password(administration_password),
            admin_state=2,
            recovery_codes=json.dumps([hash_password(code) for code in recovery_codes]),
        )
        session.add(admin_user)
        session.commit()


def get_authenticated_user(
    session_identifier: str,
    connection_details: tuple = (),
    ignore_active_sessions: bool = False,
) -> User | tuple[str, str]:
    """
    Checks if the provided session is valid and returns the authenticated
    user's information.

    :param session_identifier: The session's identifier
    :param connection_details: A tuple containing the IP address and the client's
    name to update the session's connection details, leave empty to skip
    :param ignore_active_sessions: Bypasses the active sessions check
    :return: The user's information is the session is valid, a tuple containing
    an error code and message otherwise
    """
    with Session(database_engine) as database_session:
        user_session = database_session.exec(
            select(ichiSession).where(ichiSession.session_id == session_identifier)
        ).first()
        if user_session is None:
            return (
                "invalid_session",
                "The session is invalid or has been revoked",
            )
        if user_session.user.ban_expires != 0:
            if (
                not time() > user_session.user.ban_expires
                or user_session.user.ban_expires == -1
            ):
                return (
                    "banned",
                    f"Banned from the server: {user_session.user.ban_reason}",
                )
            user_session.user.ban_expires = 0
            user_session.user.ban_reason = ""
            database_session.add(user_session.user)
        if (
            user_session.user.mute_expires > 0
            and user_session.user.mute_expires < time()
        ):
            user_session.user.mute_expires = 0
            user_session.user.mute_reason = ""
            database_session.add(user_session.user)
        if (
            user_session.username in connection_manager.clients
            and not ignore_active_sessions
        ):
            return (
                "session_active",
                "Already authenticated in another active client",
            )
        if connection_details:
            user_session.ip_address = connection_details[0]
            user_session.user_agent = connection_details[1]
            user_session.last_conn = int(time())
            database_session.add(user_session)
        database_session.commit()
        return user_session.user


def create_game_mode_image_metadata() -> None:
    for image in os.scandir(f"{RESOURCES_PATH}/game_mode_images/"):
        with open(image, "rb") as fp:
            image_data = fp.read()
        game_mode_images_metadata[image.name.replace(".webp", "")] = {
            "hash": sha1(image_data).hexdigest(),
            "type": "webp",
        }


connection_manager = ConnectionManager()
database_engine = create_engine(settings.database_path)
create_game_mode_image_metadata()
rooms: dict[str, Any] = {}
captchas: dict[str, str] = {}

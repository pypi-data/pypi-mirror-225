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

import re

from pydantic import validator
from sqlmodel import Column, JSON, SQLModel, Field, Relationship

from ichi_server.dependencies import check_password_requirements, StringEnum
from ichi_server.models.misc import CAPTCHASolution
from ichi_server.models.exceptions import (
    InvalidDisplayName,
    InvalidUsername,
    InvalidPassword,
)


class UserImmutable(SQLModel):
    """Immutable user information"""

    username: str = Field(primary_key=True)

    @validator("username")
    def check_username_validity(cls, v: str):
        username = v.strip()
        if not re.match(r"^\w{1,16}$", username):
            raise InvalidUsername
        return username


class UserProfile(SQLModel):
    """Mutable user information"""

    display_name: str | None

    @validator("display_name")
    def check_display_name_validity(cls, v: str):
        display_name = v.strip()
        if not re.match(r"^.{1,16}$", display_name):
            raise InvalidDisplayName
        return display_name


class UserMinimal(UserProfile, UserImmutable):
    """Contains only the information that's useful in a game"""

    admin_state: int = 0  # 0: non-admin, 1: admin, 2: super-admin
    mute_expires: int = Field(default=0, sa_column_kwargs={"server_default": "0"})
    mute_reason: str = Field(default="", sa_column_kwargs={"server_default": ""})


class UserBase(UserMinimal):
    """Contains all public user information, mutable or immutable"""

    stats: dict = Field(default={}, sa_column=Column(JSON))
    ban_expires: int = Field(sa_column_kwargs={"server_default": "0"})
    ban_reason: str = Field(sa_column_kwargs={"server_default": ""})


class UserPassword(SQLModel):
    password: str


class UserChangePassword(UserPassword):
    """
    Used for changing an authenticated user's password

    Since the endpoint requires a fresh token asking for the old
    password is not required

    This is splitted from UserPassword since a change in password requirements
    would lock registered users out of their accounts
    """

    @validator("password")
    def check_password_requirements(cls, v: str):
        unmet_requirements = check_password_requirements(v)
        if unmet_requirements:
            raise InvalidPassword(unmet_requirements=unmet_requirements)
        return v


class User(UserBase, UserPassword, table=True):
    """Database model, contains all public and private user information"""

    __tablename__: str = "users"

    recovery_codes: str
    sessions: list["ichiSession"] = Relationship(back_populates="user")


class UserLogin(UserPassword, UserImmutable):
    """Used for login"""


class UserRegister(UserLogin):
    """Used for account registration"""

    display_name: str | None
    captcha: CAPTCHASolution


class UserRecover(UserLogin):
    """Used for recovering an account using a recovery code"""

    recovery_code: str


class ichiSession(SQLModel, table=True):
    __tablename__: str = "sessions"

    session_id: str = Field(primary_key=True)
    username: str = Field(default=None, foreign_key="users.username")
    user: User = Relationship(back_populates="sessions")
    ip_address: str | None
    user_agent: str | None
    expiry_time: int
    last_conn: int


class BannedIPAddress(SQLModel, table=True):
    __tablename__ = "banned_addresses"

    address: str = Field(primary_key=True, nullable=False)
    username: str = Field(index=True, nullable=True, default=None)
    until: float = Field(nullable=False, default=-1)
    reason: str = Field(nullable=True)


class AccountImageTypes(StringEnum):
    picture = "picture"
    banner = "banner"

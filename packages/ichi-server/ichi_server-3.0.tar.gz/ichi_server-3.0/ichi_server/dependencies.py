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

import base64
import json
import os
import re
import sys
from copy import deepcopy
from enum import Enum
from typing import Iterable
from uuid import uuid4

import colorama
from fastapi import WebSocket
from ichi_auth import AuthJWT
from passlib.context import CryptContext
from pydantic import BaseSettings, errors


def get_config_path() -> str:
    base = os.path.expanduser("~")
    paths = {
        "linux": f"{base}/.local/share/ichi/Server",
        "win32": f"{base}\\AppData\\Local\\ichi\\Server",
        "darwin": f"{base}/Library/Application Support/ichi/Server",
    }

    if sys.platform not in paths:
        return f"{base}/.ichi/Server"
    return paths[sys.platform]


CONFIG_PATH = get_config_path()
RESOURCES_PATH = f"{os.path.dirname(__file__)}/resources"
os.makedirs(CONFIG_PATH, exist_ok=True)


class Settings(BaseSettings):
    authjwt_secret_key: str = None
    authjwt_header_name: str = "HTTPBearer"
    authjwt_access_token_expires: int = 3600  # 1 hour
    authjwt_refresh_token_expires: int = 86400 * 365  # 1 year
    database_path: str = f"sqlite:///{CONFIG_PATH}/database.db"
    enable_debug_capabilities: bool = False
    enable_profile_banners: bool = True
    enable_profile_pictures: bool = True
    enable_registration: bool = True
    hypercorn_bind_address: str = "0.0.0.0:1111"
    message_reporting_secret_key: str | None = None
    password_minimum_length: int = 8
    password_maximum_length: int = 128
    password_minimum_letters: int = 1
    password_minimum_numbers: int = 1
    password_minimum_symbols: int = 0
    profile_images_maximum_size: int = 1048576  # 1 MByte
    profile_banners_storage_path: str = f"{CONFIG_PATH}/banners"
    profile_picture_storage_path: str = f"{CONFIG_PATH}/profile_pictures"
    server_name: str = "ichi Server"

    class Config:
        env_file = ".env", "/etc/ichi.env", f"{CONFIG_PATH}/.env", "test.env"
        env_file_encoding = "utf-8"


def _h(text: str) -> str:
    """Returns a normal header"""
    return f"{colorama.Style.BRIGHT}{text}:{colorama.Style.RESET_ALL}"


def _w(text: str) -> str:
    """Returns a warning header"""
    return f"{colorama.Fore.YELLOW}{_h(text)}"


def _e(text: str) -> str:
    """Returns an error header"""
    return f"{colorama.Fore.RED}{_h(text)}"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plaintext, hashed):
    return pwd_context.verify(plaintext, hashed)


def hash_password(password):
    return pwd_context.hash(password)


if not any(os.path.exists(file) for file in Settings.Config.env_file):
    with open(f"{CONFIG_PATH}/.env", "w") as fp:
        print(f"{_h('ichi')} Generating configuration file in {CONFIG_PATH}/.env")
        fp.write(f"authjwt_secret_key={str(uuid4()).replace('-', '')}")

settings = Settings()


@AuthJWT.load_config
def get_authjwt_config():
    return settings


if settings.authjwt_secret_key is None:
    raise errors.ConfigError("AuthJWT secret key is not set")

if settings.enable_profile_pictures:
    os.makedirs(settings.profile_picture_storage_path, exist_ok=True)

if settings.enable_profile_banners:
    os.makedirs(settings.profile_banners_storage_path, exist_ok=True)

authjwt_translation = {
    "Signature has expired": "signature_expired",
    "Token has been revoked": "token_revoked",
    "Missing access token from Query or Path": "token_missing",
}


class StringEnum(str, Enum):
    def __str__(self):
        return str(self.name).lower()

    def _generate_next_value_(name, *_):
        return name.lower()


def get_argument_value(args: str | list):
    """Returns the value of one or more command line arguments"""
    _arg = None
    if type(args) is not str:
        for arg in args:
            if arg in sys.argv[1:]:
                _arg = arg
                break
    elif type(args) is str:
        _arg = args
    if _arg is None:
        # No arguments in args have been found in sys.argv
        return
    if sys.argv[1:].index(_arg) + 1 >= len(sys.argv[1:]):
        return
    return sys.argv[1:][sys.argv[1:].index(_arg) + 1]


def dict_merge(
    dct: dict, merge_dct: dict, overwrite=False, modify=True, extend_lists=False
) -> dict:
    """Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :param overwrite: replace existing keys
    :param modify: modify dct directly
    :param extend_list: extend list objects instead of replacing them
    :return: dict

    Modified version of angstwad's snippet
    https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
    """

    if not modify:
        # Make a copy of dct to not modify the obj directly
        dct = deepcopy(dct)
    for k in merge_dct:
        if k in dct and type(dct[k]) is dict and type(merge_dct[k] is dict):
            dict_merge(dct[k], merge_dct[k], overwrite, True)
        elif k not in dct or overwrite and merge_dct[k] is not None:
            if (
                k in dct
                and isinstance(dct[k], list)
                and isinstance(merge_dct[k], Iterable)
                and extend_lists
            ):
                dct[k].extend(merge_dct[k])
            else:
                dct[k] = merge_dct[k]
    return dct


async def has_missing_params(
    event: dict, required_parameters: list[str], websocket: WebSocket
) -> bool:
    """
    Checks if the received event has all the required parameters

    :param event: The event as sent by the client
    :param required_parameters: A list of the required keys' names
    :return: A list with the missing parameters
    """

    missing_params = [param for param in required_parameters if param not in event]

    if missing_params:
        await websocket.send_json(
            {
                "error": True,
                "error_code": "missing_event_parameters",
                "missing": missing_params,
                "rid": event["rid"] if "rid" in event else None,
            }
        )

    return bool(missing_params)


def get_token_data(token: str, chunk_index: int, key: str):
    chunks = token.split(".")
    decoded = base64.b64decode(chunks[chunk_index] + "==")
    as_json = json.loads(decoded)
    return as_json[key]


def get_token_subject(token: str) -> str | None:
    """
    Returns the subject of a JWT (JSON Web Token)

    fastapi_jwt_auth does not set the _token variable if the token is not provided with cookies
    when using websockets, returning None when calling .get_jwt_subject()

    :param token: The JWT, can be access or refresh
    :returns: The token's subject or None if the token is invalid
    """
    try:
        return get_token_data(token, 1, "sub")
    except (json.JSONDecodeError, IndexError):
        return


def check_password_requirements(password: str) -> list:
    """Check if a password mets the server's requirements"""
    requirements = [
        ("min_length", len(password) >= settings.password_minimum_length),
        ("max_length", len(password) <= settings.password_maximum_length),
        (
            "min_letters",
            len(re.findall(r"\w(?<!_|\d)", password))
            >= settings.password_minimum_letters,
        ),
        (
            "min_numbers",
            len(re.findall(r"[0-9]", password)) >= settings.password_minimum_numbers,
        ),
        (
            "min_symbols",
            len(re.findall(r"(?:[^\w]|_)", password))
            >= settings.password_minimum_symbols,
        ),
    ]
    unmet_requirements = [name for name, condition in requirements if not condition]

    return unmet_requirements


def generate_recovery_codes(amount: int = 5) -> list[str]:
    return [f"R{''.join(str(uuid4()).split('-')[0:3])}" for _ in range(amount)]


def is_recovery_code_valid(recovery_code: str) -> bool:
    return bool(re.match(r"R[a-z0-9]{16}", recovery_code))

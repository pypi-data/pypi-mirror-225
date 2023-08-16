# ichi Server: An ichi server written in Python
# Copyright (C) 2023-present aveeryy

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
import hashlib
import hmac
from http import HTTPStatus
import re
from enum import auto

from ichi_server.dependencies import settings, StringEnum
from ichi_server.manager import (
    connection_manager,
    database_engine,
    get_authenticated_user,
)
from ichi_server.models.account import BannedIPAddress, User

from ichi_auth import AuthJWT
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from ichi_server.models.misc import MessageReport


router = APIRouter(prefix="/admin", tags=["Administration"])

LOCAL_IP_RANGE_172 = "|".join([str(i) for i in range(16, 32)])
LOCAL_IP_REGEX = r"^(?:localhost|10\.|172\.(?:%s)\.|192\.168\.)" % LOCAL_IP_RANGE_172


class Punishment(StringEnum):
    BAN = auto()
    MUTE = auto()


class _AdministrationAction(StringEnum):
    UNBAN = auto()
    UNMUTE = auto()
    PROMOTE = auto()
    DEMOTE = auto()


AdministrationAction = StringEnum(
    "AdministrationAction",
    [(i.name, i.value) for i in [*Punishment, *_AdministrationAction]],
)


@router.post("/users/{username}/{action}")
async def apply_action_to_account(
    action: AdministrationAction,
    username: str,
    punish_until: int = -1,
    punishment_reason: str = "",
    apply_ban_to_ip_address: bool = True,
    Authorize: AuthJWT = Depends(),
):
    """
    Applies `action` into `username`'s account.

    `punish_until` and `punishment_reason` are only used with `ban` and `mute` actions.

    `promote` and `demote` actions can only be performed by a superadministrator
    (the first account created)
    """
    Authorize.jwt_required()
    caller = get_authenticated_user(
        Authorize.get_jwt_subject(), ignore_active_sessions=True
    )
    if type(caller) is not User:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": caller[0], "error_msg": caller[1]},
        )
    if caller.admin_state == 0:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": "not_an_administrator"},
        )
    elif (
        action in [AdministrationAction.PROMOTE, AdministrationAction.DEMOTE]
        and caller.admin_state != 2
    ):
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": "not_a_superadministrator"},
        )
    if caller.username == username:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": f"cannot_{action}_yourself"},
        )
    with Session(database_engine) as session:
        user = session.exec(
            select(User).where(func.lower(User.username) == username.lower())
        ).first()
        if user is None:
            raise HTTPException(
                status_code=404,
                detail={"error": True, "error_code": "non_existant_user"},
            )
        if user.admin_state >= caller.admin_state and action in [
            AdministrationAction.BAN,
            AdministrationAction.MUTE,
        ]:
            # Only a superadmin (admin_state == 2) can ban other administrators
            raise HTTPException(
                status_code=401,
                detail={
                    "error": True,
                    "error_code": f"can_not_{action}_another_admin",
                },
            )
        match action:
            case Punishment.BAN:
                user.ban_expires = punish_until
                user.ban_reason = punishment_reason
                # Automatically demote user
                user.admin_state = 0
                if username in connection_manager.clients:
                    await connection_manager.clients[username].websocket.close(
                        4040, punishment_reason
                    )
                if apply_ban_to_ip_address:
                    ip_addresses = set(
                        [session.ip_address for session in user.sessions]
                    )
                    for ip_address in ip_addresses:
                        if re.match(LOCAL_IP_REGEX, ip_address):
                            continue
                        banned_address = BannedIPAddress(
                            address=ip_address,
                            username=user.username,
                            until=punish_until,
                            reason=punishment_reason,
                        )
                        session.add(banned_address)
            case AdministrationAction.UNBAN:
                user.ban_expires = 0
                user.ban_reason = ""
                ip_addresses = session.exec(
                    select(BannedIPAddress).where(
                        BannedIPAddress.username == user.username
                    )
                )
                for ip_address in ip_addresses:
                    session.delete(ip_address)
            case AdministrationAction.MUTE:
                user.mute_expires = punish_until
                user.mute_reason = punishment_reason
                if username in connection_manager.clients:
                    client = connection_manager.clients[username]
                    client.mute_expires = punish_until
                    client.mute_reason = punishment_reason
                    for room in client.rooms:
                        await room._broadcast(
                            {
                                "type": "muted_from_server",
                                "player": username,
                                "expires": punish_until,
                                "reason": punishment_reason,
                            }
                        )
            case AdministrationAction.UNMUTE:
                user.mute_expires = 0
                user.mute_reason = ""
                if username in connection_manager.clients:
                    client = connection_manager.clients[username]
                    client.mute_expires = 0
                    client.mute_reason = ""
                    for room in client.rooms:
                        await room._broadcast(
                            {"type": "unmuted_from_server", "player": username}
                        )
            case AdministrationAction.PROMOTE:
                user.admin_state = 1
                if username in connection_manager.clients:
                    client = connection_manager.clients[username]
                    client.admin_state = 1
                    for room in client.rooms:
                        await room._broadcast(
                            {"type": "promoted_to_admin", "player": username}
                        )
            case AdministrationAction.DEMOTE:
                user.admin_state = 0
                if username in connection_manager.clients:
                    client = connection_manager.clients[username]
                    client.admin_state = 0
                    for room in client.rooms:
                        await room._broadcast(
                            {"type": "demoted_from_admin", "player": username}
                        )
        session.add(user)
        session.commit()
    return {"error": False}


@router.get("/get_{punishment}_players")
async def get_punished_players(
    punishment: Punishment,
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    caller = get_authenticated_user(
        Authorize.get_jwt_subject(), ignore_active_sessions=True
    )
    if type(caller) is not User:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": caller[0], "error_msg": caller[1]},
        )
    if caller.admin_state == 0:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": "not_an_administrator"},
        )
    with Session(database_engine) as session:
        if punishment == Punishment.BAN:
            statement = select(User).where(User.ban_expires != 0)
        elif punishment == Punishment.MUTE:
            statement = select(User).where(User.mute_expires != 0)
        punished_players = session.exec(statement)
        return {
            "error": False,
            "players": [
                {
                    "username": player.username,
                    f"{punishment}_reason": player.ban_reason
                    if punishment == Punishment.BAN
                    else player.mute_reason,
                    "until": player.ban_expires
                    if punishment == Punishment.BAN
                    else player.mute_expires,
                }
                for player in punished_players
            ],
        }


@router.get("/get_administrators")
async def get_administrators(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    caller = get_authenticated_user(
        Authorize.get_jwt_subject(), ignore_active_sessions=True
    )
    if type(caller) is not User:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": caller[0], "error_msg": caller[1]},
        )
    if caller.admin_state != 2:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": "not_a_superadministrator"},
        )
    with Session(database_engine) as session:
        administrators = session.exec(select(User).where(User.admin_state > 0))
        return {
            "error": False,
            "administrators": [
                {"username": player.username, "admin_state": player.admin_state}
                for player in administrators
            ],
        }


@router.post("/addresses/{address}/ban")
async def ban_ip_address(
    address: str,
    until: int = -1,
    reason: str | None = None,
    Authorize: AuthJWT = Depends(),
) -> dict:
    Authorize.jwt_required()
    caller = get_authenticated_user(
        Authorize.get_jwt_subject(), ignore_active_sessions=True
    )
    if type(caller) is not User:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": caller[0], "error_msg": caller[1]},
        )
    if caller.admin_state == 0:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": "not_an_administrator"},
        )
    if re.match(LOCAL_IP_REGEX, address):
        raise HTTPException(
            422, {"error": True, "error_code": "can_not_ban_local_address"}
        )
    with Session(database_engine) as session:
        address_in_db = session.exec(
            select(BannedIPAddress).where(BannedIPAddress.address == address)
        ).first()
        if address_in_db is not None:
            raise HTTPException(
                404, {"error": True, "error_code": "address_is_already_banned"}
            )
        banned_address = BannedIPAddress(
            address=address,
            until=until,
            reason=reason,
        )
        session.add(banned_address)
        session.commit()
    return {"error": False}


@router.post("/addresses/{address}/unban")
async def unban_ip_address(address: str, Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    caller = get_authenticated_user(
        Authorize.get_jwt_subject(), ignore_active_sessions=True
    )
    if type(caller) is not User:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": caller[0], "error_msg": caller[1]},
        )
    if caller.admin_state == 0:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": "not_an_administrator"},
        )
    with Session(database_engine) as session:
        address_object = session.exec(
            select(BannedIPAddress).where(BannedIPAddress.address == address)
        ).first()
        if address_object is None:
            raise HTTPException(
                404, {"error": True, "error_code": "address_is_not_banned"}
            )
        session.delete(address_object)
        session.commit()
    return {"error": False}


@router.get("/addresses")
async def get_banned_addresses(Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    caller = get_authenticated_user(
        Authorize.get_jwt_subject(), ignore_active_sessions=True
    )
    if type(caller) is not User:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": caller[0], "error_msg": caller[1]},
        )
    if caller.admin_state == 0:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "error_code": "not_an_administrator"},
        )
    with Session(database_engine) as session:
        addresses = session.exec(select(BannedIPAddress)).all()
        return {"error": False, "addresses": addresses}


@router.post("/report")
async def report_message(
    message: str, username: str, message_hash: str, Authorize: AuthJWT = Depends()
):
    if settings.message_reporting_secret_key is None:
        raise HTTPException(
            HTTPStatus.IM_A_TEAPOT,
            detail={"error": True, "error_code": "message_reporting_is_not_enabled"},
        )
    Authorize.jwt_required()
    calculated_hash = hmac.new(
        settings.message_reporting_secret_key.encode(),
        msg=f"{username}@@{message}".encode(),
        digestmod=hashlib.sha256,
    ).digest()
    encoded_hash = base64.b64encode(calculated_hash).decode()
    if encoded_hash != message_hash:
        raise HTTPException(
            HTTPStatus.NOT_ACCEPTABLE,
            detail={"error": True, "error_code": "hash_mismatch"},
        )
    with Session(database_engine) as session:
        if (
            session.exec(
                select(MessageReport).where(MessageReport.message_hash == encoded_hash)
            ).first()
            is not None
        ):
            raise HTTPException(
                HTTPStatus.CONFLICT,
                detail={"error": True, "error_code": "already_reported"},
            )
        report = MessageReport(
            username=username, message=message, message_hash=encoded_hash
        )
        session.add(report)
        session.commit()
    return {"error": False}


@router.get("/report")
async def get_reported_messages(Authorize: AuthJWT = Depends()):
    if settings.message_reporting_secret_key is None:
        raise HTTPException(
            HTTPStatus.IM_A_TEAPOT,
            detail={"error": True, "error_code": "message_reporting_is_not_enabled"},
        )
    Authorize.jwt_required()
    caller = get_authenticated_user(
        Authorize.get_jwt_subject(), ignore_active_sessions=True
    )
    if type(caller) is not User:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail={"error": True, "error_code": caller[0], "error_msg": caller[1]},
        )
    if caller.admin_state == 0:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail={"error": True, "error_code": "not_an_administrator"},
        )
    with Session(database_engine) as session:
        return {"error": False, "reports": session.exec(select(MessageReport)).all()}


@router.delete("/report")
async def resolve_report(message_hash: str, Authorize: AuthJWT = Depends()):
    if settings.message_reporting_secret_key is None:
        raise HTTPException(
            HTTPStatus.IM_A_TEAPOT,
            detail={"error": True, "error_code": "message_reporting_is_not_enabled"},
        )
    Authorize.jwt_required()
    caller = get_authenticated_user(
        Authorize.get_jwt_subject(), ignore_active_sessions=True
    )
    if type(caller) is not User:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail={"error": True, "error_code": caller[0], "error_msg": caller[1]},
        )
    if caller.admin_state == 0:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail={"error": True, "error_code": "not_an_administrator"},
        )
    with Session(database_engine) as session:
        report = session.exec(
            select(MessageReport).where(MessageReport.message_hash == message_hash)
        ).first()
        if report is None:
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                detail={"error": True, "error_code": "non_existant_report"},
            )
        session.delete(report)
        session.commit()
    return {"error": False}

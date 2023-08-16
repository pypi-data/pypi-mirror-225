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

import asyncio
import base64
import hashlib
import hmac
import re
import time
from typing import Callable
from uuid import uuid4

from pydantic.dataclasses import dataclass
from pydantic.fields import Field
from sqlmodel import Session, select

from ichi_server.dependencies import StringEnum, _h, dict_merge, settings
from ichi_server.manager import database_engine, rooms
from ichi_server.models.account import User
from ichi_server.models.client import AuthedClientRef
from ichi_server.models.misc import ChatMessage


class RoomState(StringEnum):
    PRE_GAME = "pre_game"
    IN_GAME = "in_game"
    FINISHED = "finished"


class RoomType(StringEnum):
    STATIC = "static"
    DYNAMIC = "dynamic"


@dataclass
class Room:
    _MIN_PLAYERS = 2
    _MAX_PLAYERS = 10
    _PLAYER_MODEL = AuthedClientRef
    # A dictionary containing events with their required parameters.
    # There's no need to add events that don't have any required parameter.
    _EVENTS = {
        "send_message": ["message"],
        "ban_player": ["username"],
        "unban_player": ["username"],
        "mute_player": ["username"],
        "unmute_player": ["username"],
    }

    name: str
    public: bool
    identifier: str = Field(default=None, init=False)  # Set on __post_init__
    players: dict[str, AuthedClientRef] = Field(default_factory=dict, init=False)
    leader: AuthedClientRef = Field(default=None, init=False)
    messages: list[ChatMessage] = Field(default_factory=list, init=False)
    state: RoomState = Field(default=RoomState.PRE_GAME, init=False)
    players_banned: list[str] = Field(default_factory=list, init=False)
    players_muted: list[str] = Field(default_factory=list, init=False)

    _ROOM_TYPE = RoomType.DYNAMIC
    _child = None

    def __post_init__(self):
        self.identifier = self._generate_identifier()
        # Avoid duplicate UUIDs
        while self.identifier in rooms:
            self.identifier = self._generate_identifier()
        if self._PLAYER_MODEL is None or not issubclass(
            self._PLAYER_MODEL, AuthedClientRef
        ):
            raise Exception(
                f"{self.__class__.__name__}._PLAYER_MODEL must inherit from AuthedClientRef"
            )

    def _generate_identifier(self) -> str:
        return str(uuid4()).split("-")[0]

    @property
    def info(self) -> dict:
        """Returns information given to clients on room creation"""
        return {
            "room_identifier": self.identifier,
            "game_mode": self._child.__id__,
            "room_type": "dynamic",
            "name": self.name,
        }

    @property
    def full_info(self) -> dict:
        """Returns information to create the public room list"""
        return {
            **self.info,
            "leader": self.leader.username,
            "players": {
                username: {"display_name": player.display_name}
                for username, player in self.players.items()
            },
        }

    @classmethod
    def get_events(cls) -> dict[str, list[str]]:
        """Recursively get the events from the inheritance tree"""
        events = cls._EVENTS.copy()
        for parent_class in cls.__bases__:
            if issubclass(parent_class, Room):
                dict_merge(events, parent_class.get_events(), overwrite=True)
        return events

    async def preprocess_event(self, event: dict, client: AuthedClientRef) -> None:
        if event["type"] in self.get_events():
            missing_parameters = [
                param for param in self._EVENTS[event["type"]] if param not in event
            ]
            if missing_parameters:
                return await client.send_event(
                    {
                        "error": True,
                        "error_code": "missing_event_parameters",
                        "missing_parameters": missing_parameters,
                    },
                    request=event,
                )
        if event["type"] != "join_room" and client.username not in self.players:
            return await client.send_event(
                {"error": True, "error_code": "client_not_in_room"}, request=event
            )
        print(f"{_h(self.identifier)} Received event {event['type']} from {client}")
        await self._process_event(event=event, client=client)

    async def _process_event(self, event: dict, client: AuthedClientRef) -> None:
        """Processes an event sent by a client"""
        match event["type"]:
            case "join_room":
                await self._join(client, event)
            case "leave_room":
                await self._leave(client, event)
            case "start_game":
                await self._start(client, event)
            case "update_room_details":
                await self._update_room_details(client, event)
            case "send_message":
                if self._ROOM_TYPE == RoomType.STATIC:
                    return await client.send_event(
                        {
                            "error": True,
                            "error_code": "messages_must_be_sent_to_parent",
                        },
                        event,
                    )
                if client.username in self.players_muted:
                    return await client.send_event(
                        {"error": True, "error_code": "muted_from_room"}, event
                    )
                elif client.mute_expires > time.time() or client.mute_expires == -1:
                    return await client.send_event(
                        {"error": True, "error_code": "muted_from_server"}, event
                    )
                contents = re.sub(r"\n{2,}", "\n", event["message"])
                encoded_hash = None
                if settings.message_reporting_secret_key is not None:
                    message_hash = hmac.new(
                        settings.message_reporting_secret_key.encode(),
                        f"{client.username}@@{contents}".encode(),
                        digestmod=hashlib.sha256,
                    ).digest()
                    encoded_hash = base64.b64encode(message_hash).decode()
                message = ChatMessage(
                    identifier=len(self.messages),
                    contents=contents,
                    message_hash=encoded_hash,
                    sender=client.username,
                    time=time.time(),
                    replies_to=event.get("replies_to", None),
                )
                self.messages.append(message)
                await self._broadcast({**{"type": "message_sent"}, **message.dict()})
                if "rid" in event:
                    await client.send_event({"error": False}, event)
                if client.mute_expires < time.time() and client.mute_expires != 0:
                    with Session(database_engine) as session:
                        user = session.exec(
                            select(User).where(User.username == client.username)
                        ).first()
                        user.mute_expires = 0
                        user.mute_reason = ""
                        session.add(user)
                        session.commit()
                    for room in client.rooms:
                        await room._broadcast(
                            {"type": "unmuted_from_server", "player": client.username}
                        )
            case "ban_player":
                if client.username != self.leader.username:
                    return await client.send_event(
                        {"error": True, "error_code": "not_the_leader"}, event
                    )
                if event["username"] not in self.players:
                    return await client.send_event(
                        {"error": True, "error_code": "player_not_in_room"}, event
                    )
                self.players_banned.append(event["username"])
                await self._broadcast(
                    {"type": "banned_from_room", "player": event["username"]},
                    context=event,
                )
                await self._leave(self.players[event["username"]])
            case "unban_player":
                if client.username != self.leader.username:
                    return await client.send_event(
                        {"error": True, "error_code": "not_the_leader"}, event
                    )
                if event["username"] not in self.players_banned:
                    return await client.send_event(
                        {"error": True, "error_code": "player_not_banned"}, event
                    )
                self.players_banned.remove(event["username"])
                await self._broadcast(
                    {"type": "unbanned_from_room", "player": event["username"]},
                    context=event,
                )
            case "mute_player":
                if client.username != self.leader.username:
                    return await client.send_event(
                        {"error": True, "error_code": "not_the_leader"}, event
                    )
                if event["username"] not in self.players:
                    return await client.send_event(
                        {"error": True, "error_code": "player_not_in_room"}, event
                    )
                self.players_muted.append(event["username"])
                await self._broadcast(
                    {"type": "muted_from_room", "player": event["username"]},
                    context=event,
                )
            case "unmute_player":
                if client.username != self.leader.username:
                    return await client.send_event(
                        {"error": True, "error_code": "not_the_leader"}, event
                    )
                if event["username"] not in self.players_muted:
                    return await client.send_event(
                        {"error": True, "error_code": "player_not_muted"}, event
                    )
                self.players_muted.remove(event["username"])
                await self._broadcast(
                    {"type": "unmuted_from_room", "player": event["username"]},
                    context=event,
                )
            case _:
                await client.send_event(
                    {"error": True, "error_code": "unknown_event"}, request=event
                )

    async def _broadcast(
        self, event: dict, per_player_payload: dict = {}, context: dict | None = None
    ) -> None:
        """
        Broadcasts an event to all the clients in the room

        You can also send additional data to individual clients using `per_player_payload` where
        the key is the player's username and the value is the extra data to include

        :param event: The broadcast event
        :param per_player_payload: Additional data to send to individual clients
        :param context: The client's request that caused the broadcast event (if there's one)
        """
        event = self._tweak_event(event, context)
        event["room"] = self.identifier
        for client in self.players.values():
            client_event = dict_merge(
                event, per_player_payload.get(client.username, {}), True, False
            )
            await client.send_event(client_event, request=event)

    def _tweak_event(self, event: dict, context: dict | None = None) -> dict:
        """
        Allows modifying a broadcast event before sending it

        :param event: The broadcast event
        :param context: The client's request that caused the broadcast event (if there's one)
        :return: The broadcast event, modified or not
        """
        return event

    async def _join(self, client: AuthedClientRef, request: dict | None = None) -> None:
        if client.username in self.players:
            return await client.send_event(
                {"error": True, "error_code": "already_in_room"}, request
            )
        if len(self.players) == self._MAX_PLAYERS:
            return await client.send_event(
                {"error": True, "error_code": "room_is_full"}, request
            )
        if self._ROOM_TYPE == RoomType.STATIC and request is not None:
            return await client.send_event(
                {"error": True, "error_code": "can_not_manually_join_child_room"},
                request,
            )
        if client.username in self.players_banned:
            return await client.send_event(
                {"error": True, "error_code": "banned_from_room"}, request
            )
        client.rooms.append(self)
        player = client
        if self._PLAYER_MODEL is not None and self._PLAYER_MODEL != AuthedClientRef:
            player = self._PLAYER_MODEL(**client.dict())
        self.players[player.username] = player
        print(f"{_h(self.identifier)} @{client.username} joined the room")
        if self.leader is None:
            self.leader = player
        await self._broadcast(
            {
                "type": "player_joined",
                "username": player.username,
                "display_name": player.display_name,
                "admin_state": player.admin_state,
                "muted_from_server": player.mute_expires != 0,
            },
            context=request,
        )
        if request is not None:
            await client.send_event(
                {
                    "error": False,
                    "room_name": self.name,
                    "public": self.public,
                    "players": [
                        {
                            "username": p.username,
                            "display_name": p.display_name,
                            "admin_state": player.admin_state,
                            "muted_from_server": p.mute_expires != 0,
                        }
                        for p in self.players.values()
                    ],
                    "banned_players": self.players_banned,
                    "muted_players": self.players_muted,
                    "rules": self._child.rules.dict()
                    if self._ROOM_TYPE == RoomType.DYNAMIC
                    else self.rules.dict(),
                    "game_mode": self._child.__id__
                    if self._ROOM_TYPE == RoomType.DYNAMIC
                    else self.__id__,
                    "leader": self.leader.username,
                    "child_room": self._child.identifier
                    if self._ROOM_TYPE == RoomType.DYNAMIC
                    else None,
                },
                request=request,
            )

    async def _leave(self, client: AuthedClientRef, event: dict | None = None):
        if self._ROOM_TYPE == RoomType.STATIC and event is not None:
            await client.send_event(
                {"error": True, "error_code": "can_not_leave_dynamic_room_manually"}
            )
            return
        await self._on_player_leave(self.players[client.username])
        del self.players[client.username]
        client.rooms.remove(self)
        if event is not None:
            await client.send_event({"error": False}, request=event)
        await self._broadcast({"type": "player_left", "player": client.username})
        print(f"{_h(self.identifier)} @{client.username} left the room")
        if self.state == RoomState.IN_GAME and self._ROOM_TYPE == RoomType.DYNAMIC:
            await self._child._leave(client)
        if self._ROOM_TYPE == RoomType.STATIC:
            return
        if self.leader.username == client.username:
            if self.players:
                # Player was the leader, give leader status to the next player
                self.leader = list(self.players.values())[0]
                await self._broadcast(
                    {"type": "leader_changed", "player": self.leader.username}
                )
            else:
                # There are no players left in the room, delete it
                if self.identifier in rooms:
                    self.state = RoomState.FINISHED
                    del rooms[self.identifier]
                    print(
                        f"{_h(self.identifier)} No players left in room, bailing out. Active rooms: {len(rooms)}"
                    )
                    if self._child is not None:
                        del rooms[self._child.identifier]
                        print(
                            f"{_h(self.identifier)} Deleting child room. Active rooms: {len(rooms)}"
                        )

    async def _on_player_leave(self, player: AuthedClientRef) -> None:
        return

    async def _start(self, client: AuthedClientRef, request: dict):
        """Starts the child room and waits until the game has finished"""
        if self._child is None:
            raise Exception(f"Room with UUID {self.identifier} has no child")
        if client.username != self.leader.username:
            return await client.send_event(
                {"error": True, "error_code": "not_the_leader"}, request
            )
        if len(self.players) < self._MIN_PLAYERS:
            return await client.send_event(
                {"error": True, "error_code": "not_enough_players"}, request
            )

        if len(self.players) > self._MAX_PLAYERS:
            return await client.send_event(
                {"error": True, "error_code": "too_many_players"}, request
            )
        if self.state != RoomState.PRE_GAME:
            return await client.send_event(
                {"error": True, "error_code": "already_started"}, request
            )
        print(f"{_h(self.identifier)} Starting child room")
        self.state = RoomState.IN_GAME
        for player in self.players.values():
            await self._child._join(player)
        await self._broadcast({"type": "child_room_started"}, context=request)
        await self._child._start(client, request)
        await client.send_event({"error": False}, request)
        asyncio.get_running_loop().create_task(self._wait_until_child_has_finished())

    async def _wait_until_child_has_finished(self) -> None:
        while self._child.state != RoomState.FINISHED:
            await asyncio.sleep(0.2)
        if self.state == RoomState.FINISHED:
            return
        print(f"{_h(self.identifier)} Child room finished")
        self.state = RoomState.PRE_GAME
        error = self.create_child_room(
            game_mode_name=self._child.__id__, rules=self._child.rules.dict()
        )
        if error == "finished":
            return
        await self._broadcast(
            {"type": "room_details_updated", "child_room": self._child.identifier}
        )

    def create_child_room(self, game_mode_name: str, rules: dict) -> str:
        if self._ROOM_TYPE != RoomType.DYNAMIC:
            return "not_a_dynamic_room"
        if self.state == RoomState.FINISHED:
            return "finished"
        if self._child is not None and self._child.identifier in rooms:
            del rooms[self._child.identifier]
            print(
                f"{_h(self.identifier)} Child room has finished, deleting it. Active rooms: {len(rooms)}"
            )
        from ichi_server.models.gamemodes import game_modes

        if game_mode_name not in game_modes:
            return "non_existant_game_mode"
        game_mode: Callable = game_modes[game_mode_name]
        if len(self.players) > game_mode._MAX_PLAYERS:
            return "too_many_players"
        self._MIN_PLAYERS = game_mode._MIN_PLAYERS
        self._MAX_PLAYERS = game_mode._MAX_PLAYERS
        self._child = game_mode(
            name="INTERNAL",
            public=False,
            rules=rules,
        )
        self._child._parent = self
        rooms[self._child.identifier] = self._child
        print(f"{_h(self.identifier)} Created child room {self._child.identifier}")
        return "OK"

    async def _update_room_details(
        self, client: AuthedClientRef, new_details: dict
    ) -> None:
        if self._ROOM_TYPE != RoomType.DYNAMIC:
            return await client.send_event(
                {"error": True, "error_code": "not_a_dynamic_room"},
            )
        if client.username != self.leader.username:
            return await client.send_event(
                {"error": True, "error_code": "not_the_leader"}
            )
        broadcast_event = {"type": "room_details_updated"}
        if "room_name" in new_details and type(new_details["room_name"]) is str:
            self.name = new_details["room_name"][:64]
            broadcast_event["room_name"] = self.name
        if "public" in new_details and type(new_details["public"]) is bool:
            self.public = new_details["public"]
            broadcast_event["public"] = self.public
        if "game_mode" in new_details:
            error = self.create_child_room(
                game_mode_name=new_details["game_mode"],
                rules=new_details.get("rules", {}),
            )
            if error != "OK":
                return await client.send_event({"error": True, "error_code": error})
            broadcast_event["child_room"] = self._child.identifier
            broadcast_event["game_mode"] = new_details["game_mode"]
            broadcast_event["rules"] = self._child.rules.dict()
        elif "rules" in new_details:
            self._child.rules = self._child.__dataclass_fields__["rules"].type(
                **new_details["rules"]
            )
            self._child.update_rules()
            broadcast_event["rules"] = self._child.rules.dict()
        await self._broadcast(broadcast_event, context=new_details)

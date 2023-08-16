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

from pydantic import BaseModel
from fastapi import WebSocket

from ichi_server.models.account import UserMinimal


class ClientRef(BaseModel):
    """References an unauthenticated client"""

    address: str
    client_name: str
    websocket: WebSocket | None

    class Config:
        arbitrary_types_allowed = True

    def __str__(self) -> str:
        string = f"Client({self.address}"
        if self.client_name != "Unnamed client":
            string += f", {self.client_name}"
        return string + ")"

    async def send_event(self, event: dict, request: dict | None = None) -> None:
        if self.websocket is None:
            return
        if request is not None:
            if "rid" in request:
                event["rid"] = request["rid"]
            if "room" in request:
                event["room"] = request["room"]
        await self.websocket.send_json(event)


class AuthedClientRef(ClientRef, UserMinimal):
    """References an authenticated client"""

    rooms: list = []

    def __str__(self) -> str:
        string = f"Client({self.username}, {self.address}"
        if self.client_name != "Unnamed client":
            string += f", {self.client_name}"
        return string + ")"

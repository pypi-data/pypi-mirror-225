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

from pydantic import BaseModel, root_validator
from sqlmodel import Field, SQLModel

from ichi_server.models.exceptions import InvalidCAPTCHASolution

_validated_captchas: list[str] = []


class CAPTCHASolution(BaseModel):
    identifier: str
    solution: str

    @root_validator
    def validate_captcha(cls, captcha):
        # Cheap-ass way of solving circular dependencies
        from ichi_server.manager import captchas

        if captcha["identifier"] in _validated_captchas:
            _validated_captchas.remove(captcha["identifier"])
            return captcha
        if not captcha["identifier"] in captchas:
            raise InvalidCAPTCHASolution
        is_valid = captchas[captcha["identifier"]] == captcha["solution"]
        del captchas[captcha["identifier"]]
        if not is_valid:
            raise InvalidCAPTCHASolution
        # Since this function is called once for every field and the
        # CAPTCHA's identifier is removed from the list on the first
        # run, it would cause an InvalidCAPTCHA error on the second run,
        # to fix that the identifier is added to another list so the check
        # is skipped on the second run.
        _validated_captchas.append(captcha["identifier"])
        return captcha


class ChatMessage(BaseModel):
    identifier: int
    contents: str
    sender: str
    time: float
    message_hash: str | None = None
    replies_to: int | None = None


class MessageReport(SQLModel, table=True):
    __tablename__ = "message_reports"
    username: str
    message: str
    message_hash: str = Field(primary_key=True)

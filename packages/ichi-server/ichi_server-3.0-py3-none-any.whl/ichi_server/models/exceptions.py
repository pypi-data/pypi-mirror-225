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

from pydantic import BaseModel, PydanticValueError


class GenericErrorSchema(BaseModel):
    error: bool = True
    error_code: str = "error_code_example"
    error_msg: str = "Error message example"


class ValidationErrorChildSchema(BaseModel):
    error_code: str = "error_code_example"
    error_msg: str = "Error message example"


class ValidationErrorSchema(BaseModel):
    error: bool = True
    error_code: str = "validation_error"
    errors: list[ValidationErrorChildSchema]


class InvalidUsername(PydanticValueError):
    code = "invalid_username"
    msg_template = "An username must be between 1 and 16 characters long and only contain letters, numbers and underscores (_)"


class InvalidDisplayName(PydanticValueError):
    code = "invalid_display_name"
    msg_template = "A display name must be between 1 and 16 characters long"


class InvalidPassword(PydanticValueError):
    code = "invalid_password"
    msg_template = "The provided password does not meet the server's requirements"


class InvalidCAPTCHASolution(PydanticValueError):
    code = "invalid_captcha_solution"
    msg_template = (
        "The provided CAPTCHA solution is wrong or the CAPTCHA does not exist"
    )

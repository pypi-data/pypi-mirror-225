# ichiCAPTCHA: A tool to generate simple CAPTCHA images
# ichiCAPTCHA is part of ichi Server
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

import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from ichi_server.dependencies import RESOURCES_PATH
from ichi_server.manager import game_mode_images_metadata
from ichi_server.models.exceptions import GenericErrorSchema

router = APIRouter(prefix="/game_modes")


@router.get(
    "/{game_mode}/image",
    responses={
        200: {
            "content": {"image/*": {}},
            "description": "The game mode's image metadata",
        },
        404: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "The game mode has no image or does not exist",
        },
    },
)
def get_game_mode_image(game_mode: str):
    path = f"{RESOURCES_PATH}/game_mode_images/{game_mode}.webp"
    if not os.path.exists(path):
        raise HTTPException(
            404, {"error": True, "error_code": "game_mode_has_no_image"}
        )
    return FileResponse(path)


@router.get(
    "/{game_mode}/image/metadata",
    responses={
        200: {
            "content": {"image/*": {}},
            "description": "The game mode's image metadata",
        },
        404: {
            "content": {"application/json": {}},
            "model": GenericErrorSchema,
            "description": "The game mode has no image or does not exist",
        },
    },
)
def get_game_mode_image_metadata(game_mode: str):
    if game_mode not in game_mode_images_metadata:
        raise HTTPException(
            404, {"error": True, "error_code": "game_mode_has_no_image"}
        )
    return game_mode_images_metadata[game_mode]

# ichiCAPTCHA: A tool to generate simple CAPTCHA images
# ichiCAPTCHA is part of ichi Server
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

import math
import re
import os
import string
from base64 import b64encode
from io import BytesIO
from random import choice, choices, randint
from typing import Tuple
from uuid import uuid4

from fastapi import APIRouter, Query, Response
from PIL import Image, ImageDraw, ImageFont, ImageOps

from ichi_server.dependencies import RESOURCES_PATH
from ichi_server.manager import captchas

router = APIRouter(prefix="/captcha", tags=["Authentication", "CAPTCHA"])

POSSIBLE_CHARACTERS = string.ascii_letters + re.sub(r"0|1|5", "", string.digits)


class WaveDeform:
    def transform(self, x, y):
        y = y + randint(10, 20) * math.sin(x / (40 / choice((1, 2))))
        return x, y

    def transform_rect(self, x0, y0, x1, y1):
        return (
            *self.transform(x0, y0),
            *self.transform(x0, y1),
            *self.transform(x1, y1),
            *self.transform(x1, y0),
        )

    def getmesh(self, img) -> list:
        width, height = img.size
        grid_space = 20

        grid = []
        for x in range(0, width, grid_space):
            for y in range(0, height, grid_space):
                grid.append((x, y, x + grid_space, y + grid_space))

        source_grid = [self.transform_rect(*rect) for rect in grid]

        return [i for i in zip(grid, source_grid)]


def _get_random_color(min: int, max: int) -> Tuple[int, int, int]:
    return (randint(min, max), randint(min, max), randint(min, max))


def generate_captcha_image(high_contrast: bool = False) -> Tuple[Image.Image, str]:
    """
    Generates a simple CAPTCHA-like image

    :param high_contrast: Sets the background color to black
    and the text color to yellow also reduces the blurring a bit
    :return: The PIL.Image.Image object and the text as a string
    """
    text = "".join(choices(POSSIBLE_CHARACTERS, k=7))
    # When a lowercase f is to the left of a lowercase 'i' or 'l'
    # both letters would merge making it really hard to read, the lazyest
    # fix to this is making the f letter uppercase
    text = re.sub(r"f(i|l)", r"F\g<1>", text)
    image = Image.new(
        mode="RGB",
        size=(900, 300),
        color=_get_random_color(200, 255) if not high_contrast else "black",
    )
    draw = ImageDraw.Draw(image, mode="RGB")
    captcha_font = ImageFont.truetype(f"{RESOURCES_PATH}/SpaceMono-Regular.ttf", 190)
    draw.text(
        xy=(42, 10),
        text=text,
        fill=_get_random_color(0, 127) if not high_contrast else (255, 255, 0),
        font=captcha_font,
    )
    image = ImageOps.deform(image, WaveDeform())
    if os.path.exists(f"{RESOURCES_PATH}/watermark.png"):
        watermark = Image.open(f"{RESOURCES_PATH}/watermark.png")
        # Invert the watermark colors in high contrast mode
        if high_contrast and watermark.mode == "RGBA":
            r, g, b, a = watermark.split()
            rgb_wm = Image.merge("RGB", (r, g, b))
            inverted_wm = ImageOps.invert(rgb_wm)
            r2, g2, b2 = inverted_wm.split()
            watermark = Image.merge("RGBA", (r2, g2, b2, a))
        elif high_contrast:
            watermark = ImageOps.invert(watermark)
        image.paste(watermark, (0, 0), mask=watermark)

    return image, text


@router.get(
    "",
    responses={
        200: {
            "description": "The CAPTCHA image with it's identifier",
        },
    },
    summary="Get a CAPTCHA image and identifier",
)
async def get_captcha(
    high_contrast: bool = False,
    use_encoded_image: bool = Query(default=False, deprecated=True),
):
    """
    Generates a CAPTCHA image with it's corresponding identifier, used
    for endpoints with a CAPTCHA verification.

    The 'high_contrast' parameter turns the CAPTCHA image's background black and
    foreground yellow.

    The 'use_encoded_image' gives a JSON response with the image encoded in Base64
    and the identifier instead of the later being in a response header
    """
    image, text = generate_captcha_image(high_contrast)
    identifier = str(uuid4())
    while identifier in captchas:
        # Avoid a rare, but possible UUID collision
        identifier = str(uuid4())
    captchas[identifier] = text
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    if use_encoded_image:
        encoded_image = (
            f"data:image/jpeg;base64,{b64encode(buffer.getvalue()).decode()}"
        )
        return {"encoded_image": encoded_image, "identifier": identifier}
    return Response(
        content=buffer.getvalue(),
        media_type="image/jpeg",
        headers={"X-ichi-CAPTCHA": identifier},
    )

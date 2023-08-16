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

from inspect import isclass

from .base import GameRoom
from .ichi import ichi as _ichi
from .ichi import ichi07, ichiDebug
from .debug import RulesSchemaParsingTest, EmptyRulesTest, MultipleCardPiles

from ichi_server.dependencies import settings

game_modes = {
    cls.__id__: cls
    for cls in globals().values()
    if isclass(cls) and issubclass(cls, GameRoom) and cls != GameRoom
    if not cls.__is_debug__ or cls.__is_debug__ and settings.enable_debug_capabilities
}

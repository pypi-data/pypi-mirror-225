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
from pydantic.dataclasses import dataclass
from pydantic.fields import Field

from ichi_server.models.gamemodes.base import (
    Action,
    ActionButton,
    Card,
    CardPileDefinition,
    DiscardCardAction,
    DrawCardAction,
    GameRoom,
    Player,
)


class TestChildRulesA(BaseModel):
    between_10_and_20: int = Field(
        default=10, ge=10, le=20, unit_singular="card", unit_plural="cards"
    )
    higher_or_equal_to_30: int = Field(
        default=30, ge=30, unit_singular="pear", unit_plural="pears"
    )
    units_test: int = Field(
        default=1, unit_singular="<singular>", unit_plural="<plural>"
    )


class TestRules(BaseModel):
    integer: int = 8
    boolean: bool = True

    rules_child_group: TestChildRulesA = TestChildRulesA()


@dataclass
class RulesSchemaParsingTest(GameRoom):
    """A game mode with rules to test rules' schema parsing"""

    __id__ = "schema_parsing_test"
    __fancy_name__ = "Game mode with rules"
    __is_debug__ = True

    rules: TestRules = Field(default_factory=TestRules)

    _MIN_PLAYERS = 10000
    _MAX_PLAYERS = 10000


@dataclass
class EmptyRulesTest(GameRoom):
    """A game mode without rules to test rules' schema parsing"""

    __id__ = "no_rules_test"
    __fancy_name__ = "Game mode without rules"
    __is_debug__ = True

    rules: BaseModel = Field(default_factory=BaseModel)

    _MIN_PLAYERS = 10000
    _MAX_PLAYERS = 10000


@dataclass
class MultipleCardPiles(GameRoom):
    """A game mode with multiple card piles"""

    __id__ = "multiple_piles"
    __fancy_name__ = "Game mode with multiple card piles"
    __is_debug__ = True

    rules: BaseModel = Field(default_factory=BaseModel)
    max_drawable_cards: int = 40
    turn_time: float = 20.0

    _MIN_PLAYERS = 1
    _MAX_PLAYERS = 1
    _CARD_PILE_DEFINITIONS = [
        CardPileDefinition(identifier="draw", clients_can_see_cards=False),
        CardPileDefinition(identifier="discard", clients_can_see_cards=True),
        CardPileDefinition(identifier="discard_alt", clients_can_see_cards=True),
    ]
    _ACTION_BUTTONS = [ActionButton(name="end_game")]

    async def _process_event(self, event: dict, client) -> None:
        match event["type"]:
            case "end_game":
                await self._declare_player_win(self.leader)
            case _:
                return await super()._process_event(event, client)

    async def _after_game_start(self) -> None:
        print(self.max_drawable_cards)
        # This method implementation is an example, replace in the game mode
        for player in self.players.values():
            await self._draw_card(
                amount=4, pile_identifier="draw", forced=True, player=player
            )

    def _get_player_actions(self, player: Player) -> list[Action]:
        """
        Called on turn change for each player, returns a list of
        possible actions the player can do in the turn
        """
        actions: list[Action] = [
            DrawCardAction(card_pile="draw", count=self.max_drawable_cards)
        ]
        for card in player.cards.values():
            actions.append(
                DiscardCardAction(
                    card_identifier=card.identifier,
                    card_piles=["discard", "discard_alt"],
                )
            )
        return actions

    def _can_discard_card(self, card: Card, player: Player) -> list[str]:
        return ["discard", "discard_alt"]

    def _generate_deck(self) -> list[Card]:
        cards: list = []
        for i in range(4):
            for j in range(10):
                cards.append(Card(value=j, uid=i))
        return cards

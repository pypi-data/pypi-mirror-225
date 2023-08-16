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

from collections import deque
from enum import auto
from random import choice

import colorama
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pydantic.fields import Field

from ichi_server.dependencies import StringEnum
from ichi_server.models.client import AuthedClientRef
from ichi_server.models.gamemodes.base import (
    Action,
    ActionButton,
    AddCardToHandAction,
    Card,
    CardPile,
    DiscardCardAction,
    DiscardCardAndSelectPlayerAction,
    DrawCardAction,
    EnableActionButtonAction,
    GameRoom,
    GameStatsExplodedWins,
    Player,
    PlayerState,
    TurnState,
)
from ichi_server.models.misc import ChatMessage


class DiscardCardAndSelectColorAction(DiscardCardAction):
    pass


class ichiPlayer(Player):
    one_card_vulnerable: bool = False
    has_prediscard_protection: bool = False


class ichiCardColor(StringEnum):
    RED = "RED"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    BLACK = "BLACK"


class ichiCardType(StringEnum):
    NUMBER = "NUMBER"
    BLOCK = "BLOCK"
    REVERSE = "REVERSE"
    DRAW_2 = "DRAW_2"
    DRAW_4 = "DRAW_4"
    WILDCARD = "WILDCARD"


class ichiCard(Card):
    value: int | None = None
    color: ichiCardColor
    type: ichiCardType
    wildcard_color: ichiCardColor | str | None = None

    @property
    def identifier(self):
        if self.type == ichiCardType.NUMBER:
            return f"{self.__class__.__name__}~{self.color}-{self.value}-{self.uid}"
        return f"{self.__class__.__name__}~{self.color}-{self.type}-{self.uid}"

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        color = (
            colorama.Fore.__getattribute__(self.color)
            if self.color != ichiCardColor.BLACK
            else ""
        )
        return (
            f"{colorama.Style.BRIGHT}{color}{self.__class__.__name__}(%s){colorama.Style.RESET_ALL}"
            % (self.value if self.type == ichiCardType.NUMBER else self.type.value)
        )


class ichiResult(StringEnum):
    POSITIVE = auto()
    NEGATIVE = auto()


class TwoPlayerRules(BaseModel):
    reverse_acts_as_block: bool = True


class PenalizationRules(BaseModel):
    # Amount of cards to draw if the turn is skipped by the player
    # or the turn time has passed, it's recommended to set this to
    # the same value as `max_draws_per_turn`
    turn_skipped_penalization: int = Field(
        default=2, ge=0, unit_singular="card", unit_plural="cards"
    )
    # Reduces the amount of `turn_skipped_penalization` if the player has already
    # drawn cards, the final amount would be 'turn_skipped_penalization - cards_drawn'
    reduce_turn_skipped_if_already_drawn: bool = True
    ichi_broken_penalization: int = Field(
        default=2, ge=0, unit_singular="card", unit_plural="cards"
    )


class ichiRules(BaseModel):
    # Max number of cards allowed to draw in a turn
    max_draws_per_turn: int = Field(
        default=2, ge=-1, unit_singular="card", unit_plural="cards"
    )
    # Skips the player turn after using all of their draw attempts even
    # if they have drawn a playable card
    skip_turn_after_draw_even_if_cards_playable: bool = False
    # The length of each player's turn in seconds
    turn_time: float = Field(
        default=30.0, ge=5.0, unit_singular="second", unit_plural="seconds"
    )
    cards_at_game_start: int = Field(
        default=7, ge=2, le=10, unit_singular="card", unit_plural="cards"
    )
    can_stack_draw_cards: bool = True
    continue_until_one_player_left: bool = True
    delay_win_if_draw_card_stack_active: bool = True
    allow_saying_ichi_with_two_cards: bool = True

    penalization_rules: PenalizationRules = PenalizationRules()

    two_player_rules: TwoPlayerRules = TwoPlayerRules()


@dataclass
class ichi(GameRoom):
    """
    The default and original game mode for ichi.

    An UNO card game clone with support for up to 10 players
    """

    __id__ = "ichi"
    __fancy_name__ = "ichi"

    _ACTION_BUTTONS = [
        ActionButton(name="say_ichi"),
        ActionButton(name="skip_turn", conditional=True),
    ]
    _PLAYER_MODEL = ichiPlayer
    _STATS_MODEL = GameStatsExplodedWins

    rules: ichiRules = Field(default_factory=ichiRules)
    _block_next_turn = False
    _current_draw_card_stack = 0
    _turn_rotation = -1  # -1 is normal order, 1 is inverted

    async def _process_event(self, event: dict, client: AuthedClientRef):
        match event["type"]:
            case "say_ichi":
                await self._say_ichi(player=self.players[client.username], event=event)
            case _:
                await super()._process_event(event, client)

    def _tweak_event(self, event: dict, context: dict | None = None) -> dict:
        if event["type"] == "card_discarded" and context is not None:
            if self.deck[event["card"]].type in [
                ichiCardType.WILDCARD,
                ichiCardType.DRAW_4,
            ]:
                event["color"] = self.deck[event["card"]].wildcard_color
        return event

    def update_rules(self):
        self.turn_time = self.rules.turn_time
        self.max_drawable_cards = self.rules.max_draws_per_turn

    async def _before_turn_rotation(self) -> None:
        await super()._before_turn_rotation()
        if self.turn_state in (TurnState.SKIPPED, TurnState.TIMED_OUT):
            cards_to_draw = self.rules.penalization_rules.turn_skipped_penalization
            # Reduce the penalization cards if already drawn and rule is enabled
            if self.rules.penalization_rules.reduce_turn_skipped_if_already_drawn:
                cards_to_draw -= self.drawn_cards
            # Add the cards of the current draw card stack
            if self._current_draw_card_stack:
                cards_to_draw += self._current_draw_card_stack
                await self._reset_card_stack()
            await self._draw_card(
                amount=cards_to_draw,
                pile_identifier="draw",
                forced=True,
                player=self.current_turn,
            )
        elif self.current_turn is not None and len(self.current_turn.cards) == 0:
            if (
                self._current_draw_card_stack > 0
                and self.rules.delay_win_if_draw_card_stack_active
            ):
                self.current_turn.state = PlayerState.ABOUT_TO_WIN
            else:
                await self._declare_player_win(self.current_turn)

    def _do_turn_rotation(self) -> None:
        for _ in self.players:
            self.turn_order.rotate(self._turn_rotation)
            self.current_turn = self.turn_order[0]
            if self.current_turn.state in (
                PlayerState.ABOUT_TO_WIN,
                PlayerState.PLAYING,
            ):
                if self._block_next_turn:
                    self._block_next_turn = False
                    continue
                break

    async def _after_turn_rotation(self) -> None:
        if self._current_draw_card_stack > 0 and (
            not self.rules.can_stack_draw_cards
            or not self._can_player_continue_stack(self.current_turn)
        ):
            await self._draw_card(
                self._current_draw_card_stack,
                pile_identifier="draw",
                forced=True,
                player=self.current_turn,
            )
            await self._reset_card_stack()

    def _generate_deck(self) -> list[ichiCard]:
        deck = []
        for color in (
            ichiCardColor.RED,
            ichiCardColor.BLUE,
            ichiCardColor.YELLOW,
            ichiCardColor.GREEN,
        ):
            # Generate number cards
            for value in range(10):  # Value of the card
                for i in range(2 if value != 0 else 1):  # Number of cards to generate
                    deck.append(
                        ichiCard(
                            color=color, type=ichiCardType.NUMBER, value=value, uid=i
                        )
                    )
            # Block, switch and +2 cards
            for i in range(2):
                deck.append(ichiCard(color=color, type=ichiCardType.BLOCK, uid=i))
                deck.append(ichiCard(color=color, type=ichiCardType.REVERSE, uid=i))
                deck.append(ichiCard(color=color, type=ichiCardType.DRAW_2, uid=i))
        for i in range(4):
            # Wildcards and +4 cards
            deck.append(
                ichiCard(color=ichiCardColor.BLACK, type=ichiCardType.DRAW_4, uid=i)
            )
            deck.append(
                ichiCard(color=ichiCardColor.BLACK, type=ichiCardType.WILDCARD, uid=i)
            )
        return deck

    async def _after_game_start(self) -> None:
        for player in self.players.values():
            if player.state == PlayerState.SPECTATOR:
                continue
            await self._draw_card(
                amount=self.rules.cards_at_game_start,
                pile_identifier="draw",
                forced=True,
                player=player,
            )

    async def _before_card_is_discarded(
        self, card: ichiCard, pile: CardPile, client: ichiPlayer, request: dict
    ) -> None:
        if (
            card.type not in [ichiCardType.DRAW_2, ichiCardType.DRAW_4]
            and self._current_draw_card_stack > 0
        ):
            await self._draw_card(
                amount=self._current_draw_card_stack,
                pile_identifier="draw",
                forced=True,
                player=client,
            )
            await self._reset_card_stack()
        match card.type:
            case ichiCardType.DRAW_2:
                self._current_draw_card_stack += 2
            case ichiCardType.DRAW_4 | ichiCardType.WILDCARD:
                if (
                    not "color" in request
                    or request["color"] is None
                    or not hasattr(ichiCardColor, request["color"].upper())
                ):
                    # Color is not specified or is invalid, select a random one
                    card.wildcard_color = choice(ichiCardColor._member_names_)
                else:
                    card.wildcard_color = request["color"].upper()
                if card.type == ichiCardType.DRAW_4:
                    self._current_draw_card_stack += 4
            case ichiCardType.BLOCK:
                self._block_next_turn = True
            case ichiCardType.REVERSE:
                if (
                    len(self.active_players) == 2
                    and self.rules.two_player_rules.reverse_acts_as_block
                ):
                    self._block_next_turn = True
                else:
                    self._turn_rotation = -self._turn_rotation
        client.one_card_vulnerable = (
            not client.has_prediscard_protection and len(client.cards) == 1
        )
        if client.has_prediscard_protection:
            client.has_prediscard_protection = False

    async def _get_drawn_card_actions(
        self, card: ichiCard, player: ichiPlayer, forced: bool, event: dict | None
    ) -> tuple[ichiCard, list[Action]]:
        if not forced and self._current_draw_card_stack > 0:
            await self._draw_card(
                amount=self._current_draw_card_stack,
                pile_identifier="draw",
                forced=True,
                player=player,
            )
            await self._reset_card_stack()
        # Clear the color of the wildcard cards
        if card.type in (ichiCardType.DRAW_4, ichiCardType.WILDCARD):
            card.wildcard_color = None
        # Player is vulnerable, i.e. only has one card and didn't say 'ichi'
        # Since they have drawn a card it would make them invulnerable
        if player.one_card_vulnerable:
            player.one_card_vulnerable = False
        if player.has_prediscard_protection:
            player.has_prediscard_protection = False
        # Somebody got fucked with a draw card stack
        if player.state == PlayerState.ABOUT_TO_WIN:
            player.state = PlayerState.PLAYING
        actions: list[Action] = [AddCardToHandAction()]
        valid_card_piles: list[str] = self._can_discard_card(card, player)
        if valid_card_piles:
            action, params = self._get_discard_action_for_card(card, player)
            actions.append(action(card_piles=valid_card_piles, **params))
        return (card, actions)

    async def _on_player_win(self, player: ichiPlayer) -> None:
        """Called when a player wins, checks for the number of active players"""
        if self.rules.continue_until_one_player_left and len(self.active_players) > 1:
            return
        await self._declare_game_finished()

    async def _say_ichi(self, player: ichiPlayer, event: dict) -> None:
        vulnerable_players = [
            _player
            for _player in self.players.values()
            if _player.one_card_vulnerable and player.username != _player.username
        ]
        affected_players: dict[str, ichiResult] = {
            player.username: ichiResult.NEGATIVE for player in vulnerable_players
        }
        set_prediscard_protection = False
        if (
            self.rules.allow_saying_ichi_with_two_cards
            and len(player.cards) == 2
            and self.current_turn == player
            and self.turn_state == TurnState.STARTED
            and not player.has_prediscard_protection
        ):
            set_prediscard_protection = True
            player.has_prediscard_protection = True
            affected_players[player.username] = ichiResult.POSITIVE
        if (
            not vulnerable_players
            and not player.one_card_vulnerable
            and not set_prediscard_protection
        ):
            return await player.send_event(
                {"error": True, "error_code": "nobody_is_vulnerable"}, request=event
            )
        if player.one_card_vulnerable:
            player.one_card_vulnerable = False
            affected_players[player.username] = ichiResult.POSITIVE
        await self._broadcast(
            {
                "type": "ichi_said",
                "player": player.username,
                "affected_players": affected_players,
            }
        )
        # Apply penalty on vulnerable players
        for vulnerable_player in vulnerable_players:
            vulnerable_player.one_card_vulnerable = False
            await self._draw_card(
                amount=self.rules.penalization_rules.ichi_broken_penalization,
                pile_identifier="draw",
                forced=True,
                player=vulnerable_player,
            )
        await player.send_event({"error": False}, request=event)

    async def _reset_card_stack(self) -> None:
        self._current_draw_card_stack = 0
        await self._broadcast({"type": "draw_card_stack_reset"})
        for player in sorted(self.players.values(), key=lambda x: x.last_state_change):
            if player.state == PlayerState.ABOUT_TO_WIN:
                await self._declare_player_win(player)

    def _get_player_actions(self, player: ichiPlayer) -> list[Action]:
        actions = []
        if self.current_turn.username == player.username:
            actions.append(EnableActionButtonAction(button_identifier="skip_turn"))
            actions.append(
                DrawCardAction(card_pile="draw", count=self.rules.max_draws_per_turn)
            )
            for identifier, card in player.cards.items():
                card_piles: list[str] = self._can_discard_card(card, player)
                if card_piles:
                    action, params = self._get_discard_action_for_card(card, player)
                    actions.append(
                        action(
                            card_identifier=identifier, card_piles=card_piles, **params
                        )
                    )

        return actions

    def _get_discard_action_for_card(
        self, card: ichiCard, player: ichiPlayer
    ) -> tuple[Action, dict]:
        action = DiscardCardAction
        if card.type in [ichiCardType.WILDCARD, ichiCardType.DRAW_4]:
            action = DiscardCardAndSelectColorAction
        return action, {}

    def _is_card_valid_as_first(self, card: ichiCard) -> bool:
        # Only number cards can be valid as the first drawn card
        return card.type == ichiCardType.NUMBER

    def _can_discard_card(
        self, card: ichiCard, player: ichiPlayer, ignore_turn_state: bool = False
    ) -> list[str]:
        current_card: ichiCard = self.card_piles["discard"].cards[-1]
        card_piles: list[str] = []
        if (
            # Same color
            current_card.color == card.color
            # Same color as wildcard color
            or current_card.wildcard_color == card.color
            # Special cards
            or card.color == ichiCardColor.BLACK
            # Same value (number)
            or card.type == ichiCardType.NUMBER
            and card.value == current_card.value
            # Same type (excluding numbers)
            or card.type != ichiCardType.NUMBER
            and card.type == current_card.type
        ) and (
            (
                self.current_turn is not None
                and self.current_turn.username == player.username
                and self.turn_state in [TurnState.WAITING, TurnState.STARTED]
            )
            or ignore_turn_state
        ):
            card_piles.append("discard")
        return card_piles

    def _can_player_continue_stack(self, player: ichiPlayer) -> bool:
        return any(
            [
                self._can_discard_card(card, player, ignore_turn_state=True)
                for card in player.cards.values()
                if card.type in (ichiCardType.DRAW_2, ichiCardType.DRAW_4)
            ]
        )


class ichi07Rules(ichiRules):
    can_discard_0_or_7_as_the_last_card: bool = True


@dataclass
class ichi07(ichi):
    """
    An alternative version of ichi where discarding a 0 card will swap everyone's cards
    and discarding a 7 card will let you swap cards with another player
    """

    __id__ = "ichi07"
    __fancy_name__ = "ichi-0-7"

    rules: ichi07Rules = Field(default_factory=ichi07Rules)

    async def _after_card_is_discarded(
        self, card: ichiCard, pile: CardPile, client: ichiPlayer, request: dict
    ) -> None:
        if len(client.cards) == 0:
            await self._declare_player_win(client)
            if len(self.active_players) == 1 or card.value == 7:
                return
        match card.value:
            case 0:
                player_list = self.turn_order.copy()
                if self._turn_rotation == 1:
                    # Order is inversed, reverse the list
                    player_list.reverse()
                    player_list.rotate(1)
                player_states = deque(
                    [
                        (
                            player.cards,
                            player.one_card_vulnerable,
                            player.has_prediscard_protection,
                        )
                        for player in player_list
                        if player in self.active_players
                    ]
                )
                player_states.rotate(self._turn_rotation)
                for index, player_state in enumerate(player_states):
                    player = player_list[index]
                    (
                        player.cards,
                        player.one_card_vulnerable,
                        player.has_prediscard_protection,
                    ) = player_state
                await self._broadcast(
                    {
                        "type": "hands_swapped",
                        "players": {
                            player.username: {"card_amount": len(player.cards)}
                            for player in player_list
                        },
                    },
                    per_player_payload={
                        player.username: {
                            "players": {
                                player.username: {"cards": list(player.cards.keys())}
                            }
                        }
                        for player in self.active_players
                    },
                )
            case 7:
                other_players = [
                    p.username for p in self.active_players if p != client.username
                ]
                selected_player = request.get("player", choice(other_players))
                if selected_player not in other_players:
                    selected_player = choice(other_players)
                await self._swap_players_hands(client, self.players[selected_player])

    def _get_discard_action_for_card(
        self, card: ichiCard, player: ichiPlayer
    ) -> tuple[Action, dict]:
        params = {}
        action = DiscardCardAction
        if card.type in [ichiCardType.WILDCARD, ichiCardType.DRAW_4]:
            action = DiscardCardAndSelectColorAction
        if card.value == 7:
            action = DiscardCardAndSelectPlayerAction
            params = {
                "players": [
                    p.username
                    for p in self.active_players
                    if p.username != player.username
                ]
            }
        return action, params

    def _can_discard_card(
        self, card: ichiCard, player: ichiPlayer, ignore_turn_state: bool = False
    ) -> list[str]:
        initial_veredict = super()._can_discard_card(card, player, ignore_turn_state)
        if (
            card.value in [0, 7]
            and len(player.cards) == 1
            and not self.rules.can_discard_0_or_7_as_the_last_card
        ):
            return []
        return initial_veredict

    async def _after_card_drawn(
        self,
        cards: list[ichiCard],
        card_pile: CardPile,
        forced: bool,
        player: ichiPlayer,
    ) -> None:
        first_card = next(iter(player.cards.values()))
        if (
            self.current_turn == player
            and self.turn_state == TurnState.STARTED
            and len(player.cards) - len(cards) == 1
            and first_card.value in [0, 7]
            and not self.rules.can_discard_0_or_7_as_the_last_card
        ):
            # Player couldn't discard their 0/7 card because of the rule, but since
            # they have drawn a card they can discard it now, however since the clients
            # only know what cards they can discard at turn change, an event containing
            # the new action must be sent
            action, params = self._get_discard_action_for_card(first_card, player)
            await player.send_event(
                {
                    "type": "action_available",
                    "action": action(
                        card_identifier=first_card.identifier,
                        card_piles=self._can_discard_card(first_card, player),
                        **params,
                    ).dict(),
                    "room": self.identifier,
                }
            )

    async def _swap_players_hands(
        self, player1: ichiPlayer, player2: ichiPlayer
    ) -> None:
        player1.one_card_vulnerable, player2.one_card_vulnerable = (
            player2.one_card_vulnerable,
            player1.one_card_vulnerable,
        )
        player1.has_prediscard_protection, player2.has_prediscard_protection = (
            player2.has_prediscard_protection,
            player1.has_prediscard_protection,
        )
        return await super()._swap_players_hands(player1, player2)


class ichiDebugRules(ichiRules):
    max_draws_per_turn: int = 30000
    autoplay_draws_on_turn: int = 4


@dataclass
class ichiDebug(ichi):
    """A single player version of ichi for testing purposes"""

    __id__ = "ichi_debug"
    __fancy_name__ = "ichi Debug"
    __is_debug__ = True

    _ACTION_BUTTONS = [
        ActionButton(name="say_ichi"),
        ActionButton(name="skip_turn", conditional=True),
        ActionButton(name="draw_10_cards"),
        ActionButton(name="get_player_state"),
    ]
    _MIN_PLAYERS = 1
    _MAX_PLAYERS = 1

    rules: ichiDebugRules = Field(default_factory=ichiDebugRules)
    _autoplay_started = False

    def __post_init__(self):
        return super().__post_init__()

    async def _process_event(self, client: ichiPlayer, event: dict):
        match event["type"]:
            case "draw_10_cards":
                await self._draw_card(10, "draw", True, self.players[client.username])
                self.turn_state = TurnState.PLAYED
                await self._change_turn()
            case "get_player_state":
                player: ichiPlayer = self.players[client.username]
                message = ChatMessage(
                    identifier=len(self.messages),
                    contents=f"""
                    State: {player.state}
                    Turn state: {self.turn_state}
                    Vulnerable: {player.one_card_vulnerable}
                    PD Protection: {player.has_prediscard_protection}""",
                    sender=list(self.players.keys())[0],
                    time=0,
                    replies_to=None,
                )
                self.messages.append(message)
                await self._parent._broadcast(
                    {"type": "message_sent", **message.dict()}
                )
            case _:
                await super()._process_event(event, client)

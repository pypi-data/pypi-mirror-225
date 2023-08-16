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
import os
import re
import time
from collections import deque
from copy import deepcopy
from enum import Enum, auto
from random import shuffle
from typing import Any, Iterator

from pydantic import BaseModel, validator
from pydantic.dataclasses import dataclass
from pydantic.fields import Field
from sqlmodel import Session, select

from ichi_server.dependencies import StringEnum
from ichi_server.manager import database_engine, game_mode_images_metadata
from ichi_server.models.account import User
from ichi_server.models.client import AuthedClientRef
from ichi_server.models.room import Room, RoomState, RoomType


class Card(BaseModel):
    value: int
    uid: int = 0  # Set in case two cards have the same parameters

    @property
    def identifier(self):
        return f"{self.__class__.__name__}~{self.value}-{self.uid}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        return {**super().dict(), "identifier": self.identifier}


class PlayerState(StringEnum):
    SPECTATOR = "SPECTATOR"
    IDLE = "IDLE"
    READY = "READY"
    PLAYING = "PLAYING"
    ABOUT_TO_WIN = "ABOUT_TO_WIN"
    WON = "WON"


class Player(AuthedClientRef):
    """Used in game rooms"""

    cards: dict[str, Card] = {}
    state: PlayerState = PlayerState.IDLE
    play_time: float = 0.0
    last_state_change = 0.0
    win_position: int = 9999
    updated_stats: bool = False

    @validator("state")
    def on_change_state(cls, v):
        # A bit of a hacky solution, but it works
        cls.last_state_change = time.time()
        return v


class ClientLayout(StringEnum):
    """The recommended GUI layout for the clients to use"""

    CLASSIC = "classic"


class TurnState(Enum):
    DUMMY = -1
    WAITING = 0
    STARTED = 1
    PLAYED = 2
    SKIPPED = 3
    TIMED_OUT = 4


class Action(BaseModel):
    @classmethod
    @property
    def identifier(cls) -> str:
        return re.sub(
            r"([A-Z])([^A-Z]+)", r"\1\2_", cls.__name__.removesuffix("Action")
        ).lower()[:-1]

    def dict(self, *_a, **_k) -> dict:
        return {"identifier": self.identifier, **super().dict(exclude_none=True)}


class AddCardToHandAction(Action):
    pass


class DiscardCardAction(Action):
    card_identifier: str | None = None
    card_piles: list[str]


class DiscardCardAndSelectPlayerAction(DiscardCardAction):
    players: list[str]


class DrawCardAction(Action):
    card_pile: str
    count: int


class ReplaceCardInHandAction(Action):
    card_identifier: str
    replace_with: str


class EnableActionButtonAction(Action):
    button_identifier: str


class ActionButton(BaseModel):
    name: str
    conditional: bool = False


class GameStatsBasic(BaseModel):
    time_played: float = 0.0
    games_played: int = 0

    @classmethod
    def identifier(cls):
        return cls.__name__.lower().replace("gamestats", "")

    def dict(self):
        return {**super().dict(), "model": self.identifier()}


class GameStatsBasicWins(GameStatsBasic):
    wins: int = 0


class GameStatsExplodedWins(GameStatsBasic):
    top_1_wins: int = 0
    top_2_wins: int = 0
    top_3_wins: int = 0
    other_wins: int = 0


class RefillProvider(StringEnum):
    CARD_PILE = auto()
    PLAYER = auto()


class CardPileDefinition(BaseModel):
    identifier: str
    clients_can_see_cards: bool


class CardPile(CardPileDefinition):
    cards: list[Card] = []

    def __iter__(self) -> Iterator[Card]:
        return self.cards.__iter__()

    def __len__(self) -> int:
        return self.cards.__len__()

    def add(self, card: Card | list[Card]) -> None:
        if type(card) is list:
            return self.cards.extend(card)
        return self.cards.append(card)

    def get(self, index: int = 0) -> Card:
        return self.cards.pop(index)

    def clear(self, return_cards: bool = True) -> list[Card] | None:
        """Clears the internal card list"""
        if return_cards:
            return [self.cards.pop() for _ in range(len(self.cards))]
        self.cards.clear()

    def shuffle(self) -> None:
        shuffle(self.cards)

    @property
    def state(self) -> dict:
        return {
            "identifier": self.identifier,
            "cards": [card.identifier for card in self.cards]
            if self.clients_can_see_cards
            else len(self.cards),
        }


@dataclass
class GameRoom(Room):
    # The game mode's identifier
    __id__ = "game_template"
    # The game mode's name
    __fancy_name__ = "Game mode template"
    __is_debug__ = False

    # Game mode constants
    _ACTION_BUTTONS = []  # A list with the possible actions
    _CARD_PILE_DEFINITIONS = [
        CardPileDefinition(
            identifier="draw",
            clients_can_see_cards=False,
        ),
        CardPileDefinition(
            identifier="discard",
            clients_can_see_cards=True,
        ),
    ]
    _CLIENT_LAYOUT = ClientLayout.CLASSIC
    # A dictionary containing events with their required parameters.
    # There's no need to add events that don't have any required parameter.
    _EVENTS = {
        "discard_card": ["card", "card_pile"],
        "draw_card": ["card_pile"],
    }
    _ENABLE_TURN_TIME = False
    _PLAYER_MODEL = Player  # The model to use for players
    _STATS_MODEL = GameStatsBasic  # The model to use for player's game stats

    rules: BaseModel = Field(default_factory=BaseModel)
    turn_state: TurnState = TurnState.DUMMY
    # Turn-related variables
    current_turn: Player | None = None
    turn_order: deque = Field(default_factory=deque)
    turn_start_timeout: float = 15.0
    turn_time: float = 10.0
    last_turn_change: float = 0
    turn_watchdog_enabled: bool = True
    # How much the turn watchdog waits between checks
    turn_watchdog_sleep: float = 0.05
    drawn_cards: int = 0
    # Maximum number of cards a player can draw in their turn, set to
    # 0 to disable drawing or -1 to have no limit on how much cards can
    # be drawn
    max_drawable_cards: int = 0
    # Skips the player turn if draw_cards reaches max_drawable_cards even
    # if they have a playable card
    skip_turn_when_cards_drawn: bool = False
    # Card piles
    deck: dict[str, Card] = Field(default_factory=dict)
    card_piles: dict[str, CardPile] = Field(default_factory=dict, init=False)
    # Variables mainly used for statistics
    start_time: float = 0.0
    end_time: float = 0.0
    players_that_won: int = 0

    # DO NOT CHANGE IN CHILD CLASSES
    _ROOM_TYPE = RoomType.STATIC
    _parent = None

    def __post_init__(self):
        super().__post_init__()
        if self.__id__ == "game_template" and "ICHI_TEST_ENVIRONMENT" not in os.environ:
            raise Exception("Can't create a game room with the template")
        if not re.match(r"^\w+$", self.__id__):
            raise Exception(
                f"Illegal game mode's __id__ ({self.__id__}): can only contain letters, numbers and underscores"
            )
        for pile_definition in self._CARD_PILE_DEFINITIONS:
            self.card_piles[pile_definition.identifier] = CardPile(
                **pile_definition.dict()
            )
        self.update_rules()

    @classmethod
    def get_gamemode_metadata(cls) -> dict[str, Any]:
        doc = cls.__doc__ if cls.__doc__ is not None else ""
        return {
            "name": cls.__fancy_name__,
            "id": cls.__id__,
            "description": " ".join(doc.split("\n"))
            .replace("    ", "")
            .replace("  ", " ")
            .strip(),
            "debug": cls.__is_debug__,
            "has_image": cls.__id__ in game_mode_images_metadata,
            "meta": {
                "action_buttons": [a.dict() for a in cls._ACTION_BUTTONS],
                "card_piles": [p.dict() for p in cls._CARD_PILE_DEFINITIONS],
                "layout": cls._CLIENT_LAYOUT,
                "min_players": cls._MIN_PLAYERS,
                "max_players": cls._MAX_PLAYERS,
                "rules_schema": cls.rules.default_factory.schema(False),
            },
        }

    @property
    def info(self) -> dict:
        """Returns information given to clients on room creation"""
        return {
            "room_identifier": self.identifier,
            "game_mode": self.__id__,
            "room_type": "static",
        }

    @property
    def active_players(self) -> list[Player]:
        """
        List of currently active players (i.e. the players currently playing)
        """
        return [
            player
            for player in self.players.values()
            if player.state in [PlayerState.PLAYING, PlayerState.ABOUT_TO_WIN]
        ]

    async def _process_event(self, event: dict, client: AuthedClientRef) -> None:
        match event["type"]:
            case "discard_card":
                await self._discard_card(
                    card_identifier=event["card"],
                    pile_identifier=event["card_pile"],
                    player=self.players[client.username],
                    event=event,
                )
            case "draw_card":
                await self._draw_card(
                    amount=1,
                    pile_identifier=event["card_pile"],
                    forced=False,
                    player=self.players[client.username],
                    event=event,
                )
            case "start_turn":
                if self.current_turn.username != client.username:
                    return await client.send_event(
                        {"error": True, "error_code": "not_your_turn"}, request=event
                    )
                self.turn_state = TurnState.STARTED
                self.last_turn_change = time.time()
                await self._broadcast({"type": "turn_started"})
            case "skip_turn":
                if self.current_turn.username != client.username:
                    return await client.send_event(
                        {"error": True, "error_code": "not_your_turn"}, request=event
                    )
                self.turn_state = TurnState.SKIPPED
                await self._change_turn()
            case _:
                # Check for the rest of events
                await super()._process_event(event, client)

    def update_rules(self):
        pass

    async def _join(self, client: AuthedClientRef, request: dict | None = None) -> None:
        if self.state != RoomState.PRE_GAME:
            return await client.send_event(
                {"error": True, "error_code": "already_started"}, request=request
            )
        return await super()._join(client, request)

    async def _leave(self, client: AuthedClientRef, event: dict | None = None):
        if self.state == RoomState.IN_GAME:
            self._update_player_stats(self.players[client.username])
        if len(self.players) - 1 < self._MIN_PLAYERS:
            await self._declare_game_finished(abrupt_finish=True)
        else:
            if self.current_turn.username == client.username:
                await self._change_turn()
            await self._refill_card_pile(
                card_pile=self.card_piles["discard"],
                refill_from=self.players[client.username],
            )
        return await super()._leave(client, event)

    async def _start(self, client: Player, event: dict) -> None:
        """Starts the game room"""
        if client.username != self.leader.username:
            return await client.send_event(
                {"error": True, "error_code": "not_the_leader"}, request=event
            )
        if len(self.players) < self._MIN_PLAYERS:
            return await client.send_event(
                {"error": True, "error_code": "not_enough_players"}, request=event
            )
        if self.state != RoomState.PRE_GAME:
            return await client.send_event(
                {"error": True, "error_code": "already_started"}, request=event
            )
        self.state = RoomState.IN_GAME
        self.start_time = time.time()
        # Generate a deck and shuffle it
        self.deck = {card.identifier: card for card in self._generate_deck()}
        # Set the turn order
        self.turn_order = deque(self.players.values())
        shuffle(self.turn_order)
        # Select the first card
        # Set the state of the room and the clients
        for player in self.players.values():
            if player.state != PlayerState.SPECTATOR:
                player.state = PlayerState.PLAYING
        await self._before_game_start()
        await self._broadcast(
            {
                "type": "game_started",
                "deck": {card.identifier: card.dict() for card in self.deck.values()},
                "turn_order": [player.username for player in self.turn_order],
                "card_piles": [
                    card_pile.state for card_pile in self.card_piles.values()
                ],
            }
        )
        await self._after_game_start()
        asyncio.get_running_loop().create_task(self._turn_watchdog())
        self.turn_order.rotate(-1)
        await self._change_turn()

    async def _before_game_start(self) -> None:
        """
        Called at the start of the game before the `game_started` event
        has been sent to the clients.
        """
        # Add all deck cards to the draw pile and shuffle it
        self.card_piles["draw"].add([*self.deck.values()])
        self.card_piles["draw"].shuffle()
        # Add a card to the discard pile
        for _ in range(len(self.card_piles["draw"])):
            first_card = self.card_piles["draw"].get()
            if self._is_card_valid_as_first(first_card):
                self.card_piles["discard"].add(first_card)
                break
            # Card is not valid, add it back to the draw pile
            self.card_piles["draw"].add(first_card)
        if len(self.card_piles["discard"]) == 0:
            raise Exception("Failed to pick first card")

    async def _after_game_start(self) -> None:
        """
        Called at the start of the game after the `game_started` event
        has been sent to the clients.
        """
        for player in self.players.values():
            if player.state == PlayerState.SPECTATOR:
                continue
            await self._draw_card(
                amount=1, pile_identifier="draw", forced=True, player=player
            )

    async def _change_turn(self) -> None:
        """
        Rotates the turn to the next player
        """
        await self._before_turn_rotation()
        if self.state == RoomState.FINISHED:
            return
        self._do_turn_rotation()
        self.turn_state = TurnState.WAITING
        self.last_turn_change = time.time()
        self.drawn_cards = 0
        await self._after_turn_rotation()
        await self._broadcast(
            {
                "type": "turn_changed",
                "player": self.current_turn.username,
                "turn_duration": self.turn_time,
                "turn_start_timeout": self.turn_start_timeout,
            },
            per_player_payload={
                player.username: {
                    "actions": [a.dict() for a in self._get_player_actions(player)]
                }
                for player in self.players.values()
                if player.state in [PlayerState.ABOUT_TO_WIN, PlayerState.PLAYING]
            },
        )

    async def _before_turn_rotation(self) -> None:
        """Called before the turn is rotated to the next player"""
        if len(self.card_piles["draw"]) == 0:
            await self._refill_card_pile(
                card_pile=self.card_piles["draw"],
                refill_from=self.card_piles["discard"],
            )

    def _do_turn_rotation(self) -> None:
        """Rotates to the next player in the queue."""
        for _ in self.players:
            self.turn_order.rotate(-1)
            self.current_turn = self.turn_order[0]
            if self.current_turn.state in [
                PlayerState.ABOUT_TO_WIN,
                PlayerState.PLAYING,
            ]:
                break

    async def _after_turn_rotation(self) -> None:
        """
        Called after the turn is rotated but before the
        turn_changed event is sent
        """
        pass

    async def _turn_watchdog(self) -> None:
        """Enforces turns timeouts"""
        while self.state != RoomState.FINISHED:
            if (
                self.turn_state == TurnState.STARTED
                and self.turn_time > 0.0
                and time.time() - self.last_turn_change >= self.turn_time
                or self.turn_state == TurnState.WAITING
                and time.time() - self.last_turn_change >= self.turn_start_timeout
            ):
                self.turn_state = TurnState.TIMED_OUT
                self.last_turn_change = time.time()
                await self._change_turn()
            await asyncio.sleep(self.turn_watchdog_sleep)

    async def _discard_card(
        self, card_identifier: str, pile_identifier: str, player: Player, event: dict
    ):
        if self.current_turn.username != player.username:
            return await player.send_event(
                {"error": True, "error_code": "not_your_turn"}, request=event
            )
        if self.turn_state != TurnState.STARTED:
            return await player.send_event(
                {"error": True, "error_code": "turn_not_started"}, request=event
            )
        if card_identifier not in player.cards:
            return await player.send_event(
                {"error": True, "error_code": "card_not_in_hand"}, request=event
            )
        if pile_identifier not in self.card_piles:
            return await player.send_event(
                {"error": True, "error_code": "non_existant_pile"}, request=event
            )
        card = player.cards[card_identifier]
        valid_card_piles: list[str] = self._can_discard_card(card, player)
        if not valid_card_piles or pile_identifier not in valid_card_piles:
            return await player.send_event(
                {"error": True, "error_code": "cant_discard_card"}, request=event
            )
        self.turn_state = TurnState.PLAYED
        # Remove the card from the player's hand
        del player.cards[card.identifier]
        await self._before_card_is_discarded(
            card, self.card_piles[pile_identifier], player, event
        )
        self.card_piles[pile_identifier].add(card)
        await self._broadcast(
            {
                "type": "card_discarded",
                "card": card.identifier,
                "card_pile": pile_identifier,
                "player": player.username,
            },
            context=event,
        )
        await self._after_card_is_discarded(
            card, self.card_piles[pile_identifier], player, event
        )
        await player.send_event({"error": False}, request=event)
        await self._change_turn()

    async def _draw_card(
        self,
        amount: int,
        pile_identifier: str,
        forced: bool,
        player: Player,
        event: dict | None = None,
    ) -> None:
        """
        Draws an `amount` number of cards from a `pile` to `client`'s hand

        :param amount: The number of cards to draw
        :param pile: The pile to draw the cards from
        :param forced: True if the action was not requested by `client`
        :param client: The client to add the drawn cards to
        :param event: The `draw_card` request event, None if `forced` is True
        """
        if self.current_turn != player and not forced:
            return await player.send_event(
                {"error": True, "error_code": "not_your_turn"}, request=event
            )
        if self.drawn_cards == self.max_drawable_cards and not forced:
            return await player.send_event(
                {"error": True, "error_code": "cant_draw_more"}, request=event
            )
        if (
            self.drawn_cards + amount > self.max_drawable_cards
            and self.max_drawable_cards != -1
            and not forced
        ):
            return await player.send_event(
                {"error": True, "error_code": "amount_too_big"}, request=event
            )
        if pile_identifier not in self.card_piles:
            return await player.send_event(
                {"error": True, "error_code": "invalid_card_pile"}, request=event
            )
        pile = self.card_piles[pile_identifier]
        if not self._can_draw_from_pile(pile, player) and not forced:
            return await player.send_event(
                {"error": True, "error_code": "cant_draw_from_pile"}, request=event
            )
        if not forced:
            self.drawn_cards += amount
        drawn_cards: list[Card] = []
        for _ in range(amount):
            if len(pile) == 0:
                if not await self._refill_card_pile(
                    pile, refill_from=self.card_piles["discard"]
                ):
                    break
            card = await self._get_drawn_card_actions(
                card=pile.get(), player=player, forced=forced, event=event
            )
            drawn_cards.append(card)
        if len(drawn_cards) == 0:
            if not forced:
                await player.send_event(
                    {"error": True, "error_code": "no_cards_in_pile"}, request=event
                )
            return
        # Refill after the cards have been drawn
        if len(pile) == 0:
            await self._refill_card_pile(pile, refill_from=self.card_piles["discard"])
        player.cards = {
            **player.cards,
            **{card.identifier: card for card, _ in drawn_cards},
        }
        await self._broadcast(
            {
                "type": "cards_drawn",
                "amount": len(drawn_cards),
                "card_pile": pile.identifier,
                "player": player.username,
            },
            per_player_payload={
                player.username: {
                    # Send the cards only to the player
                    "cards": [
                        (card.identifier, [a.dict() for a in actions])
                        for card, actions in drawn_cards
                    ]
                }
            },
        )
        await self._after_card_drawn(
            cards=drawn_cards, card_pile=pile, forced=forced, player=player
        )
        # Turn skips after all draws has been used, regardless of the cards that the player has
        if self.drawn_cards == self.max_drawable_cards and (
            self.skip_turn_when_cards_drawn
            # Turn does not automatically skip, but the player has no playable cards
            or not self.skip_turn_when_cards_drawn
            and not any(
                card
                for card in player.cards.values()
                if self._can_discard_card(card, player)
            )
        ):
            self.turn_state = TurnState.PLAYED
            self.last_turn_change = time.time()
            await self._change_turn()

    async def _after_card_drawn(
        self, cards: list[Card], card_pile: CardPile, forced: bool, player: Player
    ) -> None:
        """Called on _draw_card after the cards_drawn event has been sent"""
        pass

    async def _refill_card_pile(
        self,
        card_pile: CardPile,
        refill_from: CardPile | Player,
        shuffle_afterwards: bool = True,
    ) -> bool:
        """
        Refills a card pile using cards from the provider specified
        in the 'refill_from' parameter

        :param card_pile: The card pile to refill
        :param refill_from: The provider to get the cards from
        :param shuffle_afterwards: The card pile will be shuffled if True
        after adding the cards
        :return: True if cards have been added to the pile, False otherwise
        """
        match refill_from:
            case CardPile():
                refiller_identifier = refill_from.identifier
                refiller_type = RefillProvider.CARD_PILE
                cards = [
                    refill_from.cards.pop() for _ in range(len(refill_from.cards) - 1)
                ]
            case Player():
                refiller_identifier = refill_from.username
                refiller_type = RefillProvider.PLAYER
                cards = list(refill_from.cards.values())
            case _:
                raise Exception(
                    f"`refill_from` has an unsupported type ({type(refill_from)})"
                )
        if len(cards) == 0:
            return False
        card_pile.add(cards)
        if shuffle_afterwards:
            card_pile.shuffle()
        await self._broadcast(
            {
                "type": "card_pile_refilled",
                "card_pile": card_pile.identifier,
                "refilled_from": refiller_identifier,
                "refilled_from_type": refiller_type,
                "cards": [
                    card.identifier for card in cards if card_pile.clients_can_see_cards
                ],
                "delta": len(cards),
            }
        )
        return True

    async def _before_card_is_discarded(
        self, card: Card, pile: CardPile, player: Player, request: dict
    ) -> None:
        """
        Called every time before a card is discarded, can be used to do a
        game action if the card's attributes matches with a pattern.

        In the 'ichi' game mode it's used for the special cards
        (block, +2, +4...)
        """
        pass

    async def _after_card_is_discarded(
        self, card: Card, pile: CardPile, player: Player, request: dict
    ) -> None:
        """
        Called every time after a card has been discarded, can be used to do a
        game action if the card's attributes matches with a pattern.

        In the 'ichi-0-7' game mode it's used to swap player's hands after
        the card_discarded event has been broadcast
        """
        pass

    async def _get_drawn_card_actions(
        self,
        card: Card,
        player: Player,
        forced: bool,
        event: dict | None = None,
    ) -> tuple[Card, list[Action]]:
        """
        Called on the Game._draw_card loop for each card, returns the card
        with it's available actions. It can also be used to modify a card's
        attributes before being drawn.

        In the 'ichi' game mode it's used to reset a wildcard color back
        to black
        """
        actions: list[Action] = [AddCardToHandAction()]
        card_piles: list[str] = self._can_discard_card(card, player)
        if (
            len(card_piles) >= 1
            and self.current_turn == player
            and self.turn_state in [TurnState.WAITING, TurnState.STARTED]
        ):
            actions.append(DiscardCardAction(card_piles=card_piles))
        return (card, actions)

    def _get_player_actions(self, player: Player) -> list[Action]:
        """
        Called on every turn change for each player, returns a list of
        possible actions the player can do in the current turn

        :param player: The player
        :return: A list of all possible actions the player can do
        """
        actions: list[Action] = [
            DrawCardAction(card_pile="draw", count=self.max_drawable_cards)
        ]
        for card in player.cards.values():
            card_piles: list[str] = self._can_discard_card(card, player)
            if (
                len(card_piles) >= 1
                and self.current_turn == player
                and self.turn_state in [TurnState.WAITING, TurnState.STARTED]
            ):
                actions.append(
                    DiscardCardAction(
                        card_identifier=card.identifier, card_piles=["discard"]
                    )
                )
        return actions

    def _is_card_valid_as_first(self, card: Card) -> bool:
        """
        Called by _start to check if a
        Returns True if the card can be the first drawn card
        """
        # NOTE: This method implementation is an example
        return card.value != 6

    def _can_discard_card(self, card: Card, player: Player) -> list[str]:
        """
        Called by _discard_card to check if a `player` can discard a `card`.
        Returns a list of the card piles' identifiers where the card can be discarded.

        :return: List of card pile identifiers
        """
        # NOTE: This method implementation is an example
        # Only even cards can be discarded
        card_piles = []
        if (
            not card.value % 2
            and player == self.current_turn
            and self.turn_state == TurnState.STARTED
        ):
            card_piles.append("discard")
        return card_piles

    def _can_draw_from_pile(self, pile: CardPile, player: Player) -> bool:
        """
        Returns True if `player` can draw cards from `pile`

        Called by _draw_card automatically, do not call directly unless you know
        what you're doing.

        :param pile: The card pile the player wants to draw from
        :param player: The player that wants to draw cards
        :return: True if the player can draw cards, False otherwise
        """
        # This method implementation is an example, but it may work in your game mode
        return pile == self.card_piles["draw"]

    async def _swap_players_hands(self, player1: Player, player2: Player) -> None:
        player1.cards, player2.cards = player2.cards, player1.cards
        await self._broadcast(
            {
                "type": "hands_swapped",
                "players": {
                    player1.username: {"card_amount": len(player1.cards)},
                    player2.username: {"card_amount": len(player2.cards)},
                },
            },
            per_player_payload={
                player1.username: {
                    "players": {
                        player1.username: {"cards": list(player1.cards.keys())}
                    },
                },
                player2.username: {
                    "players": {
                        player2.username: {"cards": list(player2.cards.keys())}
                    },
                },
            },
        )

    def _generate_deck(self) -> list[Card]:
        """
        Creates the game's deck
        Called on _start automatically

        :return: A list of cards to be used in the game
        """
        # This method implementation is an example, replace in the game mode
        # Here's a very simple example, creates a deck of 50 generic cards
        # with values ranging from 1 to 50
        return [Card(value=i, uid=0) for i in range(1, 51)]

    async def _declare_player_win(self, player: Player) -> None:
        if player.state == PlayerState.WON:
            return
        self.players_that_won += 1
        player.state = PlayerState.WON
        player.win_position = self.players_that_won
        player.play_time = time.time() - self.start_time
        self._update_player_stats(player)
        await self._broadcast(
            {
                "type": "player_won",
                "player": player.username,
                "win_position": player.win_position,
                "play_time": player.play_time,
            }
        )
        await self._on_player_win(player)

    async def _on_player_win(self, player: Player) -> None:
        """
        Called by _declare_player_win whenever a player wins the game/round.
        This method should not be executed manually, use _declare_player_win instead.
        By default it declares that the game is finished after the first player's win.

        :param player: The player that won the game
        """
        await self._declare_game_finished()

    async def _declare_game_finished(self, abrupt_finish: bool = False) -> None:
        self.state = RoomState.FINISHED
        self.end_time = time.time()
        await self._broadcast(
            {
                "type": "game_finished",
                "leaderboard": self._generate_leaderboard(),
                "game_duration": self.end_time - self.start_time,
                "abrupt_finish": abrupt_finish,
            }
        )
        if not abrupt_finish:
            for _player in self.players.values():
                self._update_player_stats(_player)

    def _generate_leaderboard(self) -> list[dict[str, Any]]:
        """
        Creates an ordered leaderboard

        :return: List containing a dict for each player
        """
        player_list = [
            {
                "username": username,
                "remaining_cards": len(player.cards),
                "play_time": player.play_time,
                "win_position": player.win_position,
            }
            for username, player in self.players.items()
        ]
        player_list.sort(key=lambda x: x["remaining_cards"])
        player_list.sort(key=lambda x: (x["win_position"]))
        player_list.sort(key=lambda x: self.players[x["username"]].last_state_change)
        return player_list

    def _update_player_stats(self, player: Player) -> None:
        """
        Updates the player's statistics for the game mode.
        Called on _leave (only if game has started), _declare_player_win
        and _declare_game_finished.

        Do NOT call this manually or modify this method in a child class
        """
        if player.updated_stats or self._STATS_MODEL is None:
            return
        end_time = self.end_time if self.end_time != 0.00 else time.time()
        with Session(database_engine) as session:
            statement = select(User).where(User.username == player.username)
            user = session.exec(statement).first()
            # Modifying user.stats directly would not commit it to the database
            # for some fucking reason, so the only working method I found was to
            # copy the stats dict and then reassign it to user.stats
            stats = deepcopy(user.stats)
            if self.__id__ not in stats:
                stats[self.__id__] = self._STATS_MODEL().dict()
            stats[self.__id__]["time_played"] += round(end_time - self.start_time, 2)
            stats[self.__id__]["games_played"] += 1
            if (
                self._STATS_MODEL.identifier() in ["explodedwins"]
                and player.state == PlayerState.WON
            ):
                key = "other_wins"
                if player.win_position in [1, 2, 3]:
                    key = f"top_{player.win_position}_wins"
                stats[self.__id__][key] += 1
            elif (
                self._STATS_MODEL.identifier() in ["basicwins"]
                and player.state == PlayerState.WON
            ):
                stats[self.__id__]["wins"] += 1
            user.stats = stats
            session.add(user)
            session.commit()
        player.updated_stats = True

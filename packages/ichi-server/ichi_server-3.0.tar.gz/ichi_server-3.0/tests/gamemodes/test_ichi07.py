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

from copy import deepcopy
import pytest
from ichi_server.models.client import AuthedClientRef
from ichi_server.models.gamemodes.base import TurnState
from ichi_server.models.gamemodes.ichi import ichi07

players = [
    AuthedClientRef(
        username="Player0",
        display_name="Mariano Rajoy",
        address="localhost",
        client_name="",
        websocket=None,
    ),
    AuthedClientRef(
        username="Player1",
        display_name="Mariano Rajoy",
        address="localhost",
        client_name="",
        websocket=None,
    ),
    AuthedClientRef(
        username="Player2",
        display_name="Mariano Rajoy",
        address="localhost",
        client_name="",
        websocket=None,
    ),
    AuthedClientRef(
        username="Player3",
        display_name="Mariano Rajoy",
        address="localhost",
        client_name="",
        websocket=None,
    ),
    AuthedClientRef(
        username="Player4",
        display_name="Mariano Rajoy",
        address="localhost",
        client_name="",
        websocket=None,
    ),
]


@pytest.mark.asyncio()
@pytest.mark.parametrize(["turn_rotation"], [[-1], [1]])
async def test_card_rotation(turn_rotation: int) -> None:
    fix_index = lambda x, y: x if x < y else 0
    room = ichi07("Test room", False)
    for player in players:
        await room._join(player)
    room.turn_watchdog_enabled = False
    room._turn_rotation = turn_rotation
    await room._start(players[0], {})
    card = None
    for _ in players:
        cards_with_0_value = [
            card for card in room.current_turn.cards.values() if card.value == 0
        ]
        if cards_with_0_value:
            card = cards_with_0_value[0]
            break
        await room._change_turn()
    if card == None:
        card = [card for card in room.card_piles["draw"].cards if card.value == 0][0]
        room.current_turn.cards[card.identifier] = card
    room.turn_state = TurnState.STARTED
    # Ensure the card can be discarded
    room.card_piles["discard"].cards[0].color = card.color
    status_quo = {
        player.username: deepcopy(player.cards) for player in room.players.values()
    }
    # Remove the to-be-discarded card
    status_quo[room.current_turn.username].pop(card.identifier)
    expected_changes = {
        player.username: room.turn_order[
            fix_index(index + 1, len(room.turn_order))
        ].username
        for index, player in enumerate(room.turn_order)
    }
    await room._discard_card(card.identifier, "discard", room.current_turn, {})
    assert room.card_piles["discard"].cards[-1] == card
    for player in room.players.values():
        assert player.cards == status_quo[expected_changes[player.username]]


@pytest.mark.asyncio()
async def test_card_swap() -> None:
    room = ichi07("Test room", False)
    for player in players[:3]:
        await room._join(player)
    room.turn_watchdog_enabled = False
    await room._start(players[0], {})
    card = None
    for _ in players:
        cards_with_0_value = [
            card for card in room.current_turn.cards.values() if card.value == 7
        ]
        if cards_with_0_value:
            card = cards_with_0_value[0]
            break
        await room._change_turn()
    if card == None:
        card = [card for card in room.card_piles["draw"].cards if card.value == 7][0]
        room.current_turn.cards[card.identifier] = card
    room.turn_state = TurnState.STARTED
    # Ensure the card can be discarded
    room.card_piles["discard"].cards[0].color = card.color
    status_quo = {
        player.username: deepcopy(player.cards) for player in room.players.values()
    }
    # Remove the to-be-discarded card
    status_quo[room.current_turn.username].pop(card.identifier)
    expected_changes = {
        room.turn_order[0].username: room.turn_order[2].username,
        room.turn_order[1].username: room.turn_order[1].username,
        room.turn_order[2].username: room.turn_order[0].username,
    }
    await room._discard_card(
        card.identifier,
        "discard",
        room.current_turn,
        event={"player": room.turn_order[2].username},
    )
    assert room.card_piles["discard"].cards[-1] == card
    for player in room.players.values():
        assert player.cards == status_quo[expected_changes[player.username]]

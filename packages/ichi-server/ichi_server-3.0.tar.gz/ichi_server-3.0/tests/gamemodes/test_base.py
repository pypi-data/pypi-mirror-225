from ichi_server.models.gamemodes.base import GameRoom, Card, Player, PlayerState

import pytest

card = Card(value=1)

player_pos_1 = Player(
    username="Fulanito1",
    display_name="Mariano Rajoy",
    address="localhost",
    client_name="",
    websocket=None,
)
player_pos_1.win_position = 1
player_pos_1.state = PlayerState.WON
player_pos_2 = Player(
    username="Fulanito2",
    display_name="Mariano Rajoy",
    address="localhost",
    client_name="",
    websocket=None,
)
player_pos_2.win_position = 2
player_pos_2.state = PlayerState.WON
player_pos_3 = Player(
    username="Fulanito3",
    display_name="Mariano Rajoy",
    address="localhost",
    client_name="",
    websocket=None,
)
player_pos_3.state = PlayerState.ABOUT_TO_WIN
player_pos_4 = Player(
    username="Fulanito4",
    display_name="Mariano Rajoy",
    address="localhost",
    client_name="",
    websocket=None,
)
player_pos_4.cards = {"1": card}
player_pos_4.state = PlayerState.PLAYING
player_pos_5 = Player(
    username="Fulanito5",
    display_name="Mariano Rajoy",
    address="localhost",
    client_name="",
    websocket=None,
)
player_pos_5.cards = {"1": card, "2": card, "3": card, "4": card}
player_pos_5.state = PlayerState.PLAYING
player_pos_6 = Player(
    username="Fulanito6",
    display_name="Mariano Rajoy",
    address="localhost",
    client_name="",
    websocket=None,
)
player_pos_6.cards = {"1": card, "2": card, "3": card, "4": card, "5": card, "6": card}
player_pos_6.state = PlayerState.PLAYING


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["player_list", "expected"],
    [
        (
            [
                player_pos_5,
                player_pos_2,
                player_pos_3,
                player_pos_6,
                player_pos_4,
                player_pos_1,
            ],
            [
                player_pos_1,
                player_pos_2,
                player_pos_3,
                player_pos_4,
                player_pos_5,
                player_pos_6,
            ],
        )
    ],
)
async def test(player_list: list[Player], expected: list[Player]):
    test_room = GameRoom(name="TestRoom", public=False)
    test_room._MAX_PLAYERS = 6
    for player in player_list:
        await test_room._join(player)
    assert len(test_room.players) == 6
    assert [u["username"] for u in test_room._generate_leaderboard()] == [
        u.username for u in expected
    ]

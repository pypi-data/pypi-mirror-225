from ichi_server.models.gamemodes.ichi import (
    ichi,
    ichiDebug,
    ichiPlayer,
    ichiCard,
    ichiCardColor,
    ichiCardType,
)

import pytest

test_player = ichiPlayer(
    username="Fulanito",
    display_name="Mariano Rajoy",
    address="localhost",
    client_name="",
    websocket=None,
)


@pytest.mark.parametrize(
    ["current_card", "test_card", "expected"],
    [
        (
            # Cards of same color but different number
            ichiCard(value=1, color=ichiCardColor.RED, type=ichiCardType.NUMBER),
            ichiCard(value=6, color=ichiCardColor.RED, type=ichiCardType.NUMBER),
            True,
        ),
        (
            # Cards of same number but different color
            ichiCard(value=1, color=ichiCardColor.RED, type=ichiCardType.NUMBER),
            ichiCard(value=1, color=ichiCardColor.GREEN, type=ichiCardType.NUMBER),
            True,
        ),
        (
            # Wildcard on wildcard
            ichiCard(
                color=ichiCardColor.BLACK,
                type=ichiCardType.DRAW_4,
                wildcard_color=ichiCardColor.YELLOW,
            ),
            ichiCard(
                color=ichiCardColor.BLACK,
                type=ichiCardType.WILDCARD,
                wildcard_color=ichiCardColor.BLUE,
            ),
            True,
        ),
        (
            # Plus 2 on a wildcard of different color
            ichiCard(
                color=ichiCardColor.BLACK,
                type=ichiCardType.DRAW_4,
                wildcard_color=ichiCardColor.GREEN,
            ),
            ichiCard(color=ichiCardColor.BLUE, type=ichiCardType.DRAW_2),
            False,
        ),
        (
            # Cards of different number and color
            ichiCard(value=2, color=ichiCardColor.RED, type=ichiCardType.NUMBER),
            ichiCard(value=8, color=ichiCardColor.GREEN, type=ichiCardType.NUMBER),
            False,
        ),
    ],
)
def test_is_card_playable(current_card: ichiCard, test_card: ichiCard, expected: bool):
    testing_room = ichi(name="Testing", public=False)
    testing_room.players["Fulanito"] = test_player
    testing_room.current_turn = test_player
    testing_room.card_piles["discard"].add(current_card)
    assert testing_room.card_piles["discard"].cards[0] == current_card
    assert (
        bool(
            testing_room._can_discard_card(
                test_card, test_player, ignore_turn_state=True
            )
        )
        == expected
    )


@pytest.mark.asyncio
async def test_card_color_reset():
    TARGET_CARD = "ichiCard~black-wildcard-0"
    testing_room = ichiDebug(name="Testing", public=False)
    await testing_room._join(test_player)
    assert "Fulanito" in testing_room.players
    fulanito: ichiPlayer = testing_room.players["Fulanito"]
    await testing_room.preprocess_event({"type": "start_game"}, test_player)
    if TARGET_CARD not in fulanito.cards:
        card = testing_room.deck[TARGET_CARD]
        idx = testing_room.card_piles["draw"].cards.index(card)
        testing_room.card_piles["draw"].get(idx)
        fulanito.cards[TARGET_CARD] = card
    assert TARGET_CARD in fulanito.cards
    await testing_room.preprocess_event({"type": "start_turn"}, fulanito)
    await testing_room.preprocess_event(
        {
            "type": "discard_card",
            "card": TARGET_CARD,
            "card_pile": "discard",
            "color": "RED",
        },
        fulanito,
    )
    assert testing_room.card_piles["discard"].cards[-1].identifier == TARGET_CARD
    card = testing_room.card_piles["discard"].get(-1)
    assert card.wildcard_color == ichiCardColor.RED
    testing_room.card_piles["draw"].cards.insert(0, card)
    assert testing_room.card_piles["draw"].cards[0] == card
    await testing_room.preprocess_event({"type": "start_turn"}, fulanito)
    await testing_room.preprocess_event(
        {"type": "draw_card", "card_pile": "draw"}, fulanito
    )
    assert TARGET_CARD in fulanito.cards
    assert fulanito.cards[TARGET_CARD].wildcard_color is None

from base64 import b64decode

from fastapi import WebSocketDisconnect

from ichi_server.dependencies import settings
from ichi_server.manager import create_database_and_tables
from ichi_server.server import app

from fastapi.testclient import TestClient

client = TestClient(app)
create_database_and_tables()

# https://stackoverflow.com/a/36610159
TEST_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII="
TEST_IMAGE_SHA1 = "81668d396da22832d75a986407ff10035e0d5899"


def get_captcha_solution() -> dict:
    response = client.get("/debug/get_solved_captcha")
    assert response.status_code == 200
    return response.json()


def test_registration():
    captcha_solution = get_captcha_solution()
    creation_response = client.post(
        "/user/register",
        json={
            "username": "PacoElDelBar",
            "password": "Password1!",
            # NOTE: Display name and chat color are not required
            "captcha": captcha_solution,
        },
    )
    assert creation_response.status_code == 200
    account_info_response = client.get("/users/PacoElDelBar")
    assert account_info_response.status_code == 200


def test_login():
    login_response = client.post(
        "/user/login",
        json={"username": "PacoElDelBar", "password": "Password1!"},
    )
    assert login_response.status_code == 200


def test_password_change():
    login_response = client.post(
        "/user/login",
        json={"username": "PacoElDelBar", "password": "Password1!"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    password_response = client.post(
        "/user/change_password",
        headers={"HTTPBearer": f"Bearer {login_response.json()['access_token']}"},
        json={"password": "Password2!"},
    )
    assert password_response.status_code == 200
    old_pass_login_response = client.post(
        "/user/login",
        json={"username": "PacoElDelBar", "password": "Password1!"},
    )
    assert old_pass_login_response.status_code == 401
    assert old_pass_login_response.json()["error_code"] == "incorrect_credentials"
    new_pass_login_response = client.post(
        "/user/login",
        json={"username": "PacoElDelBar", "password": "Password2!"},
    )
    assert new_pass_login_response.status_code == 200


def test_password_requirements_change():
    settings.password_minimum_numbers = 10
    captcha_solution = get_captcha_solution()
    creation_response = client.post(
        "/user/register",
        json={
            "username": "this_should_fail",
            "password": "Password1!",
            # NOTE: Display name and chat color are not required
            "captcha": captcha_solution,
        },
    )
    assert creation_response.status_code == 422
    errors = creation_response.json()["errors"]
    assert len(errors) == 1
    assert errors[0]["error_code"] == "invalid_password"
    # Ensure that people with passwords that do not meet requirements can still login
    login_response = client.post(
        "/user/login",
        json={"username": "PacoElDelBar", "password": "Password2!"},
    )
    assert login_response.status_code == 200
    settings.password_minimum_numbers = 1


def test_registration_invalid_captcha():
    creation_response = client.post(
        "/user/register",
        json={
            "username": "ThisWillFailToo",
            "password": "Password1!",
            "captcha": {"identifier": "", "solution": ""},
        },
    )
    assert creation_response.status_code == 422
    errors = creation_response.json()["errors"]
    assert len(errors) == 1
    assert errors[0]["error_code"] == "invalid_captcha_solution"


def test_avoid_captcha_reuse():
    captcha_response = get_captcha_solution()
    creation_response = client.post(
        "/user/register",
        json={
            "username": "captcha_test_ok",
            "password": "Password1!",
            "captcha": captcha_response,
        },
    )
    assert creation_response.status_code == 200
    bad_creation_response = client.post(
        "/user/register",
        json={
            "username": "captcha_test_bad",
            "password": "Password1!",
            "captcha": captcha_response,
        },
    )
    assert bad_creation_response.status_code == 422
    errors = bad_creation_response.json()["errors"]
    assert len(errors) == 1
    assert errors[0]["error_code"] == "invalid_captcha_solution"


def test_upload_profile_picture():
    # TODO: ensure compression and cropping are disabled beforehand
    login_response = client.post(
        "/user/login",
        json={"username": "PacoElDelBar", "password": "Password2!"},
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    profile_picture_response = client.post(
        "/user/image",
        params={"image_type": "picture"},
        headers={"HTTPBearer": f"Bearer {access_token}"},
        files={"image": b64decode(TEST_IMAGE)},
    )
    assert profile_picture_response.status_code == 200
    assert profile_picture_response.json()["type"] == "png"
    assert profile_picture_response.json()["hash"] == TEST_IMAGE_SHA1


def test_account_ban():
    login_response = client.post(
        "/user/login",
        json={"username": "Admin", "password": "MACARRONESCONTOMATICO"},
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    ban_response = client.post(
        "/admin/ban/captcha_test_ok",
        params={"punish_until": -1, "punishment_action": "Idiot"},
        headers={"HTTPBearer": f"Bearer {access_token}"},
    )
    assert ban_response.status_code == 200
    login_response_banned = client.post(
        "/user/login",
        json={"username": "captcha_test_ok", "password": "Password1!"},
    )
    # Banned players can still login to delete their accounts
    assert login_response_banned.status_code == 200
    try:
        with client.websocket_connect("/connect") as websocket:
            websocket.send_json(
                {
                    "type": "authenticate",
                    "token": login_response_banned.json()["access_token"],
                }
            )
            websocket.receive_json()
    except WebSocketDisconnect as e:
        assert e.code == 4040
        assert "Banned from the server" in e.reason
    unban_response = client.post(
        "/admin/unban/captcha_test_ok",
        headers={"HTTPBearer": f"Bearer {access_token}"},
    )
    assert unban_response.status_code == 200
    with client.websocket_connect("/connect") as websocket:
        websocket.send_json(
            {
                "type": "authenticate",
                "token": login_response_banned.json()["access_token"],
            }
        )
        response = websocket.receive_json()
        assert not response["error"]


def test_server_mute():
    login_response = client.post(
        "/user/login",
        json={"username": "Admin", "password": "MACARRONESCONTOMATICO"},
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    mute_response = client.post(
        "/admin/mute/captcha_test_ok",
        params={"punish_until": -1, "punishment_action": "Idiot"},
        headers={"HTTPBearer": f"Bearer {access_token}"},
    )
    assert mute_response.status_code == 200
    login_response_muted = client.post(
        "/user/login",
        json={"username": "captcha_test_ok", "password": "Password1!"},
    )
    # Banned players can still login to delete their accounts
    assert login_response_muted.status_code == 200
    with client.websocket_connect("/connect") as websocket:
        websocket.send_json(
            {
                "type": "authenticate",
                "token": login_response_muted.json()["access_token"],
            }
        )
        auth_response = websocket.receive_json()
        assert not auth_response["error"]
        websocket.send_json(
            {"type": "create_room", "game_mode": "ichi", "rules": {}, "public": False}
        )
        cr_response = websocket.receive_json()
        assert not cr_response["error"]
        websocket.send_json(
            {"type": "join_room", "room": cr_response["room_identifier"]}
        )
        jr_response = websocket.receive_json()
        while "error" not in jr_response:
            jr_response = websocket.receive_json()
        assert not jr_response["error"]
        websocket.send_json(
            {
                "type": "send_message",
                "message": "monkeys are really cool",
                "room": cr_response["room_identifier"],
            }
        )
        message_response = websocket.receive_json()
        assert message_response["error"]
        assert message_response["error_code"] == "muted_from_server"

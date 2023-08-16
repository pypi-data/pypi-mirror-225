from ichi_server import app

from fastapi.testclient import TestClient

client = TestClient(app)


def test_ws_authenticate():
    auth_response = client.post(
        "/user/login",
        json={"username": "PacoElDelBar", "password": "Password2!"},
    )
    assert auth_response.status_code == 200
    access_token = auth_response.json()["access_token"]
    with client.websocket_connect("/connect") as websocket:
        websocket.send_json({"type": "authenticate", "token": access_token})
        data = websocket.receive_json()
        assert not data["error"]

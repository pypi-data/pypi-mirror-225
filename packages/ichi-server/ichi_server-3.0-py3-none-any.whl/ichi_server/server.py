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

import json
from datetime import timedelta
from time import time

from fastapi import (
    FastAPI,
    Request,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from ichi_auth import AuthJWT
from ichi_auth.exceptions import AuthJWTException
from pydantic import PydanticValueError
from sqlmodel import Session, select

from ichi_server.dependencies import (
    _h,
    get_token_subject,
    has_missing_params,
    settings,
    RESOURCES_PATH,
)
from ichi_server.manager import (
    connection_manager,
    database_engine,
    get_authenticated_user,
    rooms,
)
from ichi_server.models.account import BannedIPAddress, User, UserMinimal
from ichi_server.models.client import ClientRef, AuthedClientRef
from ichi_server.models.exceptions import ValidationErrorSchema
from ichi_server.models.gamemodes import game_modes
from ichi_server.models.room import Room, RoomState, RoomType
from ichi_server.routers import (
    AUTHENTICATION_REQUIRED,
    account_router,
    admin_router,
    captcha_router,
    debug_router,
    gamemode_router,
)
from ichi_server.version import __version__

init_time = time()
app = FastAPI(
    title="ichi Server (%s)"
    % ("Production" if not settings.enable_debug_capabilities else "Debug"),
    version=__version__,
    responses={
        422: {"model": ValidationErrorSchema, "description": "Validation error"}
    },
    docs_url=None,
)
app.mount("/static", StaticFiles(directory=f"{RESOURCES_PATH}/static"), name="static")
app.include_router(account_router)
app.include_router(admin_router)
app.include_router(captcha_router)
app.include_router(gamemode_router)
if settings.enable_debug_capabilities:
    app.include_router(debug_router)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["*"]
)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []

    for pydantic_error in exc.errors():
        error = {
            "error_code": pydantic_error["type"],
            "error_msg": pydantic_error["msg"],
        }
        if "." in error["error_code"]:
            error["error_code"] = error["error_code"].split(".")[-1]
        if "ctx" in pydantic_error:
            error = {**error, **pydantic_error["ctx"]}
        errors.append(error)

    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "error_code": "validation_error",
            "errors": errors,
            "pydantic_output": exc.errors()
            if settings.enable_debug_capabilities
            else None,
        },
    )


@app.exception_handler(PydanticValueError)
def pydantic_exception_handler(request: Request, exc: PydanticValueError):
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "error_code": "validation_error",
            "errors": [
                {
                    "error_code": exc.code,
                    "error_msg": exc.__str__(),
                }
            ],
        },
    )


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "error_code": exc.error_code, "error_msg": exc.message},
    )


def generate_custom_openapi():
    openapi_schema = get_openapi(
        title="ichi Server API (%s)"
        % ("Production" if not settings.enable_debug_capabilities else "Debug"),
        version=app.version,
        openapi_version="3.0.0",
        contact={
            "name": "Issue tracker",
            "url": "https://codeberg.org/ichi/server/issues",
        },
        license_info={
            "name": "License",
            "url": "https://codeberg.org/ichi/server/raw/branch/master/LICENSE",
        },
        routes=app.routes,
    )

    # Custom documentation fastapi-jwt-auth
    headers = {
        "name": "HTTPBearer",
        "description": 'Access or refresh token preceded by "Bearer"',
        "in": "header",
        "required": True,
        "schema": {"title": "HTTPBearer", "type": "string"},
    }

    routes_with_authorization = [
        route
        for route in [*account_router.routes, *admin_router.routes]
        if route.name in AUTHENTICATION_REQUIRED
    ]

    for route in routes_with_authorization:
        method = list(route.methods)[0].lower()
        path_method = openapi_schema["paths"][route.path][method]
        if "parameters" in path_method:
            path_method["parameters"].append(headers)
        else:
            path_method["parameters"] = [headers]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = generate_custom_openapi


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="ichi Server API (%s)"
        % ("Production" if not settings.enable_debug_capabilities else "Debug"),
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_favicon_url="/static/logo.svg",
        swagger_js_url="/static/swagger-ui-bundle-min.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_ui_parameters={
            "syntaxHighlight.theme": "catppuccin",
            "docExpansion": "none",
        },
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get(
    "/info",
    summary="Returns the server information",
    tags=["General"],
)
async def get_server_info():
    return {
        "server_name": settings.server_name,
        "software": {
            "name": "ichi Server",
            "version": __version__,
            "is_prod": not settings.enable_debug_capabilities,
        },
        "active_rooms": len(rooms),
        "connected_clients": len(connection_manager.clients),
        "config": {
            "message_reporting_enabled": settings.message_reporting_secret_key
            is not None,
            "registration_enabled": settings.enable_registration,
            "profile_pictures_enabled": settings.enable_profile_pictures,
            "profile_banners_enabled": settings.enable_profile_banners,
            "profile_images_maximum_size": settings.profile_images_maximum_size,
            "password_requirements": {
                "min_length": settings.password_minimum_length,
                "max_length": settings.password_maximum_length,
                "min_letters": settings.password_minimum_letters,
                "min_numbers": settings.password_minimum_numbers,
                "min_symbols": settings.password_minimum_symbols,
            },
        },
    }


@app.get("/rooms")
def get_public_room_list() -> list[dict]:
    public_rooms = []
    for room in rooms.values():
        if room.public and (room.state == RoomState.PRE_GAME or type(room) is Room):
            public_rooms.append(room.full_info)
    return public_rooms


@app.websocket("/connect")
async def connect(websocket: WebSocket, Authorize: AuthJWT = Depends()):
    """WebSocket endpoint for game clients to connect to the server"""
    await websocket.accept()
    # Get the IP address of the client
    ip_address: str = (
        websocket.client.host
        # Server may be behind a reverse proxy, check for "X-Forwarded-For" header
        if "x-forwarded-for" not in websocket.headers
        else websocket.headers["x-forwarded-for"]
    )
    with Session(database_engine) as session:
        banned_address = session.exec(
            select(BannedIPAddress).where(BannedIPAddress.address == ip_address)
        ).first()
        if banned_address != None:
            return await websocket.close(4041, "IP address banned from server")
    client_address: str = f"{ip_address}:{websocket.client.port}"
    client: ClientRef | AuthedClientRef = ClientRef(
        address=client_address, client_name="Unnamed client", websocket=websocket
    )
    print(f"{_h('websocket')} Created client reference for {client_address}")
    conn_time_start = time()
    try:
        while True:
            event = await websocket.receive_json()
            if (
                event["type"] == "debug_destroy_connection"
                and settings.enable_debug_capabilities
            ):
                raise Exception("Manually triggered exception")
            if event["type"] == "authenticate":
                try:
                    Authorize.jwt_required("websocket", token=event["token"])
                except AuthJWTException as err:
                    await client.send_event(
                        {
                            "error": True,
                            "error_code": err.error_code,
                            "error_msg": err.message,
                        },
                        request=event,
                    )
                    continue
                if "client_name" in event:
                    client.client_name = event["client_name"]
                session_identifier: str = get_token_subject(event["token"])
                result = get_authenticated_user(
                    session_identifier,
                    connection_details=(ip_address, client.client_name),
                )
                if type(result) is not User:
                    if result[0] == "banned":
                        return await websocket.close(4040, result[1])
                    await client.send_event(
                        {
                            "error": True,
                            "error_code": result[0],
                            "error_msg": result[1],
                        },
                        request=event,
                    )
                    continue
                print(f"{_h('websocket')} {client} authenticated as @{result.username}")
                # Upgrade the ClientRef to AuthedClientRef
                client = AuthedClientRef(**dict(result), **dict(client))
                connection_manager.clients[client.username] = client
                await client.send_event(
                    {
                        "error": False,
                        # Only send the client the minimal version of the user
                        "account": {
                            **dict(UserMinimal(**dict(result))),
                            "remaining_recovery_codes": len(
                                json.loads(result.recovery_codes)
                            ),
                        },
                    },
                    event,
                )
            elif type(client) is not AuthedClientRef:
                await client.send_event(
                    {"error": True, "error_code": "not_authenticated"}, event
                )
            elif event["type"] == "get_game_modes":
                await client.send_event(
                    {
                        "error": False,
                        "game_modes": {
                            name: game_mode.get_gamemode_metadata()
                            for name, game_mode in game_modes.items()
                        },
                    },
                    event,
                )
            elif event["type"] == "get_public_rooms":
                await client.send_event(
                    {"error": False, "rooms": get_public_room_list()}, event
                )
            elif event["type"] == "create_room":
                if await has_missing_params(
                    event, ["game_mode", "rules", "public"], client.websocket
                ):
                    continue
                if event["game_mode"] not in game_modes:
                    await client.send_event(
                        {"error": True, "error_code": "non_existant_game_mode"}, event
                    )
                    continue
                default_room_name = f"{client.username}'{'s' if client.username[-1] != 's' else 's'} room"
                room = Room(
                    name=event.get("room_name", default_room_name),
                    public=event["public"],
                )
                room.create_child_room(event["game_mode"], event["rules"])
                rooms[room.identifier] = room
                # Send the room's UUID to the client
                await client.send_event(
                    {"error": False, "room_identifier": room.identifier}, event
                )
            elif "room" in event:
                if event["room"] not in rooms:
                    await client.send_event(
                        {"error": True, "error_code": "non_existant_room"}, event
                    )
                    continue
                # Relay the event to the specified room
                await rooms[event["room"]].preprocess_event(event, client)
            else:
                await client.send_event(
                    {"error": True, "error_code": "unknown_event"}, event
                )

    except WebSocketDisconnect as err:
        print(
            f"{_h('websocket')} Closed connection with {client} after {timedelta(seconds=int(time() - conn_time_start))}"
        )
        if type(client) is ClientRef:
            return
        connection_manager.disconnect(client)
        for room in client.rooms:
            if room._ROOM_TYPE == RoomType.DYNAMIC:
                await room._leave(client)
    except:
        print(
            f"{_h('websocket')} Forcefully closing connection with {client} due to an exception"
        )
        if type(client) is ClientRef:
            return
        connection_manager.disconnect(client)
        for room in client.rooms:
            if room._ROOM_TYPE == RoomType.DYNAMIC:
                await room._leave(client)
        raise

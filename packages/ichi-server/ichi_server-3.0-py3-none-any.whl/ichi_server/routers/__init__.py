from .account import router as account_router
from .admin import router as admin_router
from .captcha import router as captcha_router
from .debug import router as debug_router
from .gamemode import router as gamemode_router

AUTHENTICATION_REQUIRED = [
    "get_authed_user_profile",
    "modify_user_profile",
    "delete_account",
    "upload_profile_image",
    "delete_profile_image",
    "change_password",
    "get_sessions",
    "get_fresh_token",
    "refresh_session",
    "revoke_session",
    "apply_action_to_account",
    "get_punished_players",
    "get_administrators",
    "ban_ip_address",
    "unban_ip_address",
    "report_message",
    "get_reported_messages",
    "resolve_report",
]

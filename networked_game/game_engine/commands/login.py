import logging

from . import Command

logger = logging.getLogger(__name__)


class Login(Command):
    def process(self, data, user_connection, game_data) -> dict:
        if data["command"] != "login":
            return {}

        logger.debug(f"Log request from  {user_connection.user_name}")

        if game_data["state"] != "waiting_for_players":
            return {"error": True, "messages": ["login_game_already_started"]}

        user_name = data["user_name"]
        if user_name in game_data["users"]:
            return {"error": True, "messages": ["login_user_already_exists"]}

        user_connection.user_name = user_name
        login_order = len(game_data["users"])
        game_data["users"][user_name] = {"login_order": login_order}

        return {"error": False, "messages": ["login_success"]}

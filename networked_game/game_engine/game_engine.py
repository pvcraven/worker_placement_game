import logging

# from gui.constants import *
# from game_engine.constants import *
# from game_engine.placements import placements
from .generate_game_board import generate_game_board

logger = logging.getLogger(__name__)


class GameEngine:

    def __init__(self):
        self.game_data = {"users": [],
                          "view": "waiting_for_players"}

    def command_login(self, data: dict, user_connection):
        user_name = data["user_name"]
        user = {"name": user_name}
        user_connection.user_name = user_name
        self.game_data["users"].append(user)
        logger.debug(f"Log in from  {user_connection.user_name}")

    def command_logout(self, _data: dict, user_connection):
        logger.debug(f"Logout from {user_connection.user_name}")
        self.game_data["users"].remove(user_connection.user_name)

    def process_data(self, data: dict, user_connection):
        command = data["command"]

        if command == "login":
            logger.debug(f"login command")
            self.command_login(data, user_connection)
        elif command == "logout":
            logger.debug(f"logout command")
            self.command_logout(data, user_connection)

        elif command == "start_game":
            logger.debug(f"start_game command")
            self.game_data["view"] = "game_view"
            self.game_data["game_board"] = generate_game_board(self.game_data["users"])

        elif command == "move_piece":
            logger.debug(f"move_piece command")

            destination = data["destination"]
            piece_name = data["name"]
            for piece in self.game_data["game_board"]["pieces"]:
                if piece["name"] == piece_name:
                    piece["location"] = destination

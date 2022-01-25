import logging

from gui.constants import *
from game_engine.constants import *
from game_engine.placements import placements

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GameEngine:

    def __init__(self):
        self.game_data = {"users": [],
                          "view": "waiting_for_players"}

    def command_login(self, data, user_connection):
        user_name = data["user_name"]
        user = {"name": user_name}
        user_connection.user_name = user_name
        self.game_data["users"].append(user)
        logger.debug(f"Log in from  {user_connection.user_name}")

    def command_logout(self, data, user_connection):
        logger.debug(f"Logout from {user_connection.user_name}")
        self.game_data["users"].remove(user_connection.user_name)

    def process_data(self, data, user_connection):
        command = data["command"]

        if command == "login":
            self.command_login(data, user_connection)
        elif command == "logout":
            self.command_logout(data, user_connection)

        elif command == "start_game":

            for user_no in range(len(self.game_data["users"])):
                pass

            self.game_data["view"] = "game_view"

        elif command == "move_piece":

            destination = data["destination"]
            placement = None
            for cur_placement in self.game_data["placements"]:
                if cur_placement["location"] == destination:
                    placement = cur_placement
            if not placement:
                logger.debug(f"Did not find placement for {destination}.")

            piece = None
            for cur_piece in self.game_data["pieces"]:
                if cur_piece["name"] == data["name"]:
                    piece = cur_piece
            if not piece:
                logger.debug(f"Did not find placement for {data['name']}.")

            player = None
            for cur_player in self.game_data["users"]:
                if cur_player["name"] == user_connection.user_name:
                    player = cur_player

            assert player is not None



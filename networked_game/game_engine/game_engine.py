import logging
from networked_game.game_engine import commands
from networked_game.util import merge_dicts

logger = logging.getLogger(__name__)


class Command:

    def process(self, data, user_connection, game_data):
        pass


class GameEngine:

    def __init__(self):
        self.game_data = {"users": {},
                          "state": "waiting_for_players",
                          "board": {}
                          }

        self.commands = []
        self.commands.append(commands.Login())
        self.commands.append(commands.Logout())
        self.commands.append(commands.StartGame())
        self.commands.append(commands.Move())
        self.commands.append(commands.FinishQuest())
        self.commands.append(commands.FinishRound())
        self.commands.append(commands.EndGame())

    def process_data(self, data: dict, user_connection) -> dict:
        full_result = {}
        for command in self.commands:
            command_result = command.process(data, user_connection, self.game_data)
            full_result = merge_dicts(full_result, command_result)

        return full_result

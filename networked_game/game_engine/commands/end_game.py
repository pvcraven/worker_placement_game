import logging

from . import Command

logger = logging.getLogger(__name__)


class EndGame(Command):
    """
    All moves are done, start a new round
    """

    def process(self, data, user_connection, game_data) -> dict:
        board = game_data["board"]

        # Is there no active game yet?
        if "round_moves" not in board:
            return {}

        # Are there turns left in this game?
        if len(board["round_moves"]) > 0:
            return {}

        # Are there no more rounds left in the game?
        if board["round"] < board["max_rounds"]:
            return {}

        # End of game logic here

        return {"messages": ["game_end"]}

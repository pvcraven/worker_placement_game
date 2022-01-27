import random
import logging

logger = logging.getLogger(__name__)


def generate_game_board(users):
    random.shuffle(users)
    number_of_users = len(users)
    logger.debug(f"Creating board with {number_of_users} players.")

    pieces = []
    for i in range(number_of_users):
        pieces.append({"name": f"player-{i}", "location": "placement-00"})

    board = {
        "pieces": pieces,
        "players": users,
        "current_player": 0
    }
    logger.debug(f"Created game board: {board}")
    return board

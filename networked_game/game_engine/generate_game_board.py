import random
import logging

from .calculate_valid_moves import calculate_valid_moves


logger = logging.getLogger(__name__)


def generate_game_board(users):
    """ Generate our game board """

    # Shuffle the user list
    random.shuffle(users)

    number_of_users = len(users)
    logger.debug(f"Creating board with {number_of_users} players.")

    # Create a player piece for each user
    pieces = []
    for i in range(number_of_users):
        pieces.append({"name": f"player-{i}", "location": "placement-00"})

    board = {
        "pieces": pieces,
        "players": users,
        "current_player": 0
    }

    # Figure out what the value moves are
    calculate_valid_moves(board)

    logger.debug(f"Created game board: {board}")
    return board

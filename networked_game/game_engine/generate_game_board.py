import random
import logging


logger = logging.getLogger(__name__)


def generate_game_board(game_data):
    """ Generate our game board """

    board = {"player_move_order": [],
             "round_moves": [],
             "round": 1,
             "turn": 1,
             "turn_phase": 1,
             "max_rounds": 8}

    # Randomize the order of who goes first
    player_move_order = []
    users = game_data["users"]
    for user in users:
        player_move_order.append(user)
    random.shuffle(player_move_order)
    board['player_move_order'] = player_move_order

    game_data['board'] = board

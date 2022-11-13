import logging

logger = logging.getLogger(__name__)


def start_round(game_data):
    board = game_data['board']
    board['round_moves'] = board['player_move_order'].copy()

import logging

logger = logging.getLogger(__name__)


def start_round(game_data):
    board = game_data['board']
    board['round_moves'] = []
    for player_name in  board['player_move_order']:
        board['round_moves'].append({'action': 'move', 'player': player_name})
        board['round_moves'].append({'action': 'finish_quest', 'player': player_name})

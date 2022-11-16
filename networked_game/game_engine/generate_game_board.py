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
             "max_rounds": 8,
             "players": {},
             "piece_positions": {'player_1_hold': {'max_pieces': 0, 'pieces': []},
                                 'player_2_hold': {'max_pieces': 0, 'pieces': []},
                                 'player_3_hold': {'max_pieces': 0, 'pieces': []},
                                 'player_4_hold': {'max_pieces': 0, 'pieces': []},
                                 'position_1': {'max_pieces': 1, 'pieces': [], 'actions': {
                                     'get_resources': {'black': 2}
                                 }},
                                 'position_2': {'max_pieces': 1, 'pieces': [], 'actions': {
                                     'get_resources': {'orange': 2}
                                 }},
                                 'position_3': {'max_pieces': 1, 'pieces': [], 'actions': {
                                     'get_resources': {'purple': 1}
                                 }},
                                 'position_4': {'max_pieces': 1, 'pieces': [], 'actions': {
                                     'get_resources': {'white': 1}
                                 }},
                                 'position_5': {'max_pieces': 1, 'pieces': [], 'actions': {
                                     'get_resources': {'coins': 4}
                                 }},
                                 },
             "pieces": {},
             "piece_locations": [['player_1_piece_1', 'position_1']],
             "card_positions": [],
             "cards": [],
             "card_locations": []}

    # Generate player info
    users = game_data["users"]
    player_count = 0
    for user in users:
        player_count += 1
        player_name = f'player_{player_count}'
        player_info = {
            'login_name': user,
            'resources': {
                'points': 0,
                'black': 0,
                'orange': 0,
                'purple': 0,
                'white': 0,
                'coins': 0,
            }
        }
        board['players'][player_name] = player_info

    # Generate pieces
    for player in board['players']:
        piece_name = f"{player}_piece_1"
        position_name = f'{player}_hold'
        piece = {
                 'start_round_position': position_name,
                 'owner': player
                }

        board['pieces'][piece_name] = piece
        board['piece_positions'][position_name]['pieces'].append(piece_name)

    # Randomize the order of who goes first
    player_move_order = []
    for player in board['players']:
        player_move_order.append(player)
    random.shuffle(player_move_order)
    board['player_move_order'] = player_move_order

    game_data['board'] = board

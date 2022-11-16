
def get_player_from_username(user_name, game_data):
    for player_name in game_data['board']['players']:
        player = game_data['board']['players'][player_name]
        if player['login_name'] == user_name:
            return player_name
    return None


def get_piece_position(piece_name, game_data):
    positions = game_data['board']['piece_positions']
    for position_name in positions:
        piece_position = positions[position_name]
        pieces = piece_position['pieces']
        if piece_name in pieces:
            return position_name

    return None


def move_piece(piece_name, current_piece_position, destination_position, board):
    board['piece_positions'][current_piece_position]['pieces'].remove(piece_name)
    board['piece_positions'][destination_position]['pieces'].append(piece_name)


def reset_piece_positions(board):
    all_pieces = board['pieces']
    for position_name in board['piece_positions']:
        piece_position = board['piece_positions'][position_name]
        pieces_in_position = piece_position['pieces']
        for piece_name in pieces_in_position:
            move_piece(piece_name, position_name, all_pieces[piece_name]['start_round_position'], board)

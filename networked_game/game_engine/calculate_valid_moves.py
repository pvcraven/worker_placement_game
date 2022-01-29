def calculate_valid_moves(game_board):
    moves = []

    current_player_number = game_board['current_player']
    current_player = game_board['players'][current_player_number]
    current_player_name = current_player['name']
    for piece in game_board['pieces']:
        piece_name = piece['name']
        piece_location = piece['location']
        players_piece = f"player-{current_player_number}"
        if piece_name == players_piece:
            _, number_str = piece_location.split("-")
            number = int(number_str)
            next_space = number + 1
            move = {"piece": piece_name,
                    "destination": f"placement-{next_space:02}"}
            moves.append(move)

    valid_moves = [
            {
                "user": current_player_name,
                "moves": moves
            }
    ]

    game_board["valid_moves"] = valid_moves

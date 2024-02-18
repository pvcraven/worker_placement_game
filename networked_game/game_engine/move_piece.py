import logging

from .calculate_valid_moves import calculate_valid_moves

logger = logging.getLogger(__name__)


def move_piece(command, game_data):
    made_valid_move = False

    requested_destination = command["destination"]
    requested_piece = command["name"]

    game_board = game_data["game_board"]
    valid_moves = game_board["valid_moves"]
    for user_moves in valid_moves:

        user_name = user_moves["user"]
        moves = user_moves["moves"]
        for move in moves:
            possible_piece = move["piece"]
            possible_destination = move["destination"]

            if (
                requested_piece == possible_piece
                and requested_destination == possible_destination
            ):
                for piece in game_data["game_board"]["pieces"]:
                    if piece["name"] == requested_piece:
                        piece["location"] = requested_destination
                        made_valid_move = True

    if made_valid_move:
        calculate_valid_moves(game_board)
    else:
        logger.debug(f"Invalid move. {command}")

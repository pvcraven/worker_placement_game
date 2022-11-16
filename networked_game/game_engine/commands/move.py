import logging
from . import Command

from networked_game.game_engine.piece_util_functions import get_player_from_username
from networked_game.game_engine.piece_util_functions import get_piece_position
from networked_game.game_engine.piece_util_functions import move_piece

logger = logging.getLogger(__name__)


class Move(Command):
    def process(self, data, user_connection, game_data) -> dict:
        if data['command'] != 'move':
            return {}

        user_name = user_connection.user_name
        player_name = get_player_from_username(user_name, game_data)
        board = game_data['board']

        destination_position = data['to_position']
        piece_name = data['piece']

        logger.debug(f"Move request from  {user_name}")

        # Rule -- must be your turn
        player_whose_turn_it_is = board['round_moves'][0]
        user_whose_turn_it_is = board['players'][player_whose_turn_it_is]['login_name']
        if user_connection.user_name != user_whose_turn_it_is:
            return {'messages': ['not_your_turn']}

        # Rule -- piece must exist
        if piece_name not in board['pieces']:
            return {'messages': ['unknown_piece_name']}
        # Rule -- must have ownership of piece
        piece = board['pieces'][piece_name]
        if piece['owner'] != player_name:
            return {'messages': ['not_your_piece']}

        # Rule -- spot must exist
        if data['to_position'] not in board['piece_positions']:
            return {'messages': ['unknown_piece_position']}

        # Rule -- can only move to spots with available space
        position = board['piece_positions'][data['to_position']]
        if len(position['pieces']) >= position['max_pieces']:
            return {'messages': ['position_full']}

        # Rule -- must be from player's hold space
        current_piece_position = get_piece_position(piece_name, game_data)
        start_piece_position = piece['start_round_position']
        if current_piece_position != start_piece_position:
            return {'messages': ['piece_already_moved']}

        # Run actions for the space
        if 'actions' in board['piece_positions'][destination_position]:
            for action_name in board['piece_positions'][destination_position]['actions']:
                if action_name == 'get_resources':
                    for resource_name in board['piece_positions'][destination_position]['actions']['get_resources']:
                        resource_value = board['piece_positions'][destination_position]['actions']['get_resources'][resource_name]
                        board['players'][player_name]['resources'][resource_name] += resource_value

        # Everything ok -- move piece
        move_piece(piece_name, current_piece_position, destination_position, board)

        # Move successful
        del board['round_moves'][0]

        return {'messages': ['move_finished']}

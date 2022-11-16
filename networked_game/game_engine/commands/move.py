import logging
from . import Command

logger = logging.getLogger(__name__)


def get_player_from_username(user_name, game_data):
    for player_name in game_data['board']['players']:
        player = game_data['board']['players'][player_name]
        if player['login_name'] == user_name:
            return player_name
    return None


class Move(Command):
    def process(self, data, user_connection, game_data) -> dict:
        if data['command'] != 'move':
            return {}

        user_name = user_connection.user_name
        player_name = get_player_from_username(user_name, game_data)
        board = game_data['board']

        logger.debug(f"Move request from  {user_name}")

        # Rule -- must be your turn
        player_whose_turn_it_is = board['round_moves'][0]
        user_whose_turn_it_is = board['players'][player_whose_turn_it_is]['login_name']
        if user_connection.user_name != user_whose_turn_it_is:
            return {'messages': ['not_your_turn']}

        # Rule -- must have ownership of piece
        piece_name = data['piece']
        piece = board['pieces'][piece_name]
        if piece['owner'] != player_name:
            return {'messages': ['not_your_piece']}

        # Rule -- can only move to spots with available space
        position = board['piece_positions'][data['to_position']]
        if len(position['pieces']) >= position['max_pieces']:
            return {'messages': ['position_full']}

        # Rule -- must be from player's hold space
        piece_position = piece['start_round_position']

        # Everything ok -- move piece

                # Move successful
        del board['round_moves'][0]

        return {'messages': ['move_finished']}

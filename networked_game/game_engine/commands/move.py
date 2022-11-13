import logging
from . import Command

logger = logging.getLogger(__name__)


class Move(Command):
    def process(self, data, user_connection, game_data) -> dict:
        if data['command'] != 'move':
            return {}

        logger.debug(f"Move request from  {user_connection.user_name}")

        board = game_data['board']

        # Rule -- must be your turn
        player_whose_turn_it_is = board['round_moves'][0]
        user_whose_turn_it_is = board['players'][player_whose_turn_it_is]['login_name']
        if user_connection.user_name != user_whose_turn_it_is:
            return {'messages': ['not_your_turn']}

        # Rule -- must have ownership of piece

        # Rule -- can only move to spots with available space

        # Move successful
        del board['round_moves'][0]

        return {'messages': ['move_finished']}

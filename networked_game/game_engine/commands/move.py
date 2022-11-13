import logging
from . import Command

logger = logging.getLogger(__name__)


class Move(Command):
    def process(self, data, user_connection, game_data) -> dict:
        if data['command'] != 'move':
            return {}

        logger.debug(f"Move request from  {user_connection.user_name}")

        board = game_data['board']
        whose_turn_is_it = board['round_moves'][0]
        if user_connection.user_name != whose_turn_is_it:
            return {'message': 'not_your_turn'}

        del board['round_moves'][0]

        return {'messages': ['move_finished']}

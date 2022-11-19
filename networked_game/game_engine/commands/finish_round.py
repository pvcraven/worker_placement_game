import logging
from . import Command
from networked_game.game_engine.start_round import start_round
from networked_game.util import merge_dicts
from networked_game.game_engine.piece_util_functions import reset_piece_positions

logger = logging.getLogger(__name__)


class FinishRound(Command):
    """
    All moves are done, start a new round
    """
    def process(self, data, user_connection, game_data) -> dict:
        board = game_data['board']

        # Is there no active game yet?
        if 'round_moves' not in board:
            return {}

        # Are there turns left in this game?
        if len(board['round_moves']) > 0:
            return {}

        # Finished round
        result = {'messages': ['finished_round']}

        # Are there no more rounds left in the game?
        if board['round'] >= board['max_rounds']:
            return result

        # Advance to the next round
        if board['round'] == board['max_rounds']:
            board['game_over'] = True
        else:
            board['round'] += 1
            reset_piece_positions(board)
            start_round(game_data)

        return merge_dicts(result, {'messages': ['new_round']})

import logging
from . import Command

logger = logging.getLogger(__name__)


class FinishQuest(Command):
    """
    All moves are done, start a new round
    """
    def process(self, data, user_connection, game_data) -> dict:
        board = game_data['board']

        # Asking to finish a quest?
        if data['command'] != 'finish_quest':
            return {}

        # Success
        board['turn_phase'] = 'move'
        del board['round_moves'][0]

        return {'messages': ['finish_quest_phase_finished']}

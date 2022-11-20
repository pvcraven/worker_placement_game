import logging
from . import Command

from networked_game.game_engine.piece_util_functions import get_player_from_username
from networked_game.game_engine.piece_util_functions import get_piece_position
from networked_game.game_engine.piece_util_functions import move_piece

logger = logging.getLogger(__name__)


class PickQuestCard(Command):

    def process(self, data, user_connection, game_data) -> dict:
        if data['command'] != 'pick_quest_card':
            return {}

        quest_name = data['quest_name']
        user_name = user_connection.user_name
        player_name = get_player_from_username(user_name, game_data)
        board = game_data['board']

        player_whose_turn_it_is = board['round_moves'][0]['player']
        if player_name != player_whose_turn_it_is:
            logger.debug(f" {player_name=} != {player_whose_turn_it_is=}")
            return {'messages': ['not_your_turn']}

        # Is the quest in the draw pile?
        if quest_name not in board['quest_draw_pile']:
            return {'messages': ['quest_not_in_draw_pile']}

        # Move quest
        board['quest_draw_pile'].remove(quest_name)
        board['players'][player_name]['uncompleted_quest_cards'].append(quest_name)

        # Pop off this action
        board['round_moves'].pop(0)

        return {'messages': ['quest_picked']}
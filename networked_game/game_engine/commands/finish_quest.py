import logging
from . import Command
from networked_game.game_engine.piece_util_functions import get_player_from_username

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

        # Did we specify the quest name?
        if 'quest_name' in data and data['quest_name']:

            # We asked to complete a quest, get the data
            quest_name = data['quest_name']
            user_name = user_connection.user_name
            player_name = get_player_from_username(user_name, game_data)

            # Is the quest owned by the player?
            if quest_name not in board['players'][player_name]['uncompleted_quest_cards']:
                return {'messages': ['quest_not_owned_by_player']}

            # Get quest details
            quest = board['quest_cards'][quest_name]

            # Does the player have enough resource?
            has_resources = True
            for resource in quest['resources']:
                if board['players'][player_name]['resources'][resource] < quest['resources'][resource]:
                    has_resources = False

            if not has_resources:
                return {'messages': ['not_enough_resources']}

            # Take away the resources
            for resource in quest['resources']:
                board['players'][player_name]['resources'][resource] -= quest['resources'][resource]

            # Give the rewards
            for resource in quest['rewards']:
                board['players'][player_name]['resources'][resource] += quest['rewards'][resource]

            # Move player to player's completed pile
            board['players'][player_name]['uncompleted_quest_cards'].remove(quest_name)
            board['players'][player_name]['completed_quest_cards'].append(quest_name)

        # Pop off this action
        board['round_moves'].pop(0)

        return {'messages': ['finish_quest_phase_finished']}

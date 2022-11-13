import logging
from . import Command
from networked_game.game_engine.generate_game_board import generate_game_board
from networked_game.game_engine.start_round import start_round

logger = logging.getLogger(__name__)


class StartGame(Command):
    def process(self, data, user_connection, game_data) -> dict:
        if data['command'] != 'start_game':
            return {}

        logger.debug(f"Start game request from {user_connection.user_name}")

        if game_data['state'] != 'waiting_for_players':
            return {'messages': ['start_game_wrong_state']}

        # Only the first user can create the game
        login_order = game_data["users"][user_connection.user_name]['login_order']
        if login_order != 0:
            return {'messages': ['start_game_wrong_user']}

        # Set to running state
        game_data['state'] = 'running'

        # Create the game board
        generate_game_board(game_data)
        start_round(game_data)

        return {'messages': ['start_game_success']}

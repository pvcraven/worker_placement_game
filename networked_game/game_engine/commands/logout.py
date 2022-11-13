import logging
from . import Command

logger = logging.getLogger(__name__)


class Logout(Command):
    def process(self, data, user_connection, game_data):
        if data['command'] != 'logout':
            return {}

        logger.debug(f"Logout request from {user_connection.user_name}")

        result = game_data["users"].pop(user_connection.user_name, None)
        if not result:
            # This user isn't even logged in!
            return {'messages': ['logout_no_such_user']}

        # Adjust login order
        for key in game_data["users"]:
            if game_data["users"][key]['login_order'] > result['login_order']:
                game_data["users"][key]['login_order'] -= 1

        return {'messages': ['logout_success']}

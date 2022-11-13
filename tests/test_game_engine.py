import json

from networked_game.game_engine.game_engine import GameEngine
from networked_game.server.user_connection import UserConnection


def test_game_engine():
    # Create game engine
    assert True
    game_engine = GameEngine()
    user_connections = []

    def get_connection_for_user(search_user_name):
        for test_user_connection in user_connections:
            if test_user_connection.user_name == search_user_name:
                return test_user_connection
        return None

    # Test initial setup
    assert 'users' in game_engine.game_data
    assert 'state' in game_engine.game_data
    assert len(game_engine.game_data['users']) == 0

    # Test logging in users
    for user_no in range(1, 5):
        user_name = f'Test User {user_no}'
        data = {'command': 'login', 'user_name': user_name}
        user_connection = UserConnection()
        user_connections.append(user_connection)
        result = game_engine.process_data(data, user_connection)
        assert len(game_engine.game_data['users']) == user_no
        assert user_name in game_engine.game_data['users']
        assert game_engine.game_data['users'][user_name]['login_order'] == user_no - 1
        assert 'messages' in result
        assert result['messages'][0] == 'login_success'

    # Test logout
    data = {'command': 'logout'}
    result = game_engine.process_data(data, user_connections[1])
    assert result['messages'][0] == 'logout_success'
    assert len(game_engine.game_data['users']) == 3
    assert game_engine.game_data['users'][user_connections[-1].user_name]['login_order'] == 2

    # Log out a person not logged in
    result = game_engine.process_data(data, user_connections[1])
    assert result['messages'][0] == 'logout_no_such_user'
    user_connections.pop(1)

    # Make sure only the first player can start the game
    data = {'command': 'start_game'}
    result = game_engine.process_data(data, user_connections[1])
    assert result['messages'][0] == 'start_game_wrong_user'

    # Start the game
    data = {'command': 'start_game'}
    result = game_engine.process_data(data, user_connections[0])
    assert result['messages'][0] == 'start_game_success'
    assert game_engine.game_data['state'] == 'running'

    # Make sure we can't start twice
    data = {'command': 'start_game'}
    result = game_engine.process_data(data, user_connections[0])
    assert result['messages'][0] == 'start_game_wrong_state'

    # Run through each round of the game
    for round_no in range(1, game_engine.game_data['board']['max_rounds'] + 1):
        assert game_engine.game_data['board']['round'] == round_no

        # Run through each turn of the round
        for turn in range(3):
            # Make a move
            board = game_engine.game_data['board']
            user = board['round_moves'][0]
            data = {'command': 'move'}
            user_connection = get_connection_for_user(user)
            result = game_engine.process_data(data, user_connection)
            assert result['messages'][0] == 'move_finished'

        # Did we finish the round?
        assert result['messages'][1] == 'finished_round'

        # Did we start a new round, provided we aren't at the end of our game?
        if round_no < game_engine.game_data['board']['max_rounds']:
            assert result['messages'][2] == 'new_round'
            assert game_engine.game_data['board']['round'] == round_no + 1

    # Game should be done
    assert result['messages'][2] == 'game_end'

    print()
    print(json.dumps(game_engine.game_data, indent=4))

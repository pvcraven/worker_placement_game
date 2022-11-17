from networked_game.game_engine import GameEngine
from networked_game.server.user_connection import UserConnection


def print_result_data(result_data):
    if 'messages' in result_data:
        for message in result_data['messages']:
            print(f"Message: {message}")


def format_resources(resources):
    points = resources['points'] if 'points' in resources else 0
    black = resources['black'] if 'black' in resources else 0
    orange = resources['orange'] if 'orange' in resources else 0
    purple = resources['purple'] if 'purple' in resources else 0
    white = resources['white'] if 'white' in resources else 0
    coins = resources['coins'] if 'coins' in resources else 0
    result = f"Points: {points:3} " \
        f"B:{black:2} " \
        f"O:{orange:2} " \
        f"P:{purple:2} " \
        f"W:{white:2} " \
        f"C:{coins:2}"
    return result


def print_board(board):
    game_round = board['round']
    current_players_turn = board['round_moves'][0]
    print()
    print(f"--- Round: {game_round}  Player Turn: {current_players_turn}")

    for position in board['piece_positions']:
        print(position)
        for piece in board['piece_positions'][position]['pieces']:
            print(f"  {piece}")
    print("--- Player Resources ---")
    for player_name in board['players']:
        player = board['players'][player_name]
        login_name = player['login_name']
        resources = player['resources']
        out = f"{login_name:20} --> {format_resources(resources)}"

        print(out)
        for quest_card_name in player['quest_cards']:
            resources = board['cards'][quest_card_name]['resources']
            resources_string = format_resources(resources)
            reward = board['cards'][quest_card_name]['reward']
            reward_string = format_resources(reward)
            print(f"  {quest_card_name}: {resources_string} -> {reward_string}")


def main():
    # Startup
    game_engine = GameEngine()
    user_name = f'My User Name'
    data = {'command': 'login', 'user_name': user_name}
    user_connection = UserConnection()
    result = game_engine.process_data(data, user_connection)
    print_result_data(result)
    data = {'command': 'start_game'}
    result = game_engine.process_data(data, user_connection)
    print_result_data(result)

    board = game_engine.game_data['board']

    for turn in range(8):
        # Print board
        print_board(board)
        print()

        if board['turn_phase'] == 'move':
            # Get user move
            piece_name = input("Piece:    ")
            position_name = input("Position: ")
            print()

            # Process user move
            data = {'command': 'move',
                    'piece': piece_name,
                    'to_position': position_name
                    }
            result = game_engine.process_data(data, user_connection)

            # Print results
            print_result_data(result)

        elif board['turn_phase'] == 'finish_quest':
            # Ask if we want to finish a quest
            quest_name = input("Finish Quest: ")
            data = {'command': 'finish_quest',
                    'quest_name': quest_name,
                    }
            result = game_engine.process_data(data, user_connection)

            # Print results
            print_result_data(result)

main()

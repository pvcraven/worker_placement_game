from networked_game.game_engine import GameEngine
from networked_game.server.user_connection import UserConnection


def print_result_data(result_data):
    if 'messages' in result_data:
        for message in result_data['messages']:
            print(f"Message: {message}")


def print_card(board, quest_card_name):
    resources = board['quest_cards'][quest_card_name]['resources']
    resources_string = format_resources(resources, True)
    reward = board['quest_cards'][quest_card_name]['rewards']
    reward_string = format_resources(reward, True)
    print(f"  {quest_card_name}: {resources_string} -> {reward_string}")


def format_resources(resources, skip_blanks):
    points = resources['points'] if 'points' in resources else 0
    black = resources['black'] if 'black' in resources else 0
    orange = resources['orange'] if 'orange' in resources else 0
    purple = resources['purple'] if 'purple' in resources else 0
    white = resources['white'] if 'white' in resources else 0
    coins = resources['coins'] if 'coins' in resources else 0
    result = ""

    if points or not skip_blanks:
        result += f" Points: {points:3}"
    if black or not skip_blanks:
        result += f" B: {black:2}"
    if orange or not skip_blanks:
        result += f" O: {orange:2}"
    if purple or not skip_blanks:
        result += f" P: {purple:2}"
    if white or not skip_blanks:
        result += f" W: {white:2}"
    if coins or not skip_blanks:
        result += f" C: {coins:2}"

    return result


def print_board(board):
    game_round = board['round']
    current_players_turn = board['round_moves'][0]

    # Print round information
    print()
    print(f"--- Round: {game_round}  Player Turn: {current_players_turn}")

    # Print piece positions
    for position in board['piece_positions']:
        resources_string = ""
        if 'actions' in board['piece_positions'][position]:
            actions = board['piece_positions'][position]['actions']
            if 'get_resources' in actions:
                resources = actions['get_resources']
                resources_string = format_resources(resources, True)
        print(f"{position} {resources_string}")

        for piece in board['piece_positions'][position]['pieces']:
            print(f"  {piece}")

    # Print quest draw pile
    print("-- Quest draw pile")
    for quest_card_name in board['quest_draw_pile']:
        print_card(board, quest_card_name)

    # Print players
    print("-- Player Resources")
    for player_name in board['players']:
        # Print player name
        player = board['players'][player_name]
        login_name = player['login_name']
        print(f"{login_name} = {player_name}")

        # Print resources
        resources = player['resources']
        out = f" {format_resources(resources, False)}"
        print(out)

        # Print player quests
        for quest_card_name in player['uncompleted_quest_cards']:
            print_card(board, quest_card_name)

        print(f"  Completed {len(player['completed_quest_cards'])} quest(s).")


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

    while not board['game_over']:
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

    print()
    print("---- Game Over---")


main()

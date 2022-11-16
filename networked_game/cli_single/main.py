from networked_game.game_engine import GameEngine
from networked_game.server.user_connection import UserConnection


def print_result_data(result_data):
    if 'messages' in result_data:
        for message in result_data['messages']:
            print(f"Message: {message}")


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
        out = f"{login_name:20} --> " \
              f"Points: {resources['points']:3} " \
              f"B:{resources['black']:2} " \
              f"O:{resources['orange']:2} " \
              f"P:{resources['purple']:2} " \
              f"W:{resources['white']:2} " \
              f"C:{resources['coins']:2} "
        print(out)


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


main()

from networked_game.util import format_resources


def text_replacement(text, game_data):
    board = game_data['board']
    players = board['players']
    resource_string = format_resources(players['player_1']['resources'], False)
    login_name = players['player_1']["login_name"]
    text = text.replace("#users-0-name#", f"{login_name} - {resource_string}")

    return text

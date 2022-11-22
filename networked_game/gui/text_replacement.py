def text_replacement(text, game_data):
    board = game_data['board']
    players = board['players']
    text = text.replace("#users-0-name#", players['player_1']["login_name"])

    return text

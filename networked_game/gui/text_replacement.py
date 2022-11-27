from networked_game.util import format_resources


def text_replacement(text, game_data):
    board = game_data['board']
    players = board['players']

    player_1_name = players['player_1']['login_name']
    player_1_resources = players['player_1']['resources']
    text = text.replace("#player-1-name#", f"{player_1_name}")
    text = text.replace("#player-1-black#", f"{player_1_resources['black']}")
    text = text.replace("#player-1-orange#", f"{player_1_resources['orange']}")
    text = text.replace("#player-1-white#", f"{player_1_resources['white']}")
    text = text.replace("#player-1-purple#", f"{player_1_resources['purple']}")
    text = text.replace("#player-1-coins#", f"{player_1_resources['coins']}")


    return text

"""
Swap placeholders with actual text
"""


def text_replacement(text, player_name, game_data):
    board = game_data["board"]
    players = board["players"]

    player_1_name = players["player_1"]["login_name"]
    player_1_resources = players["player_1"]["resources"]
    text = text.replace("#player-1-name#", f"{player_1_name}")
    text = text.replace("#player-1-points#", f"{player_1_resources['points']}")
    text = text.replace("#player-1-black#", f"{player_1_resources['black']}")
    text = text.replace("#player-1-orange#", f"{player_1_resources['orange']}")
    text = text.replace("#player-1-white#", f"{player_1_resources['white']}")
    text = text.replace("#player-1-purple#", f"{player_1_resources['purple']}")
    text = text.replace("#player-1-coins#", f"{player_1_resources['coins']}")

    if "player_2" in players:
        player_2_name = players["player_2"]["login_name"]
        player_2_resources = players["player_2"]["resources"]
        text = text.replace("#player-2-name#", f"{player_2_name}")
        text = text.replace("#player-2-points#", f"{player_2_resources['points']}")
        text = text.replace("#player-2-black#", f"{player_2_resources['black']}")
        text = text.replace("#player-2-orange#", f"{player_2_resources['orange']}")
        text = text.replace("#player-2-white#", f"{player_2_resources['white']}")
        text = text.replace("#player-2-purple#", f"{player_2_resources['purple']}")
        text = text.replace("#player-2-coins#", f"{player_2_resources['coins']}")
    else:
        text = text.replace("#player-2-name#", "")
        text = text.replace("#player-2-points#", "")
        text = text.replace("#player-2-black#", "")
        text = text.replace("#player-2-orange#", "")
        text = text.replace("#player-2-white#", "")
        text = text.replace("#player-2-purple#", "")
        text = text.replace("#player-2-coins#", "")

    if board["round_moves"]:
        move = board["round_moves"][0]
        player_whose_turn_it_is = board["round_moves"][0]["player"]
        player_name_whose_turn_it_is = players[player_whose_turn_it_is]["login_name"]
        action = move["action"]
    else:
        player_name_whose_turn_it_is = ""
        action = "Game over"

    text = text.replace("#player_name#", f"{player_name}")
    text = text.replace("#whos_turn#", f"{player_name_whose_turn_it_is}")
    text = text.replace("#action#", f"{action}")
    text = text.replace("#round#", f"{board['round']}")

    return text

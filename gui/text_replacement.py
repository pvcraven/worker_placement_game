def text_replacement(text, game_data):
    text = text.replace("#users-0-name#", game_data["users"][0]["name"])

    return text

import logging
import random

from networked_game.game_engine.piece_positions import piece_positions
from networked_game.game_engine.quest_cards import quest_cards

logger = logging.getLogger(__name__)


def generate_game_board(game_data):
    """Generate our game board"""

    # Quest cards

    quest_card_deck = []
    for quest_name in quest_cards:
        quest_card_deck.append(quest_name)
    random.shuffle(quest_card_deck)

    # Quest draw pile
    quest_draw_pile = []
    for i in range(3):
        quest_draw_pile.append(quest_card_deck.pop())

    # Generate player info
    users = game_data["users"]
    player_count = 0
    players = {}
    for user in users:
        player_count += 1
        player_name = f"player_{player_count}"

        player_quest_cards = []
        for i in range(2):
            quest_card = quest_card_deck.pop()
            player_quest_cards.append(quest_card)

        player_info = {
            "login_name": user,
            "resources": {
                "points": 0,
                "black": 0,
                "orange": 0,
                "purple": 0,
                "white": 0,
                "coins": 0,
            },
            "uncompleted_quest_cards": player_quest_cards,
            "completed_quest_cards": [],
        }
        players[player_name] = player_info

    for player_no in range(1, player_count + 1):
        position = {f"player_{player_no}_hold": {"max_pieces": 0, "pieces": []}}
        piece_positions.update(position)

    # Generate pieces
    pieces = {}
    for player in players:
        piece_name = f"{player}_piece_1"
        position_name = f"{player}_hold"
        piece = {"start_round_position": position_name, "owner": player}

        pieces[piece_name] = piece
        piece_positions[position_name]["pieces"].append(piece_name)

    # Pull it all together as our game board
    board = {
        "player_move_order": [],
        "round_moves": [],
        "round": 1,
        "max_rounds": 8,
        "players": players,
        "piece_positions": piece_positions,
        "pieces": pieces,
        "piece_locations": [["player_1_piece_1", "position_1"]],
        "quest_cards": quest_cards,
        "quest_card_deck": quest_card_deck,
        "quest_card_discard_deck": [],
        "quest_draw_pile": quest_draw_pile,
        "game_over": False,
    }

    # Randomize the order of who goes first
    player_move_order = []
    for player in board["players"]:
        player_move_order.append(player)
    random.shuffle(player_move_order)
    board["player_move_order"] = player_move_order

    game_data["board"] = board

from PIL import Image, ImageDraw
import arcade

from networked_game.game_engine.piece_positions import piece_positions

from constants import *
from draw_resources import draw_resources


def main():
    for piece_position_name in piece_positions:
        piece_position = piece_positions[piece_position_name]

        with Image.open("black.png") as im:
            print(f"Generating: {piece_position}")

            # new_image = Image.new("RGBA", im.size, color=(228, 218, 191))
            # new_image.paste(im, (0, 0), im)
            new_image = im

            draw = ImageDraw.Draw(new_image)

            # Draw title
            draw.text(TITLE_LOCATION,
                      piece_position['title'],
                      font=title_font,
                      fill=arcade.color.BLACK,
                      anchor="ms",
                      width=CARD_WIDTH)

            # Draw resources
            if 'get_resources' in piece_position['actions']:
                # Draw rewards text
                draw.text(REWARD_TEXT_LOCATION,
                          "Rewards",
                          font=text_font,
                          fill=arcade.color.BLACK,
                          anchor="ms",
                          width=CARD_WIDTH
                          )
                resources = piece_position['actions']['get_resources']
                x = REWARDS_LOCATION[0]
                y = REWARDS_LOCATION[1]
                draw_resources(draw, x, y, resources)

            if 'pick_quest_card' in piece_position['actions']:
                # Draw resources text
                draw.text(REWARDS_LOCATION,
                          "Draw Quest Card",
                          font=text_font,
                          fill=arcade.color.BLACK)

            new_image.save(f"../networked_game/images/piece_positions/{piece_position_name}.png")


main()

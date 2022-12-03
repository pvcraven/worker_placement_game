from PIL import Image, ImageDraw
import arcade

from networked_game.game_engine.quest_cards import quest_cards

from constants import *
from draw_resources import draw_resources


def main():
    for quest_name in quest_cards:
        quest = quest_cards[quest_name]

        with Image.open("purple.png") as im:
            print(f"Generating: {quest_name}")

            # new_image = Image.new("RGBA", im.size)
            # new_image.paste(im, (0, 0), im)
            new_image = im

            draw = ImageDraw.Draw(new_image)

            # Draw title
            draw.text(TITLE_LOCATION,
                      quest['title'],
                      font=title_font,
                      fill=arcade.color.BLACK,
                      anchor="ms",
                      width=CARD_WIDTH
                      )

            # Draw resources text
            draw.text(RESOURCE_TEXT_LOCATION,
                      "Cost",
                      font=text_font,
                      fill=arcade.color.BLACK,
                      anchor="ms",
                      width=CARD_WIDTH
                      )

            # Draw resources
            resources = quest['resources']
            x = RESOURCE_LOCATION[0]
            y = RESOURCE_LOCATION[1]
            draw_resources(draw, x, y, resources)

            # Draw rewards text
            draw.text(REWARD_TEXT_LOCATION,
                      "Rewards",
                      font=text_font,
                      fill=arcade.color.BLACK,
                      anchor="ms",
                      width=CARD_WIDTH
                      )
            resources = quest['rewards']
            x = REWARDS_LOCATION[0]
            y = REWARDS_LOCATION[1]
            draw_resources(draw, x, y, resources)

            new_image.save(f"../networked_game/images/quest_cards/{quest_name}.png")


main()

from PIL import Image, ImageDraw, ImageFont
import arcade

from networked_game.game_engine.quest_cards import quest_cards


fnt = ImageFont.truetype("c:/Windows/Fonts/cambria.ttc", 40)
point_fnt = ImageFont.truetype("c:/Windows/Fonts/cambria.ttc", 28)

TITLE_LOCATION = 210, 125

RESOURCE_TEXT_LOCATION = 140, 730
RESOURCE_LOCATION = 140, 800
RESOURCE_SIZE = 35
RESOURCE_X_MARGIN = 15
RESOURCE_Y_MARGIN = 15

RECTANGLE = 1
CIRCLE = 2

REWARD_TEXT_LOCATION = 450, 730
REWARDS_LOCATION = 450, 800


def draw_resources(draw, start_x, start_y, resources):
    x = start_x
    y = start_y
    for resource_type in resources:
        if resource_type == 'points':
            bb = x, y, x + RESOURCE_SIZE, y + RESOURCE_SIZE
            draw.rectangle(xy=bb, fill=arcade.color.DARK_RED)
            draw.text((x, y),
                      f"{resources[resource_type]}",
                      font=point_fnt,
                      fill=arcade.color.WHITE)
        else:
            for count in range(resources[resource_type]):
                bb = x, y, x + RESOURCE_SIZE, y + RESOURCE_SIZE
                x += RESOURCE_SIZE + RESOURCE_X_MARGIN
                if resource_type == 'black':
                    color = arcade.color.BLACK
                    shape = RECTANGLE
                elif resource_type == 'orange':
                    color = arcade.color.BURNT_ORANGE
                    shape = RECTANGLE
                elif resource_type == 'purple':
                    color = arcade.color.PURPLE
                    shape = RECTANGLE
                elif resource_type == 'white':
                    color = arcade.color.WHITE
                    shape = RECTANGLE
                elif resource_type == 'coins':
                    color = arcade.color.BRONZE
                    shape = CIRCLE

                if shape == RECTANGLE:
                    draw.rectangle(xy=bb, fill=color)
                elif shape == CIRCLE:
                    draw.ellipse(xy=bb, fill=color)

                if (count + 1) % 5 == 0:
                    x = start_x
                    y += RESOURCE_SIZE + RESOURCE_Y_MARGIN

        x = start_x
        y += RESOURCE_SIZE + RESOURCE_Y_MARGIN


def main():
    for quest_name in quest_cards:
        quest = quest_cards[quest_name]

        with Image.open("Poker_BB_Black.png") as im:
            print(f"Generating: {quest_name}")
            draw = ImageDraw.Draw(im)

            # Draw title
            draw.text(TITLE_LOCATION, quest['title'], font=fnt, fill=arcade.color.BLACK)

            # Draw resources text
            draw.text(RESOURCE_TEXT_LOCATION, "Resources", font=fnt, fill=arcade.color.BLACK)

            # Draw resources
            resources = quest['resources']
            x = RESOURCE_LOCATION[0]
            y = RESOURCE_LOCATION[1]
            draw_resources(draw, x, y, resources)

            # Draw rewards text
            draw.text(REWARD_TEXT_LOCATION, "Rewards", font=fnt, fill=arcade.color.BLACK)
            resources = quest['rewards']
            x = REWARDS_LOCATION[0]
            y = REWARDS_LOCATION[1]
            draw_resources(draw, x, y, resources)

            im.save(f"../networked_game/images/quest_cards/{quest_name}.png")


main()

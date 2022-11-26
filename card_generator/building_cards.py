from PIL import Image, ImageDraw, ImageFont
import arcade

from networked_game.game_engine.piece_positions import piece_positions


fnt = ImageFont.truetype("c:/Windows/Fonts/cambria.ttc", 40)
point_fnt = ImageFont.truetype("c:/Windows/Fonts/cambria.ttc", 28)

TITLE_LOCATION = 210, 655

RESOURCE_TEXT_LOCATION = 140, 430
RESOURCE_LOCATION = 140, 500
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
                else:
                    raise Exception("Unknown resource type")

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
    for piece_position_name in piece_positions:
        piece_position = piece_positions[piece_position_name]

        with Image.open("Mini_BB_Black.png") as im:
            print(f"Generating: {piece_position}")

            new_image = Image.new("RGBA", im.size, color=(228, 218, 191))
            new_image.paste(im, (0, 0), im)

            draw = ImageDraw.Draw(new_image)

            # Draw title
            draw.text(TITLE_LOCATION, piece_position['title'], font=fnt, fill=arcade.color.BLACK)

            # Draw resources
            if 'get_resources' in piece_position['actions']:

                # Draw resources text
                draw.text(RESOURCE_TEXT_LOCATION, "Resources", font=fnt, fill=arcade.color.BLACK)

                resources = piece_position['actions']['get_resources']
                x = RESOURCE_LOCATION[0]
                y = RESOURCE_LOCATION[1]
                draw_resources(draw, x, y, resources)

            if 'pick_quest_card' in piece_position['actions']:
                # Draw resources text
                draw.text(RESOURCE_TEXT_LOCATION, "Draw Quest Card", font=fnt, fill=arcade.color.BLACK)

            new_image.save(f"../networked_game/images/piece_positions/{piece_position_name}.png")


main()

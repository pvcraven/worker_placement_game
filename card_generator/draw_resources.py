import arcade
from constants import *


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
                    color = arcade.color.GRAY
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

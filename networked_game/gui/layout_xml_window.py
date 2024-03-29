import logging

import arcade

from networked_game.gui import (
    Rect,
    Text,
    get_point_info,
    get_rect_info,
    get_shape_at,
    process_svg,
)

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Test"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        self.svg = process_svg("layout.svg")

    def calculate_screen_data(self):
        ratio_width, ratio_height = self.svg.width, self.svg.height
        screen_width = self.width
        screen_height = self.height

        # Compare ratio to screen size, get the minimum, so we can fit on screen
        ratio = min(screen_width / ratio_width, screen_height / ratio_height)

        # Get our display size based on this ratio
        display_width = ratio * ratio_width
        display_height = ratio * ratio_height

        # Calculate our lower-left origin
        origin_x = (screen_width - display_width) / 2
        origin_y = (screen_height - display_height) / 2

        logger.debug(f"{origin_x=}, {origin_y=}, {ratio=}")
        return origin_x, origin_y, ratio

    # def draw_layout(self):
    #
    #     origin_x, origin_y, ratio = self.calculate_screen_data()
    #     for shape in self.svg.shapes:
    #         if isinstance(shape, Rect):
    #             logger.debug(f"Drawing {shape}")
    #             cx, cy, width, height = get_rect_info(shape, origin_x, origin_y, ratio)
    #             logger.debug(f"Drawing {cx=} {cy=} {width=} {height=}")
    #             if "fill" in shape.style:
    #                 color = shape.style["fill"]
    #                 if isinstance(color, str) and color.startswith("#"):
    #                     h = color.lstrip('#')
    #                     color = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    #                     if "fill-opacity" in shape.style:
    #                         opacity = int(float(shape.style["fill-opacity"]) * 255)
    #                         color.append(opacity)
    #                     arcade.draw_rectangle_filled(cx, cy, width, height, color)
    #             if "stroke" in shape.style:
    #                 color = shape.style["stroke"]
    #                 if isinstance(color, str) and color.startswith("#"):
    #                     h = color.lstrip('#')
    #                     color = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    #                     if "stroke-opacity" in shape.style:
    #                         opacity = int(float(shape.style["stroke-opacity"]) * 255)
    #                         color.append(opacity)
    #
    #                     stroke_width = shape.style["stroke-width"] * ratio
    #                     arcade.draw_rectangle_outline(cx, cy, width, height, color, stroke_width)
    #         elif isinstance(shape, Text):
    #             x, y = get_point_info(shape.x, shape.y, origin_x, origin_y, ratio)
    #             arcade.draw_text(shape.text, x, y, arcade.color.WHITE)

    def on_draw(self):
        self.clear(arcade.color.WHITE)
        self.draw_layout()

    def on_mouse_press(self, x, y, button, mod):
        logger.debug("Click")
        origin_x, origin_y, scale = self.calculate_screen_data()
        get_shape_at(self.svg, origin_x, origin_y, scale, x, y)


GameWindow()
arcade.run()

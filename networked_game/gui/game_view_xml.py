import logging
from os.path import exists

import arcade
import arcade.gui.widgets.buttons

from networked_game.game_engine.piece_util_functions import get_piece_position

from .dimension_calculations import calculate_screen_data
from .layout_xml import (
    Rect,
    Text,
    get_point_info,
    get_rect_for_name,
    get_rect_info,
    get_shape_at,
    process_svg,
)
from .lookup_image import lookup_image
from .text_replacement import text_replacement

logger = logging.getLogger(__name__)

MESSAGE_TIME = 1.5


class GameViewXML(arcade.View):
    """Our custom Window Class"""

    def __init__(self):
        """Initializer"""
        # Call the parent class initializer
        super().__init__()
        logger.debug("GameViewXML.__init__")

        self.origin_x: int = 0
        self.origin_y: int = 0
        self.ratio: float = 0

        self.messages: list = []
        self.message_timer: float = 0

        arcade.set_background_color(arcade.color.PAPAYA_WHIP)

        self.gui_manager = arcade.gui.UIManager()
        self.gui_manager.enable()

        # Pieces
        self.piece_list = arcade.SpriteList()
        self.actions_list = arcade.SpriteList()

        # List of items we are dragging with the mouse
        self.held_items = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_items_original_position = []

        self.svg = process_svg("networked_game/gui/layout.svg")

        self.process_game_data(self.window.game_data)

        finish_quests_button = arcade.gui.UIFlatButton(
            text="Finish Quests", width=200, x=1000, y=50
        )

        @finish_quests_button.event("on_click")
        def on_click_settings(_event):
            data = {"command": "finish_quest"}

            self.window.communications_channel.send_queue.put(data)

        self.gui_manager.add(finish_quests_button)

    def on_update(self, delta_time):

        # Service client network tasks
        self.window.communications_channel.service_channel()

        # Are we a server? If so, service that
        if self.window.server:
            self.window.server.server_check()

        # Any messages to process?
        if not self.window.communications_channel.receive_queue.empty():
            data = self.window.communications_channel.receive_queue.get()
            logger.debug("Received: {data}")

            if "board" in data:
                logger.debug("Calling process_game_data")
                self.window.game_data = data
                self.process_game_data(data)
            if "messages" in data:
                logger.debug("Updating messages")
                self.messages.extend(data["messages"])

        # Message list
        if len(self.messages) > 0:
            if not self.message_timer:
                self.message_timer = delta_time

            else:
                self.message_timer += delta_time
                if self.message_timer >= MESSAGE_TIME:
                    self.messages.pop(0)
                    self.message_timer = 0

    def _process_quest_draw(self, board, sprite_list):
        quest_draw_pile = board["quest_draw_pile"]
        for index, card_name in enumerate(quest_draw_pile):
            location_name = f"quest_draw_pile_{index}"
            rect = get_rect_for_name(self.svg, location_name)
            if not rect:
                logger.error(f"Can't find rect for {location_name}")
                continue

            image_name = f"networked_game/images/quest_cards/{card_name}.png"

            cx, cy, width, height = get_rect_info(
                rect, self.origin_x, self.origin_y, self.ratio
            )

            # Create sprite
            logger.debug(f"Drawing with image {image_name}")
            sprite = arcade.Sprite(image_name)
            sprite.properties["name"] = card_name
            sprite.position = cx, cy
            sprite.height = height
            sprite.width = width
            sprite_list.append(sprite)
            logger.debug(
                f"Placed {card_name} located at {location_name} at ({cx}, {cy})"
            )

    def _process_player_uncompleted_quests(self, board, sprite_list):
        for player_name in board["players"]:
            uncompleted_quests = board["players"][player_name][
                "uncompleted_quest_cards"
            ]
            for index, card_name in enumerate(uncompleted_quests):
                location_name = f"{player_name}_quest_{index}"
                rect = get_rect_for_name(self.svg, location_name)
                if not rect:
                    logger.error(f"Can't find rect for {location_name}")
                    continue

                image_name = f"networked_game/images/quest_cards/{card_name}.png"

                cx, cy, width, height = get_rect_info(
                    rect, self.origin_x, self.origin_y, self.ratio
                )

                # Create sprite
                logger.debug(f"Drawing with image {image_name}")
                sprite = arcade.Sprite(image_name)
                sprite.properties["name"] = card_name
                sprite.position = cx, cy
                sprite.height = height
                sprite.width = width
                sprite_list.append(sprite)
                logger.debug(
                    f"Placed {card_name} located at {location_name} at ({cx}, {cy})"
                )

    def _process_piece_positions(self, board, sprite_list):
        piece_positions = board["piece_positions"]
        for index, piece_position_name in enumerate(piece_positions):

            rect = get_rect_for_name(self.svg, piece_position_name)
            if not rect:
                logger.error(f"Can't find rect for {piece_position_name}")
                continue

            image_name = (
                f"networked_game/images/piece_positions/{piece_position_name}.png"
            )
            file_exists = exists(image_name)

            if file_exists:
                cx, cy, width, height = get_rect_info(
                    rect, self.origin_x, self.origin_y, self.ratio
                )

                # Create sprite
                logger.debug(f"Drawing with image {image_name}")
                sprite = arcade.Sprite(image_name)
                sprite.properties["name"] = piece_position_name
                sprite.position = cx, cy
                sprite.height = height
                sprite.width = width
                sprite_list.append(sprite)
                logger.debug(
                    f"Placed card located at {piece_position_name} at ({cx}, {cy})"
                )

    def _process_pieces(self, board, sprite_list):
        """Create sprites and put them in the correct location"""
        pieces = board["pieces"]

        # Loop through each item in the list we are given
        for piece_name in pieces:

            # Get piece location
            location_name = get_piece_position(piece_name, board)

            logger.debug(f"Placing {piece_name}, {location_name}")

            # Get the rect for this location from the SVG
            rect = get_rect_for_name(self.svg, location_name)
            if not rect:
                logger.warning(
                    f"Can't find location named {location_name} to place {piece_name}."
                )
                continue

            # Get rect, adjusted for our screen dimensions
            cx, cy, width, height = get_rect_info(
                rect, self.origin_x, self.origin_y, self.ratio
            )

            # Figure out what image to use for this sprite
            image_name = lookup_image(piece_name)

            if not image_name:
                logger.warning(
                    f"Can't find image for {location_name}, so can't create sprite."
                )
                continue

            # Create sprite
            logger.debug(f"Drawing with image {image_name}")
            sprite = arcade.Sprite(image_name, 0.2)
            sprite.properties["name"] = piece_name
            sprite.position = cx, cy
            sprite_list.append(sprite)
            logger.debug(
                f"Placed {piece_name} located at {location_name} at ({cx}, {cy})"
            )

    def process_game_data(self, data):

        logger.debug(f"Processing game data")

        # Create new sprite lists
        self.piece_list = arcade.SpriteList()
        self.actions_list = arcade.SpriteList()

        self.origin_x, self.origin_y, self.ratio = calculate_screen_data(
            self.svg.width, self.svg.height, self.window.width, self.window.height
        )
        logger.debug(
            f"{self.svg.width=}, {self.svg.height=}, {self.window.width=}, {self.window.height=}"
        )
        logger.debug(f"{self.origin_x=}, {self.origin_y=}, {self.ratio=}")

        # logger.debug(f"- Placements")
        # placement_list = data["placements"]
        # process_items(placement_list, self.piece_list)
        if "board" in data:
            board = data["board"]
            self._process_quest_draw(board, self.piece_list)
            self._process_piece_positions(board, self.piece_list)
            self._process_player_uncompleted_quests(board, self.piece_list)
            self._process_pieces(board, self.piece_list)
        if "messages" in data:
            self.messages.extend(data["messages"])
        # logger.debug(f"- Actions")
        # pieces_list = data["action_items"]
        # process_items(pieces_list, self.actions_list)

    def draw_layout(self):

        origin_x, origin_y, ratio = calculate_screen_data(
            self.svg.width, self.svg.height, self.window.width, self.window.height
        )
        for shape in self.svg.shapes:
            if isinstance(shape, Rect):
                pass
                # cx, cy, width, height = get_rect_info(shape, origin_x, origin_y, ratio)
                # if "fill" in shape.style:
                #     color = shape.style["fill"]
                #     if isinstance(color, str) and color.startswith("#"):
                #         h = color.lstrip('#')
                #         color = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
                #         if "fill-opacity" in shape.style:
                #             opacity = int(float(shape.style["fill-opacity"]) * 255)
                #             color.append(opacity)
                #         arcade.draw_rectangle_filled(cx, cy, width, height, color)
                # if "stroke" in shape.style:
                #     color = shape.style["stroke"]
                #     if isinstance(color, str) and color.startswith("#"):
                #         h = color.lstrip('#')
                #         color = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
                #         if "stroke-opacity" in shape.style:
                #             opacity = int(float(shape.style["stroke-opacity"]) * 255)
                #             color.append(opacity)
                #
                #         stroke_width = shape.style["stroke-width"] * ratio
                #         arcade.draw_rectangle_outline(cx, cy, width, height, color, stroke_width)
            elif isinstance(shape, Text):
                x, y = get_point_info(shape.x, shape.y, origin_x, origin_y, ratio)
                text = text_replacement(
                    shape.text, self.window.user_name, self.window.game_data
                )
                text_size_string = shape.style["font-size"]
                text_size_string = text_size_string[:-2]
                text_size_float = float(text_size_string) * 1 * ratio
                arcade.draw_text(
                    text,
                    x,
                    y,
                    arcade.color.BLACK,
                    text_size_float,
                    multiline=True,
                    width=800,
                )

    def draw_messages(self):
        if len(self.messages) > 0:
            _, _, ratio = calculate_screen_data(
                self.svg.width, self.svg.height, self.window.width, self.window.height
            )

            hh = self.window.height / 2
            hw = self.window.width / 2

            arcade.draw_rectangle_filled(hw, hh, hw, hh / 4, color=arcade.color.ALMOND)
            arcade.draw_text(
                self.messages[0],
                0,
                hh,
                align="center",
                anchor_y="center",
                color=arcade.color.BLACK,
                font_size=34 * ratio,
                width=self.window.width,
            )

    def on_draw(self):
        arcade.start_render()
        self.draw_layout()
        self.piece_list.draw()
        self.actions_list.draw()
        self.gui_manager.draw()
        self.draw_messages()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.process_game_data(self.window.game_data)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""

        # Get list of sprites we've clicked on
        sprites = arcade.get_sprites_at_point((x, y), self.piece_list)

        # Have we clicked on a sprites?
        if len(sprites) > 0:

            # Might be a stack, get the top one
            primary = sprites[-1]
            name = primary.properties["name"]
            if name.startswith("quest_"):
                logger.debug(f"Clicked on quest {name}")
                board = self.window.game_data["board"]
                quest_draw_pile = board["quest_draw_pile"]
                if name in quest_draw_pile:
                    data = {
                        "command": "pick_quest_card",
                        "quest_name": name,
                    }
                else:
                    data = {
                        "command": "finish_quest",
                        "quest_name": name,
                    }
                self.window.communications_channel.send_queue.put(data)
            else:
                # All other cases, grab the face-up card we are clicking on
                self.held_items = [primary]
                # Save the position
                self.held_items_original_position = [self.held_items[0].position]

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """User moves mouse"""

        # If we are holding items, move them with the mouse
        for item in self.held_items:
            item.center_x += dx
            item.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """Called when the user presses a mouse button."""

        # If we don't have any cards, who cares
        if len(self.held_items) == 0:
            return

        origin_x, origin_y, ratio = calculate_screen_data(
            self.svg.width, self.svg.height, self.window.width, self.window.height
        )
        destination = get_shape_at(self.svg, origin_x, origin_y, ratio, x, y)

        if destination:
            for item in self.held_items:
                item_name = item.properties["name"]
                destination_name = destination.id
                logger.debug(f"Move {item_name} to {destination_name}")

                data = {
                    "command": "move",
                    "piece": item_name,
                    "to_position": destination_name,
                }

                self.window.communications_channel.send_queue.put(data)
        else:
            logger.debug(f"No item at dropped location")

            for i, item in enumerate(self.held_items):
                item.position = self.held_items_original_position[i]

        self.held_items = []

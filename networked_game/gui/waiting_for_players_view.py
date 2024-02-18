import logging

import arcade
import arcade.gui

from networked_game.gui.game_view_xml import GameViewXML

logger = logging.getLogger(__name__)


class WaitingForPlayersView(arcade.View):
    """Our custom Window Class"""

    def __init__(self, server=None):
        """Initializer"""
        # Call the parent class initializer
        super().__init__()

        self.gui_manager = None
        self.gui_manager = arcade.gui.UIManager()
        self.gui_manager.enable()

        self.server = server

        arcade.set_background_color(arcade.color.PAPAYA_WHIP)

        logger.debug(f"Have server {self.window.server}")
        if server:

            width = 250
            start_button = arcade.gui.UIFlatButton(
                text="Start Game",
                width=width,
                x=self.window.width / 2 - width / 2,
                y=50,
            )
            self.gui_manager.add(start_button)

            @start_button.event("on_click")
            def on_click_settings(_event):
                logger.debug(f"Start game")
                data = {"command": "start_game"}
                self.window.communications_channel.send_queue.put(data)

    def on_hide_view(self):
        self.gui_manager.disable()

    def on_update(self, delta_time):

        # Service client network tasks
        self.window.communications_channel.service_channel()

        # Are we a server? If so, service that
        if self.server:
            self.server.server_check()

        # Any messages to process?
        if not self.window.communications_channel.receive_queue.empty():
            data = self.window.communications_channel.receive_queue.get()
            if "state" in data and data["state"] == "running":
                self.window.game_data = data
                logger.debug("Message received, switching to game view.")
                view = GameViewXML()
                self.window.show_view(view)
            elif "users" in data:
                self.window.game_data = data

    def on_draw(self):
        arcade.start_render()

        # Draw buttons and stuff if we have them.
        if self.gui_manager:
            self.gui_manager.draw()

        x = 20
        y = self.window.height - 50

        arcade.draw_text(
            "Waiting For Players",
            start_x=x,
            start_y=y,
            color=arcade.color.BLACK,
            font_size=24,
            font_name="Kenney Future",
        )

        y -= 30
        ip = self.window.communications_channel.their_ip
        port = self.window.communications_channel.their_port
        arcade.draw_text(
            f"Server: {ip}:{port}",
            start_x=x,
            start_y=y,
            color=arcade.color.BLACK,
            font_size=24,
            font_name="Kenney Future",
        )

        y -= 30

        if self.window.game_data:
            users = self.window.game_data["users"]
            for user in users:
                y -= 30
                arcade.draw_text(
                    user,
                    start_x=x,
                    start_y=y,
                    color=arcade.color.BLACK,
                    font_size=24,
                    font_name="Kenney Future",
                )

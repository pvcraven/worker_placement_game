import arcade
import time
import logging

from networked_game.gui.constants import *
from networked_game.gui.waiting_for_players_view import WaitingForPlayersView
from networked_game.server.server import Server
from networked_game.network.communications_channel import CommunicationsChannel

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        self.communications_channel = None
        self.server = None
        self.game_data = None
        self.user_name = None

    def on_close(self):
        logger.debug("Closing connection...")
        if self.communications_channel:
            self.communications_channel.send_queue.put({"command": "logout"})
            while not self.communications_channel.send_queue.empty():
                self.communications_channel.service_channel()
                time.sleep(0.1)
            self.communications_channel.close()
        logger.debug("Closed.")
        self.close()

    def start_server(self, user_name, server_address, server_port):
        logger.debug(f"Starting server with user name {user_name}")

        # Create server
        self.server = Server(server_address, server_port)

        # Create server view
        view = WaitingForPlayersView(server=self.server)
        self.show_view(view)
        self.user_name = user_name

        self.communications_channel = CommunicationsChannel(their_ip=server_address,
                                                            their_port=server_port)
        self.communications_channel.connect()
        data = {"command": "login", "user_name": user_name}
        self.communications_channel.send_queue.put(data)

        self.server.server_check()

    def connect_to_server(self, user_name, server_address, server_port):
        self.communications_channel = CommunicationsChannel(their_ip=server_address, their_port=server_port)
        self.communications_channel.connect()
        data = {"command": "login", "user_name": user_name}
        self.communications_channel.send_queue.put(data)

        view = WaitingForPlayersView()
        self.show_view(view)

import argparse
import arcade
import logging

from networked_game.gui.client_or_server_view import ClientOrServerView
from networked_game.gui.game_window import GameWindow

import logging.config
import yaml


logger = logging.getLogger(__name__)

def main():
    """ Main function """

    # Set up logging
    with open('logging_config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    # Set up for any command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_name', help='Player\'s name.')
    parser.add_argument('--connect_to_server', help='Connect to a server.')
    parser.add_argument('--start_server', help='Start a server.')
    parser.add_argument('--port', help='Port name.')
    parser.add_argument('--address', help='Port name.')
    args = parser.parse_args()

    # Create our window
    window = GameWindow()

    # Process command line arguments
    user_name = args.user_name if args.user_name else "Bob"
    server_address = "127.0.0.1" if not args.address else args.address
    server_port = 10000 if not args.port else args.port
    if args.start_server:
        logger.info(f"Start server: {args.start_server}")
        window.start_server(user_name, server_address, server_port)
    elif args.connect_to_server:
        logger.info(f"Connect to server: {args.connect_to_server}")
        window.connect_to_server(user_name, server_address, server_port)
    else:
        # No arguments to skip screens, open up with first view
        # asking if this is a client or server
        view = ClientOrServerView()
        window.show_view(view)

    arcade.run()


if __name__ == "__main__":
    main()

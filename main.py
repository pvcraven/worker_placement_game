import argparse
import arcade
import logging

from networked_game.gui.client_or_server_view import ClientOrServerView
from networked_game.gui.game_window import GameWindow

logging.basicConfig(format='%(levelname)-7s %(filename)-35s %(lineno)-3d %(msecs)03d %(message)s', level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARN)


def main():
    """ Main function """

    parser = argparse.ArgumentParser()
    parser.add_argument('--user_name', help='Player\'s name.')
    parser.add_argument('--connect_to_server', help='Connect to a server.')
    parser.add_argument('--start_server', help='Start a server.')
    parser.add_argument('--port', help='Port name.')
    parser.add_argument('--address', help='Port name.')
    args = parser.parse_args()

    window = GameWindow()

    if args.start_server:
        print(f"Start server: {args.start_server}")
        user_name = args.user_name if args.user_name else "Bob"
        server_address = "127.0.0.1" if not args.address else args.address
        server_port = 10000 if not args.port else args.port
        window.start_server(user_name, server_address, server_port)
    elif args.connect_to_server:
        print(f"Connect to server: {args.connect_to_server}")
        user_name = args.user_name if args.user_name else "Bob"
        server_address = "127.0.0.1" if not args.address else args.address
        server_port = 10000 if not args.port else args.port
        window.start_server(user_name, server_address, server_port)

    else:
        view = ClientOrServerView()
        window.show_view(view)

    arcade.run()


if __name__ == "__main__":
    main()

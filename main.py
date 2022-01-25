import arcade
from gui.client_or_server_view import ClientOrServerView
from gui.game_window import GameWindow

import logging
logging.basicConfig(format='%(levelname)-7s %(filename)-35s %(lineno)-3d %(msecs)03d %(message)s', level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARN)


def main():
    """ Main function """

    window = GameWindow()
    start_view = ClientOrServerView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

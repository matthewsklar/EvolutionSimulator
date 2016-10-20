import random
from tkinter import Tk, Canvas, Frame, BOTH

import Board
import Creature
import Test
import Utils


class App(Frame):
    """
    The application

    Attributes:
        parent: Parent of the application
        width: An integer for the width of the application
        height: An integer for the height of the application
        canvas: A Canvas object for the application's canvas
    """

    def __init__(self, parent, width, height):
        """
        Initializes the application

        Args:
            parent: An object for the parent of the application
            width: An integer for the width of the application
            height: An integer for the height of the application
            tile_update: A list of Tile objects that have been updates since the last update
        """
        Frame.__init__(self, parent)  # Create the frame

        self.parent = parent
        self.width = width
        self.height = height

        center_window(self)

        self.parent.title("Evolution Simulator")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.create_tiles()
        Utils.creatures = Creature.create_creatures(Utils.init_creature_num, self.canvas)

        self.canvas.pack(fill=BOTH, expand=1)

        self.update_app()

    def create_tiles(self):
        """
        Creates the world tiles

        Raises:
            TypeError: Utils.tiles_per_row cannot be interpreted as an integer
        """
        r1 = random.random()
        r2 = random.random()

        for y in range(0, Utils.tiles_per_row):
            for x in range(0, Utils.tiles_per_row):
                tile = Board.Tile(x * Utils.tile_width,
                                  y * Utils.tile_width,
                                  0,
                                  int(Test.perlin(x / Utils.tiles_per_row, y / Utils.tiles_per_row, r1) * 255),
                                  int(Test.perlin(x / Utils.tiles_per_row, y / Utils.tiles_per_row, r2) * 255),
                                  self.canvas)
                Utils.tiles.append(tile)
                tile.draw()

    def update_app(self):
        """
        Main loop where all parts of the program that need updates are updated

        Raises:
            TypeError: self.init_creatures is not iterable
            AttributeError: self.update_app is not a function
        """
        for i in Utils.creatures:
            i.update()

        self.after(100, self.update_app)

        for tile in Utils.tile_update:
            tile.draw()
            Utils.tile_update.remove(tile)


def center_window(app):
    """
    Centers the window on the screen

    Args:
        app: An object for the application to center

    Raises:
        AttributeError: app is not the correct data type
    """
    screen_width = app.parent.winfo_screenwidth()
    screen_height = app.parent.winfo_screenheight()

    x = (screen_width - app.width) / 2
    y = (screen_height - app.height) / 2

    app.parent.geometry("%dx%d+%d+%d" % (app.width, app.height, x, y))

def init():
    """
    Initializes the application
    """
    root = Tk()
    App(root, Utils.app_width, Utils.app_height)
    root.mainloop()

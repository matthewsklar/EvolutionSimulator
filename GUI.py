from tkinter import Tk, Canvas, Frame, BOTH
import Board
import Utils
import random
import Test
import Creature


class App(Frame):
    def __init__(self, parent, width, height):
        # Create the frame
        Frame.__init__(self, parent)

        self.parent = parent
        self.width = width
        self.height = height

        self.center_window()

        self.parent.title("Evolution Simulator")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        create_tiles(self.canvas)
        self.init_creatures = Creature.create_creatures(Utils.init_creature_num, self.canvas)

        self.canvas.pack(fill=BOTH, expand=1)

        self.update_app()

    def center_window(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - self.width) / 2
        y = (screen_height - self.height) / 2

        self.parent.geometry("%dx%d+%d+%d" % (self.width, self.height, x, y))

    def update_app(self):
        for i in self.init_creatures:
            i.update()
        self.after(100, self.update_app)


def create_tiles(canvas):
    hi = random.random()
    by = random.random()

    for x in range(0, Utils.tiles_per_row):
        for y in range(0, Utils.tiles_per_row):
            tile = Board.Tile(x * Utils.tile_width,
                              y * Utils.tile_width,
                              0,
                              int(Test.perlin(x / Utils.tiles_per_row, y / Utils.tiles_per_row, hi) * 255),
                              int(Test.perlin(x / Utils.tiles_per_row, y / Utils.tiles_per_row, by) * 255))
            tile.draw(canvas)


def init():
    root = Tk()
    App(root, Utils.app_width, Utils.app_height)
    root.mainloop()

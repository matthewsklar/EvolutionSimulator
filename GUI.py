from tkinter import Tk, Canvas, Frame, BOTH
import Board
import Utils


class App(Frame):
    def __init__(self, parent, width, height):
        # Create the frame
        Frame.__init__(self, parent)

        self.parent = parent

        self.width = width
        self.height = height

        self.center_window()

        self.init_ui()

    def center_window(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - self.width) / 2
        y = (screen_height - self.height) / 2

        self.parent.geometry("%dx%d+%d+%d" % (self.width, self.height, x, y))

    def init_ui(self):
        self.parent.title("Evolution Simulator")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        self.create_tiles(canvas)
        canvas.pack(fill=BOTH, expand=1)

    @staticmethod
    def create_tiles(canvas):
        for x in range(0, Utils.tiles_per_row):
            for y in range(0, Utils.tiles_per_row):
                tile = Board.Tile(x * Utils.tile_width, y * Utils.tile_width, 0, 0, 255)
                tile.draw(canvas)


def run():
    root = Tk()
    App(root, Utils.app_width, Utils.app_height)
    root.mainloop()

if __name__ == "__main__":
    run()

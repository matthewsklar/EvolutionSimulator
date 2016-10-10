import Utils


class Tile(object):
    def __init__(self, x, y, r, g, b):
        self.x0 = x
        self.y0 = y
        self.x1 = x + Utils.tile_width
        self.y1 = y + Utils.tile_width
        print(r, g, b)
        # Default temperature and red value
        self.temp = clamp_rgb(r)

        # Amount of food and green value
        self.food = clamp_rgb(g)

        # Amount of water and blue value
        self.water = clamp_rgb(b)

    def draw(self, canvas):
        rgb_hex = "#%02x%02x%02x" % (self.temp, self.food, self.water)

        return canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, outline="black", fill=rgb_hex, width=2)


def clamp_rgb(x):
    return max(0, min(x, 255))

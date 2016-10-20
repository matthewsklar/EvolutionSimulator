import Utils
import GUI


class Tile(object):
    def __init__(self, x, y, r, g, b, canvas):
        self.x0 = x
        self.y0 = y
        self.x1 = x + Utils.tile_width
        self.y1 = y + Utils.tile_width

        # Default temperature and red value
        self.temp = clamp_rgb(r)

        # Amount of food and green value
        self.food = clamp_rgb(g)

        # Amount of water and blue value
        self.water = clamp_rgb(b)

        self.canvas = canvas

    def set_temp(self, temp):
        self.temp = temp
        Utils.tile_update.append(self)

    def set_food(self, food):
        self.food = food
        Utils.tile_update.append(self)

    def set_water(self, water):
        self.water = water
        Utils.tile_update.append(water)

    def draw(self):
        rgb_hex = Utils.rgb_to_hex(self.temp, self.food, self.water)

        self.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, outline="black", fill=rgb_hex)


def clamp_rgb(x):
    return max(0, min(x, 255))

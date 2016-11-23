import Utils


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

        rgb_hex = Utils.rgb_to_hex(self.temp, self.food, self.water)
        self.rectangle = self.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, outline="black", fill=rgb_hex)

    def set_temp(self, temp):
        self.temp = temp
        self.add_to_update()

    def set_food(self, food):
        self.food = food
        self.add_to_update()

    def set_water(self, water):
        self.water = water
        self.add_to_update()

    def add_to_update(self):
        if self not in Utils.tile_update:
            Utils.tile_update.append(self)

    def update(self):
        # TODO: use calculus to only update when Creature interacts
        if self.food < 255:
            self.set_food(Utils.clamp(self.food + 1, 0, 255))

        if self.water < 255:
            self.set_water(Utils.clamp(self.water + 1, 0, 255))

    def draw(self):
        rgb_hex = Utils.rgb_to_hex(self.temp, self.food, self.water)

        self.canvas.itemconfig(self.rectangle, fill=rgb_hex)
        self.canvas.coords(self.rectangle, self.x0, self.y0, self.x1, self.y1)


def clamp_rgb(x):
    return max(0, min(x, 255))

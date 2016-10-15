import math
import random

import NeuralNetwork
import Utils


class Creature(object):
    """
    The creature object

    Arguments:
        tag: A string for the tag used for Tkinter identification and grouping
        x: An integer for the x position between 0 and Utils.board_width
        y: An integer for the y position between 0 and Utils.board_width
        r: An integer for the red value between 0 and 255
        g: An integer for the green value between 0 and 255
        b: An integer for the blue value between 0 and 255
        food: An integer representing the amount of food the creature has stored
        direction_facing: An integer for the direction the creature is facing in degrees between 0 and 360
        speed: A float for the percentage of the maximum speed between 0 and 1
        reproduction: A boolean for the reproduction value where 0 means do not reproduce and 1 means reproduce
        radius: An integer for the radius
        speed_coefficient: An integer for the maximum speed
        canvas: A Canvas object for the application's canvas
    """

    def __init__(self, canvas, tag, *args):
        """
        Initializes the Creature

        Args:
            canvas: A Canvas object for the application's canvas
            tag: A string for the tag used for Tkinter identification and grouping
            args: A list of weights if the Creature has a parent
        """
        self.tag = "%s%d" % ("creature-", tag)
        self.x = int(random.random() * Utils.board_width)
        self.y = int(random.random() * Utils.board_height)
        self.r = int(random.random() * 255)
        self.g = int(random.random() * 255)
        self.b = int(random.random() * 255)
        self.food = 10
        self.direction_facing = int(random.random() * 360)
        self.speed = random.random()
        self.reproduction = round(random.random())
        self.radius = 10
        self.speed_coefficient = 10
        self.canvas = canvas

        rgb_hex = Utils.rgb_to_hex(self.r, self.g, self.b)
        center_x = self.x + self.radius
        center_y = self.y + self.radius

        self.body = self.canvas.create_oval(self.x, self.y, self.x + self.radius * 2, self.y + self.radius * 2,
                                            fill=rgb_hex, tags=self.tag)
        self.line = self.canvas.create_line(center_x, center_y,
                                            center_x + math.cos(self.direction_facing) * self.radius,
                                            center_y + math.sin(self.direction_facing) * self.radius,
                                            tags=self.tag)

        # Inputs: 0: Red, 1: Green, 2: Blue
        # Outputs: 0: Red, 1: Green, 2: Blue, 3: Direction Facing, 4: Speed, 5: Reproduction (maybe change to action for eat, drink, reproduce, fight, sleep (etc))
        self.network = NeuralNetwork.NeuralNetwork(3, 6, 1, 6)
        self.network.create_network()
        if len(args) == 0:
            self.network.create_weights()
        else:
            self.network.create_weights(args[0])

    def update(self):
        inputs = [self.r, self.g, self.b]
        outputs = self.network.calculate_network(inputs)

        #print("%s:%s" % (self.tag, str(outputs)))

        # TODO: Have output between 0 and 255 instead of scaling here (can do with sigmoid * 255)
        self.r = int(outputs[0] * 255)
        self.g = int(outputs[1] * 255)
        self.b = int(outputs[2] * 255)

        # TODO: Have output between 0 and 360 instead of scaling here (can do with sigmoid * 360)
        self.direction_facing = int(outputs[3] * 360)
        self.speed = outputs[4]
        self.reproduction = round(outputs[5])
        self.reproduce()

        self.move()
        self.draw()

        self.die()

    def reproduce(self):
        if self.reproduction:
            self.food -= 20
            if self.food >= 0:
                Utils.creatures.append(Creature(self.canvas, len(Utils.creatures), self.network.get_weights()))

    def die(self):
        if self.food <= 0:
            Utils.creatures.remove(self)
            self.canvas.delete(self.tag)
            del self

    def move(self):
        self.x += math.cos(self.direction_facing) * self.speed_coefficient * self.speed
        self.y += math.sin(self.direction_facing) * self.speed_coefficient * self.speed

    def draw(self):
        rgb_hex = Utils.rgb_to_hex(self.r, self.g, self.b)
        center_x = self.x + self.radius
        center_y = self.y + self.radius

        self.canvas.itemconfig(self.body, fill=rgb_hex)
        self.canvas.coords(self.body, self.x, self.y, self.x + self.radius * 2, self.y + self.radius * 2)
        self.canvas.coords(self.line, center_x, center_y, center_x + math.cos(self.direction_facing) * self.radius,
                           center_y + math.sin(self.direction_facing) * self.radius)


def create_creatures(num, canvas):
    creature_list = []

    for i in range(num):
        creature_list.append(Creature(canvas, i))

    return creature_list

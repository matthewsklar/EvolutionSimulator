import NeuralNetwork
import random
import Utils
import math


class Creature(object):
    def __init__(self, canvas, tag):
        self.tag = "%s%d" % ("creature-", tag)

        # x position (0 - Utils.board_width)
        self.x = int(random.random() * Utils.board_width)

        # y position (0 - Utils.board_height)
        self.y = int(random.random() * Utils.board_height)

        # Red value (0 - 255)
        self.r = int(random.random() * 255)

        # Green value (0 - 255)
        self.g = int(random.random() * 255)

        # Blue value (0 - 255)
        self.b = int(random.random() * 255)

        # Direction facing in degrees (0 - 360)
        self.direction_facing = int(random.random() * 360)

        # Percent of the maximum speed (0 - 1)
        self.speed = random.random()

        # Radius of the creature
        self.radius = 10

        # Maximum speed
        self.speed_constant = 10

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

        """
        Inputs:
        Outputs: Red, Green, Blue, Direction Facing, Direction Moving, Speed, Diameter
        """
        self.network = NeuralNetwork.NeuralNetwork(3, 7, 1, 6)
        self.network.create_network()

    def update(self):
        inputs = [self.r, self.g, self.b]
        outputs = self.network.calculate_network(inputs)

        print(outputs)

        # TODO: Have output between 0 and 255 instead of scaling here (can do with sigmoid * 255)
        self.r = int(outputs[0] * 255)
        self.g = int(outputs[1] * 255)
        self.b = int(outputs[2] * 255)

        # TODO: Have output between 0 and 360 instead of scaling here (can do with sigmoid * 360)
        self.direction_facing = int(outputs[3] * 360)
        self.speed = outputs[4]
        self.move()
        self.draw()

    def move(self):
        self.x += math.cos(self.direction_facing) * self.speed_constant * self.speed
        self.y += math.sin(self.direction_facing) * self.speed_constant * self.speed

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

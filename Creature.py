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
        action: A float for the current action
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
        self.food = 100
        self.direction_facing = int(random.random() * 360)
        self.speed = random.random()
        self.action = round(random.random())
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
        # Outputs: 0: Red, 1: Green, 2: Blue, 3: Direction Facing, 4: Speed,
        # 5: Action (eat, drink, reproduce, fight, sleep)
        self.network = NeuralNetwork.NeuralNetwork(3, 6, 1, 6)
        self.network.create_network()
        if len(args) == 0:
            self.network.create_weights()
        else:
            self.network.create_weights(args[0])

        print("Birth: %s" % self.tag)

    def update(self):
        inputs = [self.r, self.g, self.b]
        outputs = self.network.calculate_network(inputs)

        # print("%s:%s" % (self.tag, str(outputs)))

        # TODO: Have output between 0 and 255 instead of scaling here (can do with sigmoid * 255)
        self.r = int(outputs[0] * 255)
        self.g = int(outputs[1] * 255)
        self.b = int(outputs[2] * 255)

        # TODO: Have output between 0 and 360 instead of scaling here (can do with sigmoid * 360)
        self.direction_facing = int(outputs[3] * 360)
        self.speed = outputs[4]
        self.action = math.floor(6 * outputs[5])

        self.do_action()
        self.move()

        self.draw()

        self.die()

    def do_action(self):
        """
        Do the current action based on what the action output neuron's value is
        1 -> Eat
        2 -> Drink
        3 -> Reproduce
        4 -> Fight
        5 -> Sleep
        6 -> Nothing
        """
        if self.action == 0:
            self.eat()
        elif self.action == 1:
            self.drink()
        elif self.action == 2:
            self.reproduce()
        elif self.action == 3:
            self.fight()
        elif self.action == 4:
            self.sleep()

    def eat(self):
        pass

    def drink(self):
        pass

    def reproduce(self):
        self.food -= 100
        if self.food >= 0:
            Utils.creatures.append(Creature(self.canvas, len(Utils.creatures), self.network.get_weights()))

    def fight(self):
        pass

    def sleep(self):
        pass

    def die(self):
        if self.food <= 0:
            print("Death: %s" % self.tag)

            Utils.creatures.remove(self)
            self.canvas.delete(self.tag)
            del self

    def move(self):
        self.x += math.cos(self.direction_facing) * self.speed_coefficient * self.speed
        self.y += math.sin(self.direction_facing) * self.speed_coefficient * self.speed

        self.food -= self.speed_coefficient

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

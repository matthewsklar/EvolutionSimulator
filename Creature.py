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
        water: An integer representing the amount of water the creature has stored
        direction_facing: An integer for the direction the creature is facing in degrees between 0 and 360
        speed: A float for the percentage of the maximum speed between 0 and 1
        action: A float for the current action
        radius: An integer for the radius
        speed_coefficient: An integer for the maximum speed
        canvas: A Canvas object for the application's canvas
        tile: A Tile object for the occupied Tile
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
        self.x = int(random.random() * Utils.board_width) if len(args) == 0 else args[1]
        self.y = int(random.random() * Utils.board_height) if len(args) == 0 else args[2]
        self.r = int(random.random() * 255)
        self.g = int(random.random() * 255)
        self.b = int(random.random() * 255)
        self.food = Utils.birth_food
        self.water = Utils.birth_water
        self.direction_facing = int(random.random() * 360)
        self.speed = random.random()
        self.action = round(random.random())
        self.radius = 10
        self.speed_coefficient = 10
        self.canvas = canvas
        self.tile = Utils.get_tile(self.x, self.y)

        rgb_hex = Utils.rgb_to_hex(self.r, self.g, self.b)
        center_x = self.x + self.radius
        center_y = self.y + self.radius

        self.body = self.canvas.create_oval(self.x, self.y, self.x + self.radius * 2, self.y + self.radius * 2,
                                            fill=rgb_hex, tags=self.tag)
        self.line = self.canvas.create_line(center_x, center_y,
                                            center_x + math.cos(self.direction_facing) * self.radius,
                                            center_y + math.sin(self.direction_facing) * self.radius,
                                            tags=self.tag)

        # Inputs: 0: Red, 1: Green, 2: Blue, 3: Food, 4: Water
        # Outputs: 0: Red, 1: Green, 2: Blue, 3: Direction Facing, 4: Speed,
        # 5: Action (eat, drink, reproduce, fight, sleep)
        self.network = NeuralNetwork.NeuralNetwork(5, 6, 1, 6)
        self.network.create_network()
        if len(args) == 0:
            self.network.create_weights()
        else:
            self.network.create_weights(args[0])

        print("Birth: %s" % self.tag)

    def update(self):
        inputs = [self.r, self.g, self.b, self.food, self.water]
        outputs = self.network.calculate_network(inputs)

        self.tile = Utils.get_tile(self.x, self.y)

        # print("%s:%s" % (self.tag, str(outputs)))

        self.r = int(outputs[0] * 255)
        self.g = int(outputs[1] * 255)
        self.b = int(outputs[2] * 255)

        self.direction_facing = int(outputs[3] * 360)
        self.speed = outputs[4]
        self.action = math.floor(6 * outputs[5])

        self.do_action()
        self.move()

        self.draw()

        self.die()

    def do_action(self):
        """
        Do the current action based on what the action output neuron's value is:
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
        food_eaten = min(self.tile.food, 30)

        self.food += food_eaten
        self.tile.set_food(self.tile.food - food_eaten)

        print("%s has eaten %d: food = %d" % (self.tag, food_eaten, self.food))

    def drink(self):
        water_drunk = min(self.tile.water, 30)

        self.water += water_drunk
        self.tile.set_water(self.tile.water - water_drunk)

        print("%s has drunk %d: water = %d" % (self.tag, water_drunk, self.water))

    def reproduce(self):
        if self.food >= Utils.birth_food and self.water >= Utils.birth_water:
            self.food -= Utils.birth_food
            self.water -= Utils.birth_water

            Utils.creatures.append(
                Creature(self.canvas, len(Utils.creatures), self.network.get_weights(), self.x, self.y))

    def fight(self):
        pass

    def sleep(self):
        pass

    def die(self):
        if self.food <= 0 or self.water <= 0:
            print("Death: %s with food = %d and water = %d" % (self.tag, self.food, self.water))

            Utils.creatures.remove(self)
            self.canvas.delete(self.tag)
            del self

    def move(self):
        self.x += math.cos(self.direction_facing) * self.speed_coefficient * self.speed
        self.y += math.sin(self.direction_facing) * self.speed_coefficient * self.speed

        self.x %= Utils.board_width
        self.y %= Utils.board_height

        # TODO: Improve resource consumption algorithm
        self.food -= self.speed_coefficient / 4
        self.water -= self.speed_coefficient / 4

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

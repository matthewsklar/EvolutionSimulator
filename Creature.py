import math
import random

import NeuralNetwork
import Utils

vision = Utils.tile_width * 2


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
        left_eye_rad: A float representing the angle in radians between the left eye and forward between 0 and pi/2
        right_eye_rad: A float representing teh angle in radians between the right eye and forward between 0 and pi/2
        body: An oval for the body of the Creature
        left_eye: A line for the Creature's left eye
        right_eye: A line for the Creature's right eye
        network: A NeuralNetwork object for the Neural Network used by the Creature
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
        self.radius = (self.food + self.water) / 30
        self.speed_coefficient = 10
        self.canvas = canvas
        self.tile = Utils.get_tile(self.x, self.y)
        self.left_eye_rad = eye_rad(random.random()) if len(args) == 0 else args[3]
        self.right_eye_rad = eye_rad(random.random()) if len(args) == 0 else args[4]

        rgb_hex = Utils.rgb_to_hex(self.r, self.g, self.b)
        center_x = self.x + self.radius
        center_y = self.y + self.radius
        left_eye_pos = self.get_eye_pos(self.left_eye_rad)
        right_eye_pos = self.get_eye_pos(self.right_eye_rad)

        self.body = self.canvas.create_oval(self.x, self.y, self.x + self.radius * 2, self.y + self.radius * 2,
                                            fill=rgb_hex, tags=self.tag)
        self.left_eye = self.canvas.create_line(center_x, center_y, left_eye_pos[0], left_eye_pos[1], tags=self.tag)
        self.right_eye = self.canvas.create_line(center_x, center_y, right_eye_pos[0], right_eye_pos[1], tags=self.tag)

        self.network = NeuralNetwork.NeuralNetwork(13, 8, 1, 11)
        self.network.create_network()
        if len(args) == 0:
            self.network.create_weights()
        else:
            self.network.create_weights(args[0])

        print("Birth: %s" % self.tag)

    def get_eye_pos(self, eye_rads):
        """
        Calculate the coordinates of the Creature's vision

        Args:
            eye_rads: A float representing the degree in radians between the eye and forward

        Returns:
            A tuple containing the the x and y coordinates

        Raises:
            TypeError: eye_rads is an unsupported operand type
        """
        center_x = self.x + self.radius
        center_y = self.y + self.radius
        x = center_x + math.cos(self.direction_facing - eye_rads) * (self.radius + vision)
        y = center_y + math.sin(self.direction_facing - eye_rads) * (self.radius + vision)

        return x, y

    def update(self):
        """
        Update the Creature

        Raises:
            IndexError: List index out of range
        """
        left_eye = self.get_eye_pos(self.left_eye_rad)
        right_eye = self.get_eye_pos(self.right_eye_rad)

        left_tile = Utils.get_tile(left_eye[0], left_eye[1])
        right_tile = Utils.get_tile(right_eye[0], right_eye[1])

        # 0: Red, 1: Green, 2: Blue, 3: Food, 4: Water, 5: Left seen tile R, 6: Left seen tile G, 7: Left seen tile B,
        # 8: Right seen tile R, 9: Right seen tile G, 10: Right seen tile B, 11: Left eye radian, 12: Right eye radian
        inputs = [self.r, self.g, self.b, self.food, self.water, left_tile.temp, left_tile.food, left_tile.water,
                  right_tile.temp, right_tile.food, right_tile.water, self.left_eye_rad, self.right_eye_rad]

        # 0: Red, 1: Green, 2: Blue, 3: Direction Facing, 4: Speed, 5: Action (eat, drink, reproduce, fight, sleep),
        # 6: Left eye radian, 7: Right eye radian
        outputs = self.network.calculate_network(inputs)

        self.tile = Utils.get_tile(self.x, self.y)

        # print("%s:%s" % (self.tag, str(outputs)))

        self.r = int(outputs[0] * 255)
        self.g = int(outputs[1] * 255)
        self.b = int(outputs[2] * 255)

        self.direction_facing = int(outputs[3] * 360)
        self.speed = outputs[4]
        self.action = math.floor(6 * outputs[5])

        self.left_eye_rad = eye_rad(outputs[6])
        self.right_eye_rad = eye_rad(outputs[7])

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
        """
        Eat food to add food to the Creature and remove food from the Tile
        """
        food_eaten = min(self.tile.food, 30)

        self.food += food_eaten
        self.tile.set_food(self.tile.food - food_eaten)

        print("%s has eaten %d: food = %d" % (self.tag, food_eaten, self.food))

    def drink(self):
        """
        Drink water to add water to the Creature and remove water from the Tile
        """
        water_drunk = min(self.tile.water, 30)

        self.water += water_drunk
        self.tile.set_water(self.tile.water - water_drunk)

        print("%s has drunk %d: water = %d" % (self.tag, water_drunk, self.water))

    def reproduce(self):
        """
        If the Creature is able to reproduce, have it reproduce by creating a Creature using some of its resources at
        it's position with weights based off it's own
        """
        if self.food >= Utils.birth_food and self.water >= Utils.birth_water:
            self.food -= Utils.birth_food
            self.water -= Utils.birth_water

            Utils.creatures.append(
                Creature(self.canvas, Utils.total_creature_num, self.network.get_weights(), self.x, self.y,
                         self.left_eye_rad, self.right_eye_rad))
            Utils.total_creature_num += 1

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
        left_eye = self.get_eye_pos(self.left_eye_rad)
        right_eye = self.get_eye_pos(self.right_eye_rad)

        self.canvas.itemconfig(self.body, fill=rgb_hex)
        self.canvas.coords(self.body, self.x, self.y, self.x + self.radius * 2, self.y + self.radius * 2)

        self.canvas.coords(self.left_eye, center_x, center_y, left_eye[0], left_eye[1])
        self.canvas.coords(self.right_eye, center_x, center_y, right_eye[0], right_eye[1])


def eye_rad(x):
    return x * (math.pi / 2)


def create_creatures(num, canvas):
    creature_list = []

    for i in range(num):
        creature_list.append(Creature(canvas, i))

    return creature_list

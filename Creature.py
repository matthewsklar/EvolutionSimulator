import NeuralNetwork
import random
import Utils


class Creature(object):
    def __init__(self):
        self.x = int(random.random() * Utils.board_width)
        self.y = int(random.random() * Utils.board_height)

        self.r = int(random.random() * 255)
        self.g = int(random.random() * 255)
        self.b = int(random.random() * 255)

        print("Creature created at", self.x, self.y)

        """
        Inputs:
        Outputs: Red, Green, Blue, Direction Facing, Direction Moving, Speed
        """
        self.network = NeuralNetwork.NeuralNetwork(3, 3, 2, 2)
        self.network.create_network()

    def update(self, canvas):
        inputs = [self.r, self.g, self.b]
        outputs = self.network.calculate_network(inputs)
        print(outputs)
        self.r = int(outputs[0] * 255)
        self.g = int(outputs[1] * 255)
        self.b = int(outputs[2] * 255)

        self.draw(canvas)

    def draw(self, canvas):
        rgb_hex = Utils.rgb_to_hex(self.r, self.g, self.b)
        print(rgb_hex)
        return canvas.create_oval(self.x, self.y, self.x + 50, self.y + 50, fill=rgb_hex)

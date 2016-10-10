# Imports
import random
import math


# The neurons making up neuron layers
class Neuron(object):
    def __init__(self, inputs):
        # Number if inputs in the neuron
        self.inputs = inputs

        # Weights in the neuron
        self.weights = []

        # Bias of the neuron
        self.bias = random.random() * 2 - 1

        # The error of the neuron
        self.delta = 0

        # The output of the neuron
        self.output = 0

        # Create the weights
        self.create_weights()

    def create_weights(self):
        """
        Add a random number between -1 and 1 for each weight
        """
        for x in range(0, self.inputs):
            self.weights.append(random.random() * 2 - 1)


class NeuronLayer(object):
    def __init__(self, num_neurons, inputs_per_neuron):
        # Number of neurons in the layer
        self.num_neurons = num_neurons

        # Neurons in the layer
        self.neurons = []

        # Create the neurons
        self.create_neurons(inputs_per_neuron)

    def create_neurons(self, inputs):
        """
        Add the neurons to the layer
        """
        for i in range(0, self.num_neurons):
            self.neurons.append(Neuron(inputs))


class NeuralNetwork(object):
    def __init__(self, num_inputs, num_outputs, num_hidden_layers, num_neurons_per_hidden_layer):
        # Number of input neurons
        self.num_inputs = num_inputs

        # Number of output neurons
        self.num_outputs = num_outputs

        # Number of hidden layers
        self.num_hidden_layers = num_hidden_layers

        # Number of neurons in a hidden layer
        self.num_neurons_per_hidden_layer = num_neurons_per_hidden_layer

        # Layers
        self.layers = []

    def create_network(self):
        """
        Create the neural network
        """
        # Create the input layer
        self.layers.append(NeuronLayer(self.num_inputs, 1))

        # Create the hidden layers
        for i in range(0, self.num_hidden_layers):
            self.layers.append(NeuronLayer(self.num_neurons_per_hidden_layer, self.layers[i - 1].num_neurons - 1))

        # Create the output layer
        self.layers.append(NeuronLayer(self.num_outputs, self.num_neurons_per_hidden_layer))

    def calculate_network(self, inputs):
        """
        Calculate the output layer
        """
        # Stores the resultant outputs from each layer
        outputs = []

        # Check that the correct amount of inputs are available
        if len(inputs) != self.num_inputs:
            print("Aborting network: Inconsistent inputs for input size")

            return outputs

        for i in range(0, self.num_hidden_layers + 1):
            # If it is not the first layer, the inputs are the previous outputs
            if i > 0:
                inputs.clear()

                for o in outputs:
                    inputs.append(o)

            outputs.clear()
            corr_weight = 0

            # For each neuron in the layer
            for j in self.layers[i + 1].neurons:
                net = 0

                # For each weight in the neuron
                for k in j.weights:
                    # Add the product (weight * input) to the sum
                    net += k * inputs[corr_weight]

                    corr_weight += 1

                # Add the bias to the sum
                # TODO: Multiply bias by constant
                net += j.bias

                # Filter the output of the neuron then add it to the outputs
                j.output = Sigmoid(net)

                outputs.append(j.output)

                corr_weight = 0

        return outputs


def Sigmoid(t):
    """
    The sigmoid transfer function
              1
    S(t) = -------
            1+e^t
    """
    return 1 / (1 + math.e ** -t)

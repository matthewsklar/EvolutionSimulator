# Imports
import random


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

    '''
    Add a random number between -1 and 1 for each weight
    '''

    def create_weights(self):
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

    '''
    Add the neurons to the layer
    '''
    def create_neurons(self, inputs):
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

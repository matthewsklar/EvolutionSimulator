import random
import math
import Utils


class Neuron(object):
    """
    Individual neurons

    Attributes:
        inputs: An integer count of the inputs of the neuron
        weights: A list of the weights of the neuron
        bias: A float for the bias of the neuron
        delta: A float for the delta (error) of the neuron
        output: A float of the output of the neuron
    """

    def __init__(self, inputs):
        """
        Initializes the Neuron

        Args:
            inputs: An integer count of the inputs of the neuron
        """
        self.inputs = inputs
        self.weights = []
        self.bias = random.random() * 2 - 1
        self.delta = 0
        self.output = 0

    def create_weights(self):
        """
        Creates the weights by adding a random number between -1 and 1 for each weight

        Raises:
            TypeError: self.inputs cannot be interpreted as an integer
        """
        for x in range(0, self.inputs):
            self.weights.append(random.random() * 2 - 1)

    def set_weight(self, weights):
        """
        Creates weights using predetermined values. Based on the mutation rate,
        there is a chance that mutations occur causing random rates to be replaced with random numbers between -1 and 1.

        Args:
            weights: A list representing the predetermined value for weights

        Raises
            TypeError: weights is not iterable
        """
        weights = list(map(lambda x: x if random.random() > Utils.mutation_rate else random.random() * 2 - 1, weights))

        self.weights = weights


class NeuronLayer(object):
    """
    Layers of neurons: can be input, hidden, or output layer

    Attributes:
        num_neurons: An integer count of the neurons in the layer
        neurons: A list of the Neurons in the layer
    """

    def __init__(self, num_neurons, inputs_per_neuron):
        """
        Initializes the Neuron

        Args:
            num_neurons: An integer count of the neurons in the layer
            inputs_per_neuron: An integer count of the amount of inputs of each neuron in the layer
        """
        self.num_neurons = num_neurons
        self.neurons = []

        self.create_neurons(inputs_per_neuron)

    def create_neurons(self, inputs):
        """
        Creates the neurons and adds them to the list neurons

        Args:
            inputs: An integer count of the amount of inputs of each neuron in the layer

        Raises:
            TypeError: self.num_neurons cannot be interpreted as an integer
        """
        for i in range(0, self.num_neurons):
            self.neurons.append(Neuron(inputs))


class NeuralNetwork(object):
    """
    Creates a neural network and runs it

    Attributes:
        num_inputs: An integer count of the input neurons
        num_outputs: An integer count of the output neurons
        num_hidden_layers: An integer count of the hidden layers
        num_neurons_per_hidden_layer: An integer count of the neurons in a hidden layer
        layers: A list of each NeuronLayer
    """

    def __init__(self, num_inputs, num_outputs, num_hidden_layers, num_neurons_per_hidden_layer):
        """
        Initializes the NeuralNetwork

        Args:
            num_inputs: An integer count of the input neurons
            num_outputs: An integer count of the output neurons
            num_hidden_layers: An integer count of the hidden layers
            num_neurons_per_hidden_layer: An integer count of the neurons in a hidden layer
        """
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.num_hidden_layers = num_hidden_layers
        self.num_neurons_per_hidden_layer = num_neurons_per_hidden_layer
        self.layers = []

    def create_network(self):
        """
        Creates the neural network

        Raises:
            TypeError: self.num_inputs, self.num_hidden_layers, self.num_neurons_per_hidden_layer, self.num_outputs
            cannot all be interpreted as an integer
        """
        self.layers.append(NeuronLayer(self.num_inputs, 1))  # Create the input layer

        for i in range(0, self.num_hidden_layers):
            self.layers.append(NeuronLayer(self.num_neurons_per_hidden_layer,
                                           self.layers[i - 1].num_neurons))  # Create the hidden layers

        self.layers.append(
            NeuronLayer(self.num_outputs, self.num_neurons_per_hidden_layer))  # Create the output layer

    def create_weights(self, *args):
        """
        Create the weights of each neuron either randomly if their are no given weights from a parent,
        or base them on the weights from a parent.

        Args:
            args: Either nothing or a list containing the list of weights from the parent

        Raises:
            TypeError: args[0] is not subscriptable
        """
        is_random = len(args) == 0
        neurons_counted = 0
        for layer in self.layers:  # For each layer in the neural network
            for neuron in layer.neurons:  # For each neuron in the layer
                if is_random:
                    neuron.create_weights()
                else:
                    neuron.set_weight(args[0][neurons_counted])
                    neurons_counted += 1

    def get_weights(self):
        """
        Get all the weights in the neural network

        Return:
            A list of all the weights in the neural network
        """

        weight = []
        for i, layer in enumerate(self.layers):  # For each layer in the neural network
            for j, neuron in enumerate(layer.neurons):  # For each neuron in the layer
                # print("(%d, %d): %s" % (i, j, str(neuron.weights)))
                weight.append(neuron.weights)

        return weight

    def calculate_network(self, inputs):
        """
        Calculate the output layer

        Args:
            inputs: A list of Neurons in the input layer

        Returns:
            A list of outputs of neurons from the output layer. For example

            [.1, .5, .3]
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
                j.output = sigmoid(net)

                outputs.append(j.output)

                corr_weight = 0

        return outputs


def sigmoid(t):
    """
    The sigmoid transfer function
              1
    S(t) = -------
            1+e^-t

    Args:
        t: An int for the t in S(t)

    Returns:
        A float representing the output from the sigmoid function with t as the input.
        If math.e ** -t causes an overflow error, then the output is rounded to 0.
    """
    try:
        return 1 / (1 + math.e ** -t)
    except OverflowError:
        return 0

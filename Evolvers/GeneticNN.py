import random
import copy

class Neuron:
    def __init__(self, type="neuron", prev_layer=1):
        self.type = str(type)

        self.input_weights = [2 * (random.random()-0.5) for i in range(prev_layer)]

    def __repr__(self):
        if self.type == "neuron":
            return "<Neuron with input weights of " + str(self.input_weights) + ">"
        else:
            return "< " + str(self.type) + " Neuron with input weights of " + str(self.input_weights) + ">"

class Network:
    def __init__(self, layers=[], neurons=[]):
        self.layers = layers
        self.layer_count = len(layers)
        self.neurons = []

        for layer_no, layer in enumerate(layers):
            self.neurons += [[]]
            for neuron in range(layer):
                if layer_no == 0:
                    self.neurons[-1] += [Neuron(type="input")]
                else:
                    self.neurons[-1] += [Neuron(prev_layer=layers[layer_no - 1])]

    def get_architecture(self):
        return str(self.neurons)

    def get_layer_output(self, data, layer_no):
        if (len(data) != self.layers[layer_no]) and (len(data) != len(self.neurons[layer_no][0].input_weights)):
            raise IndexError("Data length of " + str(len(data)) + " does not match layer length of " + str(self.layers[layer_no]) + ".")

        if self.layer_count - 1 < layer_no:
            raise IndexError("Layer " + str(layer_no) + " does not exist. Maximum value is " + str(self.layer_count - 1))

        neuron_outputs = []

        if layer_no == 0:
            for n_neuron, neuron in enumerate(self.neurons[layer_no]):
                neuron_input = data[n_neuron]

                neuron_output = neuron_input * neuron.input_weights[0]

                neuron_outputs += [neuron_output]

            return neuron_outputs

        else:
            for neuron in self.neurons[layer_no]:
                neuron_inputs = data.copy()

                for element, value in enumerate(neuron_inputs):
                    neuron_inputs[element] = value * neuron.input_weights[element] #Apply input weights

                neuron_output = sum(neuron_inputs)

                neuron_outputs += [neuron_output]

            return neuron_outputs

    def predict(self, data):

        last_output = data.copy()

        if len(data) != self.layers[0]:
            raise IndexError("Input length of " + str(len(data)) + " does not match input layer length of " + str(self.layers[0]) + ".")

        for layer_no in range(self.layer_count):
            last_output = self.get_layer_output(last_output, layer_no)

        return last_output

    def mutate(self):
        mutated = copy.deepcopy(self)

        for i in range(random.randint(1, 5)):
            random_layer = random.randint(0, self.layer_count - 1)
            random_neuron = random.randint(0, len(self.neurons[random_layer]) - 1)

            random_position = random.randint(0, len(mutated.neurons[random_layer][random_neuron].input_weights) - 1)

            mutated.neurons[random_layer][random_neuron].input_weights[random_position] += random.choice([-1, 1]) * random.choice([1, 0.1, 0.1, 0.1, 0.01])

        return mutated

import numpy as np


class Neural:
    def __init__(self, input_layer, hidden_layer, output_layer):
        self.input_layer = input_layer
        self.hidden_layer = hidden_layer
        self.output_layer = output_layer
        self.weights_input_to_hidden = np.random.uniform(-0.5, 0.5, (self.hidden_layer, self.input_layer))
        self.weights_hidden_to_output = np.random.uniform(-0.5, 0.5, (self.output_layer, self.hidden_layer))
        self.bias_input_to_hidden = np.zeros((hidden_layer, 1))
        self.bias_hidden_to_output = np.zeros((output_layer, 1))
    
    def training(self, learning_rate, input_data, output_data):

        hidden_raw = self.bias_input_to_hidden + self.weights_input_to_hidden @ input_data
        hidden = 1 / (1 + np.exp(-hidden_raw))

        output_raw = self.bias_hidden_to_output + self.weights_hidden_to_output @ hidden
        output = 1 / (1 + np.exp(-output_raw))

        #Обучение Backpropagation (output layer)
        delta_output = output - output_data
        self.weights_hidden_to_output += -learning_rate * delta_output @ np.transpose(hidden)
        self.bias_hidden_to_output += -learning_rate * delta_output

        #Обучение Backpropagation (hidden layer)
        delta_hidden = np.transpose(self.weights_hidden_to_output) @ delta_output * (hidden * (1 - hidden))
        self.weights_input_to_hidden += -learning_rate * delta_hidden @ np.transpose(input_data)
        self.bias_input_to_hidden += -learning_rate * delta_hidden

        return output


    def usage(self, input_data):
        hidden_raw = self.bias_input_to_hidden + self.weights_input_to_hidden @ input_data
        hidden = 1 / (1 + np.exp(-hidden_raw))

        output_raw = self.bias_hidden_to_output + self.weights_hidden_to_output @ hidden
        output = 1 / (1 + np.exp(-output_raw))

        return output
    
    def save_weights(self, file='model'):
        np.savez(file, weights_input_to_hidden=self.weights_input_to_hidden, weights_hidden_to_output=self.weights_hidden_to_output, bias_input_to_hidden=self.bias_input_to_hidden, bias_hidden_to_output=self.bias_hidden_to_output)

    def load_weights(self, file='model'):
        data = np.load(file + '.npz')
        self.weights_input_to_hidden = data['weights_input_to_hidden']
        self.weights_hidden_to_output = data['weights_hidden_to_output']
        self.bias_input_to_hidden = data['bias_input_to_hidden']
        self.bias_hidden_to_output = data['bias_hidden_to_output']
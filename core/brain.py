# Standard Library Imports
import random

# Third-Party Imports
import numpy as np

class Brain:
    def __init__(self, size):
        self.size = size
        self.weights = [np.random.randn(y, x) for x, y in zip(size[:-1], size[1:])]
        self.biases = [np.random.randn(y, 1) for y in size[1:]]

    def feed_forward(self, data):
        i = 0
        for b, w in zip(self.biases, self.weights):
            activation = np.dot(w, data) + b
            if i == 0:
                data = ReLU(activation)
                data = softmax(data)
            else:
                data = sigmoid(activation)
            i += 1
        data = softmax(data)

        controller = []

        for i in range(len(data)):
            controller.append(np.max(data[i]))

        val = np.argmax(controller)

        if val == 0:
            return 1
        elif val == 1:
            return 0
        else:
            return -1

    def crossover(self, other):
        newBrain1 = Brain(self.size)
        newBrain2 = Brain(self.size)
        
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                for k in range(len(self.weights[i][j])):
                    if random.randint(0, 1):                        
                        newBrain1.weights[i][j][k] = self.weights[i][j][k]
                        newBrain2.weights[i][j][k] = other.weights[i][j][k]
                    else:
                        newBrain1.weights[i][j][k] = other.weights[i][j][k]
                        newBrain2.weights[i][j][k] = self.weights[i][j][k]

        for i in range(len(self.biases)):
            for j in range(len(self.biases[i])):
                for k in range(len(self.biases[i][j])):
                    if random.randint(0, 1):                        
                        newBrain1.biases[i][j][k] = self.biases[i][j][k]
                        newBrain2.biases[i][j][k] = other.biases[i][j][k]
                    else:
                        newBrain1.biases[i][j][k] = other.biases[i][j][k]
                        newBrain2.biases[i][j][k] = self.biases[i][j][k]

        return newBrain1, newBrain2

    def mutation(self, mutation_rate, mutation_coef, seed=None):

        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
    
        if random.random() <= mutation_rate / 100.0:

            for i in range(len(self.weights)):
                mutation_mask = np.random.rand(*self.weights[i].shape) < mutation_rate / 100.0
                self.weights[i] += mutation_mask * np.random.randn(*self.weights[i].shape) * mutation_coef

            for i in range(len(self.biases)):
                mutation_mask = np.random.rand(*self.biases[i].shape) < mutation_rate / 100.0
                self.biases[i] += mutation_mask * np.random.randn(*self.biases[i].shape) * mutation_coef

def ReLU(data):
    data[data < 0] = 0
    return data

def sigmoid(data):
    return 1.0/(1.0 + np.exp(-data))

def softmax(data):
    summation = np.sum(data)

    if summation == 0.0:
        summation = 1.0
    
    for i in range(len(data)):
        data[i] = data[i]/summation

    return data

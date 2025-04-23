import numpy as np

class Perceptron:
    def __init__ (self, entryValues , weights , bias , typeAct ):
        self.entryValues = entryValues
        self.weights = weights
        self.bias = bias
        self.summation = 0
        self.typeAct = typeAct


    def activation(self):
        match self.typeAct:
            case 'escalon':
                return 1 if self.summation >= 0 else 0
            case 'sigmoide': 
                return 1/(1+np.exp(-self.summation))
                


    def finalValue(self):
        for i in range(len(self.entryValues)):
            self.summation += self.entryValues[i] * self.weights[i]
        self.summation += self.bias
        return self.activation()







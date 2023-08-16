import numpy as np
import matplotlib.pyplot as plt
import random
import json
from time import time

class ActivationFunctions:
    class Sigmoid:
        identifier = 0

        def Function (input):
            return 1.0 / (1.0 + np.exp(-input))
        
        def WeightInitiation (numNodesIn, numNodesOut, seed = time()):
            weights = []
            random.seed(seed)

            for row in range(numNodesIn):
                weights.append([])

                for col in range(numNodesOut):
                    randVal = random.uniform(-1, 1) * 2 - 1
                    weights[row].append(randVal / np.sqrt(numNodesIn))

            return weights
        
        def Derivative (input):
            pass

    IdentifierDict = {0 : Sigmoid}

class LabledData:
    def __init__ (self, input, output):
        self.input = input
        self.output = output
    
class Layer:
    def __init__ (self, numNodesIn, numNodesOut, activationFunctionClass):
        self.numNodesIn = numNodesIn
        self.numNodesOut = numNodesOut
        self.activationFunctionClass = activationFunctionClass

        self.weights = self.activationFunctionClass.WeightInitiation(self.numNodesIn, self.numNodesOut).copy()
        self.biases = [0 for i in range(self.numNodesOut)]
        self.weightGradients = [[0 for i in range(self.numNodesOut)] for i in range(self.numNodesIn)]
        self.biasGradients = [0 for i in range(self.numNodesOut)]
 
    def ApplyGradients (self, learnRate):
        for nodeOut in range(self.numNodesOut):
            self.biases[nodeOut] -= self.biasGradients[nodeOut] * learnRate

            for nodeIn in range(self.numNodesIn):
                self.weights[nodeIn][nodeOut] -= self.weightGradients[nodeIn][nodeOut] * learnRate

    def CalculateOutput (self, inputs):
        Outputs = [0 for i in range(self.numNodesOut)]

        for nodeOut in range(self.numNodesOut):
            Outputs[nodeOut] += self.biases[nodeOut]

            for nodeIn in range(self.numNodesIn):
                Outputs[nodeOut] += inputs[nodeIn] * self.weights[nodeIn][nodeOut]
                
            Outputs[nodeOut] = self.activationFunctionClass.Function(Outputs[nodeOut])

        return Outputs
    
class NeuralNetwork:
    def __init__ (self, layerLayout, activationFunctionClass):
        self.layerLayout = layerLayout
        self.layers = [None for i in range(len(layerLayout) - 1)]
        self.activationFunctionClass = activationFunctionClass

        for index in range(len(layerLayout) - 1):
            self.layers[index] = Layer(layerLayout[index], layerLayout[index + 1], activationFunctionClass)

        self.Costs = np.array([])

    def CalculateOutput (self, input):
        for layer in self.layers:
            input = layer.CalculateOutput(input)

        return input
    
    def CalculateCostSingle (self, dataPoint):
        output = self.CalculateOutput(dataPoint.input)
        cost = 0

        for nodeOut in range(len(output)):
            cost += CalculateError(output[nodeOut], dataPoint.output[nodeOut])

        return cost
    
    def CalculateCost (self, dataPoints):
        totalCost = 0

        for dataPoint in dataPoints:
            totalCost += self.CalculateCostSingle(dataPoint)

        return totalCost / len(dataPoints)
    
    def Learn (self, trainingData, learnRate, repeat = 1):
        H = 0.001

        for r in range(repeat):
            OriginalCost = self.CalculateCost(trainingData)
            self.Costs = np.append(OriginalCost, self.Costs)

            for layer in self.layers:

                for nodeIn in range(layer.numNodesIn):
                    for nodeOut in range(layer.numNodesOut):
                        OriginalWeight = layer.weights[nodeIn][nodeOut]

                        layer.weights[nodeIn][nodeOut] += H
                        newCost = self.CalculateCost(trainingData)
                        layer.weights[nodeIn][nodeOut] = OriginalWeight

                        gradientApprox = (newCost - OriginalCost) / H
                        layer.weightGradients[nodeIn][nodeOut] = gradientApprox

                for biasIndex in range(layer.numNodesOut):
                    OriginalBias = layer.biases[biasIndex]

                    layer.biases[biasIndex] += H
                    newCost = self.CalculateCost(trainingData)
                    layer.biases[biasIndex] = OriginalBias

                    gradientApprox = (newCost - OriginalCost) / H
                    layer.biasGradients[biasIndex] = gradientApprox

                layer.ApplyGradients(learnRate)

            #print(f"Cost: {self.CalculateCost(trainingData)}")

    def Predict (self, input):
        return self.CalculateOutput(input)
    
    def SaveNetwork (self, fileName):
        weights = [layer.weights for layer in self.layers]
        biases = [layer.biases for layer in self.layers]
        data = {"Layout" : self.layerLayout, "Weights" : weights, "Biases" : biases, "Actiation Function ID" : self.activationFunctionClass.identifier}

        try:
            with open(fileName, 'w') as file:
                json.dump(data, file)

            return True
        
        except Exception:
            return False

    def LoadNetwork (fileName):
        with open(fileName, 'r') as file:
            data = json.load(file)

        DataLayerLayout = data["Layout"]
        DataWeights = data["Weights"]
        DataBiases = data["Biases"]
        DataActivationFunctionIdentifier = data["Actiation Function ID"]

        NewNetwork = NeuralNetwork(DataLayerLayout, ActivationFunctions.IdentifierDict[DataActivationFunctionIdentifier])

        for layerIndex, layer in enumerate(NewNetwork.layers):
            layer.biases = DataBiases[layerIndex]

            for nodeIn in range(layer.numNodesIn):
                layer.weights = DataWeights[layerIndex]

        return NewNetwork


def CalculateError (value, expectedValue):
    error = value - expectedValue
    return error * error

def CreateLabledData (inputList, outputList):
    result = []

    for index in range(len(inputList)):
        input = inputList[index]
        output = outputList[index]
        result.append(LabledData(input, output))

    return result

def main():
    #inputs = [[1, 10],  [0.9, 11],  [4.9, 5],   [1.1, 9],   [4.5, 4],   [1.2, 12],  [1.2, 9],   [5.2, 3],   [0.5, 12],  [6.4, 4],   [0.8, 10],  [5.9, 5],   [1.3, 11],  [1, 12],    [6.1, 4],   [0.7, 9],   [1.3, 12],  [6.2, 5]]
    #outputs = [[1, 0],  [1, 0],     [0, 1],     [1, 0],     [0, 1],     [1, 0],     [1, 0],     [0, 1],     [1, 0],     [0, 1],     [1, 0],     [0, 1],     [1, 0],     [1, 0],     [0, 1],     [1, 0],     [1, 0],     [0, 1]]
    #trainingData = CreateLabledData(inputs, outputs)
#
    #Network = NeuralNetwork([2, 10, 2], ActivationFunctions.Sigmoid)
    #Network.Learn(trainingData, 0.005, 1000)
    #Network.SaveNetwork("Test.json")
    LoadedNetwork = NeuralNetwork.LoadNetwork("Fruits.json")
    print(LoadedNetwork.Predict([1, 10]))

if __name__ == "__main__":
    main()
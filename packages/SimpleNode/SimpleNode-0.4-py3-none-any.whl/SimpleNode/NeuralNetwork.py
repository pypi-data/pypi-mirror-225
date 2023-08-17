import numpy as np
import json

from SimpleNode.ActivationFunctions import ActivationFunctions
from SimpleNode.Layer import Layer
    
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
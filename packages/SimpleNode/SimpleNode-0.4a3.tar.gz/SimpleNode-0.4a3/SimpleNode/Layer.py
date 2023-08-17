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
import numpy as np
import random

class ActivationFunctions:
    class Sigmoid:
        identifier = 0

        def Function (input):
            return 1.0 / (1.0 + np.exp(-input))
        
        def WeightInitiation (numNodesIn, numNodesOut):
            weights = []

            for row in range(numNodesIn):
                weights.append([])

                for col in range(numNodesOut):
                    randVal = random.uniform(-1, 1) * 2 - 1
                    weights[row].append(randVal / np.sqrt(numNodesIn))

            return weights
        
        def Derivative (input):
            pass

    IdentifierDict = {0 : Sigmoid}
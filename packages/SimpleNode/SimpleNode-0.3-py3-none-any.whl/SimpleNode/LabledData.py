class LabledData:
    def __init__ (self, input, output):
        self.input = input
        self.output = output

def CreateLabledData (inputList, outputList):
    result = []

    for index in range(len(inputList)):
        input = inputList[index]
        output = outputList[index]
        result.append(LabledData(input, output))

    return result
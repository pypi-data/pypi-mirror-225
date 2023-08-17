import csv

class LabledData:
    def __init__ (self, input, output):
        self.input = input
        self.output = output

    def CreateLabledData (inputList, outputList):
        LableList = []

        for index in range(len(inputList)):
            input = inputList[index]
            output = outputList[index]
            LableList.append(LabledData(input, output))

        return LableList

    def CreateLabledDataFromCSV (csvFilePath, lableName):
        LableList = []

        with open(csvFilePath) as file:
            dataDict = csv.DictReader(file)

            for row in dataDict:
                output = row[lableName]
                input = list(row.values())
                input.remove(output)

                LableList.append(LabledData(input, output))

        return LableList
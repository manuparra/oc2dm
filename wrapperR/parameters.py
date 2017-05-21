import pandas as pd


class Parameters():
    def __init__(self, dataset, formula, input_parameter):
        self.input = self.__parser(input_parameter)
        self.dataset = dataset
        self.output_route = self.__dataset_parser(dataset)
        self.formula = formula

    def __parser(self, input_parameters):
        string = ''
        for key, value in input_parameters.items():
            if (value != None):
                string += key + ' = ' + value + ', '
        return string

    def __dataset_parser(self, dataset):
        split = dataset.rsplit('/', 1)
        if len(split) > 1:
            return split[0]
        else:
            return ''

    def __read_dataset(self):
        self.dataset = pd.read_csv(self.dataset, header=None, sep=" ")

    def getDataset(self):
        self.__read_dataset()
        return self.dataset


formula = "mpg~disp"
entrada = {"param1": "hola", "param2": "adios", "param3": None, "param4": "caracola"}
p = Parameters("dataset.csv", formula, entrada)

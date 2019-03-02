from matplotlib import pyplot as plt
import numpy as np

class PlotterDataCreator:
    pass

class StackedBarGraphPlotterDataCreator(PlotterDataCreator):

    def __init__(self, model):
        self.numerical_model = model
        value_tuples = self.get_x_y_and_chatter_tuples()
        self.x_values = value_tuples[0]
        self.y_dict = value_tuples[1]

    def get_x_y_and_chatter_tuples(self):
        model_dict = self.numerical_model.get_model_data()
        x_values = model_dict.keys()
        chatters_values = {}
        for key in x_values:
            for chatter in model_dict[key]:
                if chatter not in chatters_values:
                    chatters_values[chatter] = []
                chatters_values[chatter].append(model_dict[key][chatter])
        return x_values, chatters_values

    def get_x_values(self):
        return self.x_values

    def get_y_dict(self):
        return self.y_dict


class Plotter:
    pass

class StackedBarGraphPlotter(Plotter):
    title = ''
    y_label = ''
    x_label = ''
    width = 0.5

    def __init__(self, graph_data_creator):
        self.graph_data_creator = graph_data_creator

    def get_padded_list(self, original, to_pad_to):
        if to_pad_to >= len(original):
            return np.pad(original, (0, to_pad_to - len(original)), 'constant')

    def plot(self):
        x_values = self.graph_data_creator.get_x_values()
        print x_values
        indices = np.arange(len(x_values))
        y_vals = self.graph_data_creator.get_y_dict()
        keys = y_vals.keys()
        chatter1_values = tuple(self.get_padded_list(y_vals[keys[0]], len(x_values)))
        chatter2_values = tuple(self.get_padded_list(y_vals[keys[1]], len(x_values)))
        p1 = plt.bar(indices, chatter1_values, self.width, color='r')
        p2 = plt.bar(indices, chatter2_values, self.width, bottom=chatter1_values, color='b')
        max_messages = max(max(chatter1_values),max(chatter2_values))
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.xticks(indices, tuple(x_values))
        plt.yticks(np.arange(0, max_messages * 2, max_messages/20))
        plt.legend((p1[0], p2[0]), (keys[0], keys[1]))

        plt.show()

class NumberOfMessagesDayPlotter(StackedBarGraphPlotter):
    title = 'Number of Messages sent in a day'
    x_label = 'Date'
    y_label = 'Number of messages'

    def __init__(self, graph_data_creator):
        StackedBarGraphPlotter.__init__(self, graph_data_creator)
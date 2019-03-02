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
        indices = np.arange(0, len(x_values), 1)
        y_vals = self.graph_data_creator.get_y_dict()
        keys = y_vals.keys()
        chatter1_values = tuple(self.get_padded_list(y_vals[keys[0]], len(x_values)))
        chatter2_values = tuple(self.get_padded_list(y_vals[keys[1]], len(x_values)))

        fig = plt.figure()
        ax = fig.add_subplot(111)

        p1 = ax.bar(indices, chatter1_values, self.width, color='r')
        p2 = ax.bar(indices + self.width, chatter2_values, self.width, color='b')
        max_messages = max(max(chatter1_values),max(chatter2_values))
        ax.set_title(self.title)
        ax.set_ylabel(self.y_label)
        ax.set_xticks(indices + self.width)
        ax.set_xticklabels(tuple(x_values))
        ax.set_yticks(np.arange(0, max_messages, max_messages/20))
        ax.legend((p1[0], p2[0]), (keys[0], keys[1]))

        plt.show()

class NumberOfMessagesDayPlotter(StackedBarGraphPlotter):
    title = 'Number of Messages sent in a day'
    x_label = 'Date'
    y_label = 'Number of messages'

    def __init__(self, graph_data_creator):
        StackedBarGraphPlotter.__init__(self, graph_data_creator)

class NumberOfMessagesMonthPlotter(StackedBarGraphPlotter):
    title = 'Number of Messages sent in a month'
    x_label = 'Date'
    y_label = 'Number of messages'

    def __init__(self, graph_data_creator):
        StackedBarGraphPlotter.__init__(self, graph_data_creator)

class WhoInitiatedInAMonthPlotter(StackedBarGraphPlotter):
    title = 'Who initiated the conversation first, monthwise'
    x_label = 'Date'
    y_label = 'Number of times conversation was initiated'

    def __init__(self, graph_data_creator):
        StackedBarGraphPlotter.__init__(self, graph_data_creator)
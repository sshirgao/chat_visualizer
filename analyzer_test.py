from model import DayModel, MonthModel
from model import NumberOfMessagesChatParser, WhoInitiatedChatParser
from model import FileParser
import plotter

file_name = '/Users/shirsoha/Downloads/whatsapp_shalaka.txt'

file_parser = FileParser(file_name)
chat_parser = WhoInitiatedChatParser()
model = MonthModel(file_parser, chat_parser)

#print day_model.get_daily_model()

graph_data_creator = plotter.StackedBarGraphPlotterDataCreator(model)
number_of_messages_day_plotter = plotter.WhoInitiatedInAMonthPlotter(graph_data_creator)
number_of_messages_day_plotter.plot()



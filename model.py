# This file will contain all of the data types which will be used by the visualizer to create the graphs

import re
import collections

class FileParser:

    def __init__(self, file_name):
        self.file_name = file_name
        self.day_dict = collections.OrderedDict()
        self.parse()

    def parse(self):
        file = open(self.file_name, 'r')
        for line in file:
            self.create_day_dict_entry(line)

    def is_chat_line(self, line):
        pattern_string = '[0-9]+/[0-9]+/[0-9]+, [0-9]+:[0-9]+ .*'
        pattern = re.compile(pattern_string)
        return pattern.match(line) != None

    def create_day_dict_entry(self, line):
        if self.is_chat_line(line):
            line_split = line.split('-')
            date_time = line_split[0]
            chat = line_split[1]
            date_key = self.get_date_key_from_date_time(date_time)
            if date_key not in self.day_dict:
                self.day_dict[date_key] = []
            self.day_dict[date_key].append(chat)

    def get_date_key_from_date_time(self, date_time):
        return date_time.split(',')[0]

    def get_day_dict(self):
        return self.day_dict

class ChatParser:

    def get_colon_index(self, line):
        return line.find(':')

    def extract_chatter_name_from_chat(self, line):
        colon_index = self.get_colon_index(line)
        return line[:colon_index]

    def extract_chat_line_from_chat(self, line):
        colon_index = self.get_colon_index(line)
        return line[colon_index + 1:]

    def parse_chat(self, chat):
        pass

class NumberOfMessagesChatParser(ChatParser):

    def __init__(self):
        pass

    def get_number_of_messages_dict(self, chat):
        chat_dict = collections.OrderedDict()
        for chat_line in chat:
            chatter_name = self.extract_chatter_name_from_chat(chat_line)
            if chatter_name not in chat_dict:
                chat_dict[chatter_name] = 0
            chat_dict[chatter_name] += 1
        return chat_dict

    def parse_chat(self, chat):
        return self.get_number_of_messages_dict(chat)

class WhoInitiatedChatParser(ChatParser):

    def __init__(self):
        pass

    def get_who_initiated_dict(self, chat):
        chat_dict = collections.OrderedDict()
        chat_initiator = self.extract_chatter_name_from_chat(chat[0])
        for chat_line in chat:
            chatter_name = self.extract_chatter_name_from_chat(chat_line)
            if chatter_name == chat_initiator:
                chat_dict[chatter_name] = 1
            else:
                chat_dict[chatter_name] = 0
        return chat_dict

    def parse_chat(self, chat):
        return self.get_who_initiated_dict(chat)

class Model:

    def get_model_data(self):
        pass

class DayModel(Model):

    def __init__(self, file_parser, chat_parser):
        self.chat_parser = chat_parser
        self.file_parser = file_parser
        self.daily_model = collections.OrderedDict()
        self.create_daily_model()

    def create_daily_model(self):
        for day, chat in self.file_parser.get_day_dict().iteritems():
            self.daily_model[day] = self.chat_parser.parse_chat(chat)

    def get_daily_model(self):
        return self.daily_model

    def get_model_data(self):
        return self.get_daily_model()


class MonthModel(DayModel):

    def __init__(self, file_parser, chat_parser):
        DayModel.__init__(self, file_parser, chat_parser)
        self.monthly_model = self.create_monthly_model()

    def create_monthly_model(self):
        keys = self.get_daily_model().keys()
        monthly_map = collections.OrderedDict()
        for key in keys:
            month_key = self.get_month_from_key(key)
            if month_key not in monthly_map:
                monthly_map[month_key] = {}
            for chatter in self.get_daily_model()[key]:
                if chatter not in monthly_map[month_key]:
                    monthly_map[month_key][chatter] = 0
                monthly_map[month_key][chatter] += self.get_daily_model()[key][chatter]
        return monthly_map

    def get_month_from_key(self, key):
        split_key = key.split('/')
        return split_key[0] + '/' + split_key[2]

    def get_model_data(self):
        return self.monthly_model


class YearModel(MonthModel):
    pass


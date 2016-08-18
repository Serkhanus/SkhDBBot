import logging

"""
$ python3.5 commandParser.py.py

CommandParser class, dictionaries and helpers

"""


class CommandParser:
    responds = {'Hi': 'Hi to you',
                'Bye': 'Goodbye, have a good time'}

    def __init__(self):
        logging.debug(self.responds['Hi'])

    def commandProcessor(self, request):
        return 'Command \n' + request + '\ncompleted'

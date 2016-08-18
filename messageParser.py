import logging

"""
$ python3.5 messageParser.py

MessageParser class, dictionaries and helpers.

Remember to `/setinline` and `/setinlinefeedback` to enable inline mode for your bot.



"""


class MessageParser:
    responds = {'Hi': 'Hi to you',
                'Bye': 'Goodbye, have a good time'}

    def __init__(self):
        logging.debug(self.responds['Hi'])

    def messageProcessor(self, request):
        return 'You told ' + request

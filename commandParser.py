import logging

"""
$ python3.5 commandParser.py.py

CommandParser class, dictionaries and helpers

Structure of commands:
 - 1st level command - command section - ex. config
 --- 2nd level command (to be followed by parameters) ex. set var1 = 12345
 --- parameters to be presented in form 'variable_name = value'

Note1: 1st level command + 2nd level command + parameters could be entered as single line in case of started with (commandProc to use final='yes' that is default)
Note2: command could be entered as multiline. Then:
 - first line to contain just 1st level command
 - every next line to contain on 2nd level command with parameter
 - 2nd level command with commapdProc call and set final to 'yes' treated as a last command in the sequense - so command mode closed

"""


class CommandParser:
    responds = {'Hi': 'Hi to you',
                'Bye': 'Goodbye, have a good time'}
    commandMode = None
    commands = [
        {
            'config': 1,
            'reset': 2,
            'talk': 3
        },
        {
            'config': None
        },
        {
            'reset': None
        },
        {
            'talk': None
        }
    ]
    response = {
        'message': None,
        'status': None,
        'command': None,
        'action': None,
        'flag': None
    }

    def __init__(self):
        logging.debug(self.responds['Hi'])
        self.commands[1]['config'] = self.configProc
        self.commands[2]['reset'] = self.resetProc
        self.commands[3]['talk'] = self.talkProc


    def commandProcessor(self, request):
        respond = ''
        ret = None
        logging.debug('Request is: ' + request)
        try:
            ret = self.commands[0][request]
            logging.debug('Key is: ' + str(ret))
            self.response['message'] = self.commands[ret][request](request)['message']
        except KeyError as ex:
            logging.debug(ex)
            self.response['message'] = 'Command unknown'

        logging.debug('Respond is: ' + self.response['message'])

        return self.response

    def configProc(self, request, final='yes'):
        self.response['message'] = 'Config executed'

        if final == 'yes':
            self.response['command'] = None
            self.response['status'] = None
            self.response['action'] = None
            self.response['flag'] = 'Done'
        else:
            self.response['command'] = 'config'
            self.response['status'] = 'command'
            self.response['action'] = None
            self.response['flag'] = None
        return self.response

    def resetProc(self, request, final='yes'):
        self.response['message'] = 'Reset executed'
        if final == 'yes':
            self.response['command'] = None
            self.response['status'] = None
            self.response['action'] = None
            self.response['flag'] = 'Done'
        else:
            self.response['command'] = 'reset'
            self.response['status'] = 'command'
            self.response['action'] = None
            self.response['flag'] = None
        return self.response

    def talkProc(self, request, final='yes'):
        self.response['message'] = 'Talking now'
        if final == 'yes':
            self.response['command'] = None
            self.response['status'] = None
            self.response['action'] = None
            self.response['flag'] = 'Done'
        else:
            self.response['command'] = 'talk'
            self.response['status'] = 'command'
            self.response['action'] = None
            self.response['flag'] = None
        return self.response

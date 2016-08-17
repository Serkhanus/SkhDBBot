import asyncio
import logging

import telepot
import telepot.aio

"""
$ python3.5 SkhDBBot.py <token>

Integration between Telegram Bot and neo4J DB access quesries.

Remember to `/setinline` and `/setinlinefeedback` to enable inline mode for your bot.

It works like this:
- All strings passed to skh pacjage for parsing and processing. responses sent back to user chat
- Initial communication starts with session authorization. Token to be provided as a command
- Special mode is accessed by sending '!' simbol as the first symbol in command
- Command mode is closed by sending '#' simbol as the last simbol in line
- for multi line commands bot sends chat messages with the corresponding prefix:
    - 'LangDB'
    - 'Config'
    - 'Learn'

"""
class SkhDBBot:
    modes = [{"Normal": 0}, {"LangDB": 1}, {"Config": 2}, {"Learn": 3}]
    message_with_inline_keyboard = None
    command_Status = None
    command_cont = []
    command_mode = 'Normal'

    def __init__(self):
        command_mode='Normal'
        logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        logging.info('Chat:' + content_type + ' '+ chat_type+ ' ' + str(chat_id))

        if content_type != 'text':
            return
        command = msg['text'][0]
        if self.command_Status=='Command' and msg['text'][0] == '!':
            logging.debug('Chat: ' + str(chat_id) + ' !!!! Already in Command Mode !!!!')
            await bot.sendMessage(chat_id, 'Already in Command Mode - Input rejected')
        elif msg['text'][0] == '!' and msg['text'][-1] == '#' and self.command_Status==None:
            if len(msg['text'])>2:
                respond = self.parseCommand(msg['text'][1:-1])
                logging.debug('Chat: '+ str(chat_id)+ ' message is: '+ msg['text'])
                logging.debug('Chat: ' + str(chat_id) + ' **** Command Received ****')
                logging.debug('Chat: ' + str(chat_id) + ' **** Command Mode: ' + self.command_mode)
                await bot.sendMessage(chat_id, respond)
                self.command_Status=None
                logging.debug('Chat: ' + str(chat_id) + ' **** Command Executed ****')
            else:
                logging.debug('Chat: ' + str(chat_id) + ' !!!! No command received - nothing done !!!!')
                await bot.sendMessage(chat_id, 'No command received - nothing done')
        elif msg['text'][0] == '!' and self.command_Status==None:
            respond='*'
            if len(msg['text'])>1:
                respond = self.parseCommand(msg['text'][1:])
                logging.debug('Chat: ' + str(chat_id) + ' **** Command Received ****')
                logging.debug('Chat: ' + str(chat_id) + ' **** Command Mode: ' + self.command_mode)
            await bot.sendMessage(chat_id, respond)
            self.command_Status='Command'
            logging.debug('Chat: ' + str(chat_id) + ' **** Command Status : ' + self.command_Status)
            await bot.sendMessage(chat_id, 'Command started')
        elif self.command_Status == 'Command' and msg['text'][-1:] == '#':
            respond='*'
            if len(msg['text'])>1:
                respond = self.parseCommand(msg['text'][0:-1])
                logging.debug('Chat: ' + str(chat_id) + ' **** Command Received ****')
                logging.debug('Chat: ' + str(chat_id) + ' **** Command Mode: ' + self.command_mode)
                logging.debug('Chat: ' + str(chat_id) + ' **** Command Status : ' + self.command_Status)
            self.command_Status=None
            await bot.sendMessage(chat_id, respond)
            logging.debug('Chat: ' + str(chat_id) + ' **** Command Executed ****')
        elif self.command_Status == 'Command':
            respond = self.parseCommand(msg['text'])
            await bot.sendMessage(chat_id, 'Command input in progress')
            logging.debug('Chat: ' + str(chat_id) + ' **** Command Mode: ' + self.command_mode)
            logging.debug('Chat: ' + str(chat_id) + ' **** Command Status : ' + self.command_Status)
            await bot.sendMessage(chat_id, respond)
        elif msg['text'][-1:] == '#':
            logging.debug('Chat: ' + str(chat_id) + ' !!!! Command not started - input rejected !!!!')
            await bot.sendMessage(chat_id, 'Command not started - input rejected')
            logging.debug('Chat: ' + str(chat_id) + ' **** Command Mode: ' + self.command_mode)
        else:
            respond = self.parseMessage(msg['text'])
            logging.debug('Chat: ' + str(chat_id) + ' **** Message Received ****')
            logging.debug('Chat: ' + str(chat_id) + ' **** Command Mode: ' + self.command_mode)
            await bot.sendMessage(chat_id, respond)


    def on_edited_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg, flavor='edited_chat')
        print('Edited chat:', content_type, chat_type, chat_id)


    async def on_callback_query(self, msg):
        query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
        print('Callback query:', query_id, from_id, data)

        if data == 'notification':
            await bot.answerCallbackQuery(query_id, text='Notification at top of screen')
        elif data == 'alert':
            await bot.answerCallbackQuery(query_id, text='Alert!', show_alert=True)
        elif data == 'edit':
            global message_with_inline_keyboard

            if message_with_inline_keyboard:
                msg_idf = telepot.message_identifier(message_with_inline_keyboard)
                await bot.editMessageText(msg_idf, 'NEW MESSAGE HERE!!!!!')
            else:
                await bot.answerCallbackQuery(query_id, text='No previous message to edit')

    def parseCommand(self, msg):
        if msg == None:
            return "***"
        return 'Respond to Command: '+msg



    def parseMessage(self, msg):
        if msg == None:
            return "***"
        return 'Respond to message: '+msg

#TOKEN = sys.argv[1]  # get token from command-line


TOKEN = "xxx"

bot = telepot.aio.Bot(TOKEN)
answerer = telepot.aio.helper.Answerer(bot)
skh_bot=SkhDBBot()
loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop({'chat': skh_bot.on_chat_message,
                                   'edited_chat': skh_bot.on_edited_chat_message,
                                   'callback_query': skh_bot.on_callback_query}))
print('Listening ...')

loop.run_forever()

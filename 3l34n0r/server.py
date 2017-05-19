from telegram import Telegram

from modules.chat import eliza
from modules.start import start
from modules.calendar import today

def run_command(command, args = []):
    return command(*args)

def callback(bot, message, chat_id):
    case = message.split()[0]

    print(case)
    
    if   case == '/start' : func = start
    elif case == '/today' : func = today
    else                  : func = eliza

    response = run_command(func, [bot, message, chat_id])
    bot.sendMessage(chat_id, response)

# -- main --
if __name__ == '__main__':
    token = open("/Users/chiayo/.3l34n0r-token.txt", 'r').readline()[:-1]
    Telegram(token).listen(callback)

from api.pytelegram.telegram import *

from modules.greet import *
from modules.eliza import *
from modules.today import *
from modules.email import mail

def run_command(command, args = []):
    return command(*args)

def callback(bot, message, chat_id):
    case = message.split()[0]

    print(case)
    
    if   case == '/greet' : func = greet
    elif case == '/today' : func = today
    elif case == '/email' : func = mail.send
    else                  : func = eliza

    response = run_command(func, [bot, message, chat_id])
    bot.sendMessage(chat_id, response)

# -- main --
if __name__ == '__main__':
    token = ''
    Telegram(token).listen(callback)

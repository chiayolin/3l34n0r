from nltk.chat.util import Chat, reflections
from nltk.chat.eliza import pairs

def eliza(bot, message, chat_id):
    return Chat(pairs, reflections).respond(message)

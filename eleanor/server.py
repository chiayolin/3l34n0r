#!/usr/bin/env python3
#
# This file is part of 3l34n0r (Eleanor - A bot)
#
# Copyright (C) 2017 Chiayo Lin <chiayo.lin@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The server for 3l34n0r bot"""

from config import *

import sys, signal, logging

from eleanor.telegram import Telegram
from eleanor.modules.chat import eliza
from eleanor.modules.start import start
from eleanor.modules.calendar import today

def _apply(func, args = []):
    """Apply a function to some arguments, port of apply() from Python2.

    Args:
        func: a function object
        args: a list of arguments
    
    Returns:
        It returns whatever the func object returned.
    """
    
    return func(*args)

def callback(bot, message, chat_id):
    """Invokes by the Telegram interface during each poll."""

    case = message.split()[0] # Get the first part of a message
    
    # Run a command otherwise start a chat
    if   case == '/start' : func = start
    elif case == '/today' : func = today
    else                  : func = eliza

    response = _apply(func, [bot, message, chat_id])
    bot.sendMessage(chat_id, response)

def sigterm_handler(signal, frame):
    logging.getLogger(__name__).info("SIGTERM received, terminating...")
    sys.exit(0)

# -- main --
if __name__ == '__main__':
    # Register the handler so the process knows to handle SITGTERM
    signal.signal(signal.SIGTERM, sigterm_handler)

    # Get Telegram token and start polling
    token = open(TELEGRAM_TOKEN_PATH, 'r').read()[:-1]
    Telegram(token).listen(callback)

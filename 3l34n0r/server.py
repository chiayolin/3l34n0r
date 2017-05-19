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

from telegram import Telegram
from modules.chat import eliza
from modules.start import start
from modules.calendar import today

TELEGRAM_TOKEN_PATH = '/Users/chiayo/.3l34n0r-token.txt'

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
    token = open(TELEGRAM_TOKEN_PATH, 'r').read()[:-1]
    Telegram(token).listen(callback)
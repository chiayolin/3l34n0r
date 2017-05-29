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

"""Minimalistic Telegram Python interface"""

import requests
import logging

class Telegram:

    def __init__(self, token):
        self.token = token
        self.logger = logging.getLogger(__name__)
    
    def __telegram(self, token, method, payload = {}):
        return requests.get('https://api.telegram.org/bot' + \
                self.token + method, params = payload).json()
    
    def getMe(self):
        return self.__telegram(self.token, '/getMe')

    def getUpdates(self, offset, timeout = 60):
        return self.__telegram(self.token, '/getUpdates',
                {'timeout' : timeout, 'offset' : offset})
        
    def sendMessage(self, recipient, message, parse_mode = 'HTML'):
        self.logger.info('sent: ' + message)

        return self.__telegram(self.token, '/sendMessage', 
                {'chat_id' : recipient, 'text' : message, 
                    'parse_mode' : parse_mode})

    def listen(self, callback, parse_mode = 'HTML', offset = 0):
        while True:
            request = self.getUpdates(offset)
            if not (request['ok'] and request['result']): continue
           
            for result in request['result']:
                if 'message' not in result: 
                    continue
                
                message = result['message']['text'] 
                chat_id = result['message']['chat']['id']

                self.logger.info('received: ' + message)
                callback(self, message, chat_id)

                offset = result['update_id'] + 1

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

from eleanor.oauth2 import *
from eleanor.config import *
from eleanor.context import Context

import logging
import smtplib
import csv

"""Send an email using Google's SMTP server"""

logger = logging.getLogger(__name__)

gmail_user = SMTP_USERNAME
gmail_password = open(SMTP_PASSWORD_PATH, 'r').read()[:-1]

def _get_meta(chat_id):
    # Here we assume that the exact location of each field is known
    c = Context(CONTEXT_FILE).read(chat_id)[1:]
    return dict([*map(lambda x: [c[x], c[x + 1]], range(0, 6, 2))])

def gmail(bot, message, chat_id):
    # Get current context
    context = Context(CONTEXT_FILE).read(chat_id)

    # Start here since context is not 'gmail'
    if not context or context[0] != 'gmail':
        Context(CONTEXT_FILE).write(chat_id, ['gmail', 'to'])

        # Prompt user to enter email address to be sent
        return "Email? Old school.. To whom shall I send it?"

    # Get 'send to' address
    elif context[-1] == 'to':
        Context(CONTEXT_FILE).write(chat_id, context + [message, 'subject'])

        # Prompt user to enter the subject
        return "What's the subject of your email?"

    # Get the subject of this email
    elif context[-1] == 'subject':
        Context(CONTEXT_FILE).write(chat_id, context + [message, 'body'])

        # Prompt user to enter the body
        return "Cool! What would you like the email to say?"

    # Get the body of this email
    elif context[-1] == 'body':
        Context(CONTEXT_FILE).write(chat_id, context + [message, 'end'])

        meta = _get_meta(chat_id)
        _resp  = meta['subject'] + '\n----------\n' + meta['body']
        bot.sendMessage(chat_id, "Okay. Here are your messages to " +
            meta['to'] + ":")

        bot.sendMessage(chat_id, _resp)

        # Promptuser for confirmation
        return "Would you like me to send it? (yes/no)"

    # Finally send the email depending on user's choice
    elif context[-1] == 'end':
        flag = message.lower()[0] == 'y'

    meta = _get_meta(chat_id)
    Context(CONTEXT_FILE).write(chat_id, []) # reset the context

    # Send the mail
    if flag:
        # Try and let it fail if something went wrong
        try:
            logger.info('Establishing SMTP server connection')
            server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server_ssl.ehlo()
            logger.info('Logging in..')
            server_ssl.login(gmail_user, gmail_password)

            send_to   = meta['to']
            sent_from = gmail_user

            # Apeend subject to the email header
            text = 'Subject: {}\n\n{}'.format(meta['subject'], meta['body'])

            server_ssl.sendmail(sent_from, send_to, text)
            server_ssl.close()

            logger.info('Email sent: ' + str(meta))

        except:
            logger.error('The email could not be sent.')
            return "I couldn't send your email, sorry."

    return flag and "Alright. I've sent the email!" or \
        "Okay. Your mail is not sent."

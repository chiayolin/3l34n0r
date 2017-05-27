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

import os, csv, time, logging

class Context:
    """
    This class provides a mechanism to keep track of the context of the
    current conversation with the user. For example, if the user asked
    the bot to send an email, it may be logical for the bot to prompt the
    use to enter more information such as the title, body, and to whom
    the email is sent to. However, because the callback during polling is
    invoked every time an update is received, no states are saved. In other
    words, each poll is a new session and this class enables the bot to
    "remember" the context of the previous session/poll.

    An instance of this calss can be created with the following syntax:

        context = Context(csv_file_path)

    Where csv_file_path is the path to a csv file -- A new file named
    context.csv will be created if no arguments were given.

    The write() methold will write the current context in the csv file as:

        chat_id,context

    The chat_id is an unique ID for the user we are currently having a con-
    versation with. The context is a string and can bascially be anything
    depending on the implementation of the module that needs the context.
    Futhermore, if the context for a given chat_id will be over-written if
    a context was already being recorded.

    The read() method simply returns the current context of a given chat_id.
    If the given chat_id is not found or has not context, '' is returned.
    An empty string is retunred because the split method is usually used to
    parse the context and return other types would require the user to write
    addtional test statements.
    """

    def __init__(self, csv_file_path = 'context.csv'):
        self.context_file = csv_file_path
        self.logger = logging.getLogger(__name__)

    def write(self, chat_id, context):
        # Open a file to read and write
        with open(self.context_file, 'w+', newline = '') as _file:
            # Read the file
            reader = list(csv.reader(_file))

            # Check if chat_id existed in the file already
            chat_id_existed = index = 0
            while index != len(reader):
                chat_id_existed = reader[index][0] is chat_id
                index += 1

            # Replace the context if chat_id existed else append it
            if chat_id_existed:
                reader[index][1] += [context]
                self.logger.info('chat_id_existed: ' + str(reader[index][1]))
            else:
                self.logger.info(str([chat_id] + [context]))
                reader.append([str(chat_id)] + context)

            # write the new result back into the file
            writer = csv.writer(_file, delimiter=',')
            for line in reader:
                writer.writerow(line)

        return

    def read(self, chat_id):
        with open(self.context_file, 'r') as _file:
            reader = list(csv.reader(_file))

            if not reader or not reader[0]:
                self.logger.warn('chat_id not found')
                return []

            for line in reader:
                if line[0] == str(chat_id):
                    return line[1:]

        self.logger.warn('chat_id not found')
        return []

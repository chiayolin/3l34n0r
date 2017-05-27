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
    
    Where csv_file_path is the path of a csv file -- A new file named 
    'context' post-fixed with a timestamp and '.csv' extension is created 
    in the current directory if no arguments were given. Note that the file 
    is post-fixed with an Unix timestamp in order to avoid duplications.
    
    The write() methold will write the current context in the csv file as:

        chat_id,context

    The chat_id is an unique ID for the user we are currently having a con-
    versation with. The context is a string and can bascially be anything
    depending on the implementation of the module that needs the context.
    Futhermore, if the context for a given chat_id will be over-written if
    a context was already being recorded.

    The read() method simply returns the current context of a given chat_id.
    If the given chat_id is not found or has not context, False is returned.
    """
    
    def __init__(self, csv_file_path = 'context.csv'):
        name, extension = os.path.splitext(csv_file_path)
        self.context_file = name + str(int(time.time())) + extension

    def write(self, chat_id, context):
        # Open a file to read and write
        with open(self.csv_file_path, 'rw', newline = '') as _file:
            # Read the file
            reader = csv.reader(_file)
            
            # Check if chat_id existed in the file already
            chat_id_existed = index = 0
            while index != len(reader):
                chat_id_existed = reader[index][0] is chat_id
                index += 1
            
            # Replace the context if chat_id existed else append it
            if chat_id_existed:
                reader[index][1] = context
            else:
                reader += [[chat_id, context]]
            
            # write the new result back into the file
            writer = csv.writer(_file, delimiter=',')
            for line in reader:
                writer.writerow(line)

        return

    def read(self, chat_id):
        # Read every line and return context of a chat_id if found
        with open(self.csv_file_path, 'r') as _file:
            for line in csv.reader(_file):
                if line[0] is chat_id: 
                    return line[1]
        
        # Otherwise return False
        return False

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

import os, sys, logging

"""Path configuration"""

# We know this file is at 3l34n0r/eleanor/config.py
this_path = os.path.abspath(__file__)

# Walk up 2 directories to 3l34n0r
eleanor_path = os.path.dirname(os.path.dirname(this_path))

# Insert path so we can import with eleanor.package at every level
sys.path.insert(0, eleanor_path)

"""Logging configuration"""

logging_format = '%(levelname)s::%(asctime)s::%(name)s::%(message)s'
logging_level = logging.INFO
logging_file = '/tmp/eleanor.log'

# set global logging config
logging.basicConfig(format = logging_format, level = logging_level,
    filename = logging_file)

# disable log messages from the Requests library
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

"""Globals variables"""

HOME = os.path.expanduser("~")
CONTEXT_FILE = HOME + '/.3l34n0r/context.csv'

# Telegram token file path
TELEGRAM_TOKEN_PATH = HOME + '/.3l34n0r/telegram_token.txt'

# SMTP configuration
## Yep PLAINTEXT password and is not secure at all!
SMTP_PASSWORD_PATH = HOME + '/.3l34n0r/ssis_password.txt'
SMTP_USERNAME = 'chlin18@ssis.edu.vn'

# Google Calendar
## If modifying these scopes, delete your previously credentials
## at ~/.credentials/<GCAL_APPLICATION_NAME>.json
GCAL_SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
GCAL_CLIENT_SECRET_FILE = HOME + '/.3l34n0r/client_secret.json'
GCAL_APPLICATION_NAME = '3l34n0r-calendar'

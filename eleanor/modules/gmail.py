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

import logging
import smtplib

if CONTEXT is "gmail":
    print("hello, world")

def gmail():
    gmail_user = ''  
    gmail_password = ''

    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()
    server_ssl.login(gmail_user, gmail_password)

    sent_from = gmail_user
    to = ['chiayo.lin@gmail.com']  
    subject = 'hello, world'  
    body = "This is a test email"

    server_ssl.sendmail(sent_from, to, body)
    server_ssl.close()

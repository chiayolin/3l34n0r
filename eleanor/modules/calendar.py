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

from __future__ import print_function
import httplib2
import os

from apiclient import discovery

from datetime import datetime
from datetime import timedelta

from eleanor.oauth2 import *

def _get_upcoming():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(1)
    
    print('Getting today\'s events')
    eventsResult = service.events().list(
        calendarId='primary', 
        singleEvents=True, 
        orderBy='startTime',
        timeMin=start.isoformat() + '+07:00', 
        timeMax=end.isoformat() + '+07:00').execute()
    
    response = ''
    events = eventsResult.get('items', [])
    if not events:
        response = 'No upcoming events found.'
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            response = response + '• ' + event['summary'] + '\n'

    return response

def today(bot, message, chat_id):
    bot.sendMessage(chat_id, 'Reading your calendar...')
    response = _get_upcoming()
    bot.sendMessage(chat_id, 'Here are the events for today:')

    return response

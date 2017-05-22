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

import httplib2

from eleanor.oauth2 import *
from eleanor.config import *

from datetime import datetime
from datetime import timedelta

from apiclient import discovery

def _get_todays_events():
    """Get today's events from Google Calendar"""
    
    credentials = get_credentials(
        GCAL_APPLICATION_NAME,
        GCAL_CLIENT_SECRET_FILE,
        GCAL_SCOPES)
    
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day) + timedelta(hours = 7)
    end = start + timedelta(1)

    logging.getLogger(__name__).info('Getting today\'s event...')
    eventsResult = service.events().list(
        calendarId   ='primary', 
        singleEvents = True, 
        orderBy      = 'startTime',
        timeMin      = start.isoformat() + 'Z', 
        timeMax      = end.isoformat()   + 'Z').execute()
    
    logging.getLogger(__name__).info(eventsResult)
    events = eventsResult.get('items', [])
    response = ''

    if not events:
        response = 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        response = response + '• ' + event['summary'] + '\n'
    
    logging.getLogger(__name__).info(response)

    return response

def today(bot, message, chat_id):
    bot.sendMessage(chat_id, 'Reading your calendar...')
    response = _get_todays_events()
    bot.sendMessage(chat_id, 'Here are the events for today:')

    return response

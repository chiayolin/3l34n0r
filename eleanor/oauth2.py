#!/usr/bin/env python3
#
# This file is part of 3l34n0r (Eleanor - A bot)
#
# Original License:
# -----------------
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, logging, argparse

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def get_credentials(app_name, secret_file, scopes):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    logger = logging.getLogger(__name__)
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        logger.warn('Credential dir not found, creating ' + credential_dir)
        os.makedirs(credential_dir)
    
    credential_path = os.path.join(credential_dir, app_name + '.json')
    store = Storage(credential_path)
    credentials = store.get()

    logger.info(credentials)
    
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(secret_file, scopes)
        flow.user_agent = app_name
        
        credentials = tools.run_flow(flow, store, flags)
        
        logger.info('Storing credentials to ' + credential_path)
    
    return credentials

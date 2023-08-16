"""
File       : WebTools.py
Author     : Hasan Ozturk <haozturk AT cern dot com>
Description: Class which contains helper functions for web interaction
"""

import os
import http.client
import json
from workflow.utils.Configuration import Configuration
import logging

# Get necessary parameters
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SC = Configuration( os.path.join( BASE_DIR , 'workflow' , 'conf' , 'serviceConfiguration.json' ))
reqmgr_url = os.getenv('REQMGR_URL', SC.get('reqmgr_url'))

def getX509Conn(url=reqmgr_url,max_try=5):
    tries = 0
    logging.info( os.getenv('X509_USER_PROXY') )
    while tries<max_try:
        try:
            conn = http.client.HTTPSConnection(url, cert_file = os.getenv('X509_USER_PROXY'), key_file = os.getenv('X509_USER_PROXY'))
            return conn
        except:
            tries+=1
            pass
    return None

def getResponse(url, endpoint, param='', headers=None):

    if headers == None:
        headers = {"Accept":"application/json"}

    if type(param)==dict:
        _param = '&'.join( [ "=".join([k,v]) for k,v in param.items()] )
        param = '?' + _param

    try:
        conn = getX509Conn(url)
        request= conn.request("GET",endpoint+param,headers=headers)
        response=conn.getresponse()
        data = json.loads(response.read())
        return data
    except Exception as e:
        print("Failed to get response from %s" % url+endpoint+param)
        print(str(e))

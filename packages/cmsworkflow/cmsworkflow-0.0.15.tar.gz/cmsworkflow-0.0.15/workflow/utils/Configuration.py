
"""
File       : SearchTools.py
Author     : Hasan Ozturk <haozturk AT cern dot com>
Description: Class for Unified configuration
"""

import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
class Configuration:
    def __init__(self, configFile=os.path.join( BASE_DIR,'workflow' , 'conf' , 'serviceConfiguration.json')):
        self.configFile = configFile
        if self.configFile is None:
            self.configs = self.configFile
        else:
            try:
                self.configs = json.loads(open(self.configFile).read())
            except Exception as ex:
                print(("Could not read configuration file: %s\nException: %s" %
                      (self.configFile, str(ex))))
                sys.exit(124)

    def get(self, parameter):
        if self.configs:
            if parameter in self.configs:
                return self.configs[parameter]['value']
            else:
                print(parameter, 'is not defined in global configuration')
                print(','.join(list(self.configs.keys())), 'possible')
                sys.exit(124)

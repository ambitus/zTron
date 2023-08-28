"""
  config.py - the zTron Config class.  Configurations contain the essential
              parameters for a pipeline of tasks.

  Author: Joe Bostian

  Copyright Contributors to the Ambitus Project.

  SPDX-License-Identifier: Apache-2.0
"""
import os, yaml

class Config:
    def __init__(self, arg_config, arg_llvl):
        self.file_name = arg_config
        self.log = None
        self.cfg = {}
        self.env = os.environ.copy()

        self.read()
        self.build_env()
        return

    def cleanup(self):
        return

    # File operations
    def read(self):
        if self.file_name != None:
            with open(self.file_name) as f:
                cfg_list = yaml.safe_load(f)

            # Only deal with keys in lower case.  Preserve the case of the values.
            d = {}
            for k in cfg_list:
                d[k.upper()] = cfg_list[k]
                self.cfg.update(d)
        return

    # Build a runtime environment for running the pipeline.
    def build_env(self):
        for k,v in self.cfg.items():
            if k != 'name':
                self.env[k] = v
        return

    # Getters
    def get_desc_name(self):
        if 'NAME' in self.cfg:
            return self.cfg['NAME']
        else:
            return None

    def get_file_name(self):
        return self.file_name

    def get_env(self):
        return self.env

    def get_log_path(self):
        if 'LOGS' in self.cfg:
            return self.cfg['LOGS']
        else:
            return None

    def get_log_level(self):
        # This default needs to be one of the log levels defined in the Log class.
        if 'LOG_LVL' in self.cfg:
            return self.cfg['LOG_LVL']
        else:
            return 'warn'

    def get_cfg_setting(self,setting):
        if setting in self.cfg:
            return self.cfg[setting]
        else:
            return None

    # Setters
    def set_log(self,log):
        self.log = log

    # Show ourselves
    def show(self):
        if 'NAME' in self.cfg:
            desc_name = self.cfg['NAME']
        else:
            desc_name = ''

        self.log.log('info','-- Config (%s) -------------------------',(desc_name))
        self.log.log('info','     file name: %s',(self.file_name))
        for k,v in self.cfg.items():
            if k != 'name':
                self.log.log('info','     %s: %s',(k,v))
        return

"""
  ztron.py - the main ztron workbook class

  Author: Joe Bostian

  Copyright Contributors to the Ambitus Project.

  SPDX-License-Identifier: Apache-2.0
"""
import os, time
from datetime import datetime

# from ztron.workbook import Workbook
from ztron.config import Config
from ztron.log import Log

# Log method wrappers for easy access.  These are for application use - you won't
# be able to import them from internal ztron code.
def log_info(mcp,fmt,args=None):
    mcp.log.log('info',fmt,args)
def log_warn(mcp,fmt,args=None):
    mcp.log.log('warn',fmt,args)
def log_err(mcp,fmt,args=None):
    mcp.log.log('err',fmt,args)
def log_trc(mcp,fmt,args=None):
    mcp.log.log('trace',fmt,args)

class Mcp:
    # If no workbook and configuration is provided, it can be specified
    # interactively.
    def __init__(self,args=None):
        self.workbooks = []
        self.spool = {}
        self.cfg = None
        self.log = None
        self.workbook = None
        self.start_time = time.time()

        if (args != None) & (len(args) >= 4):
            # Bootstrap situation between config and log ...
            self.cfg = Config(args[2], args[3])
            self.log = Log('ztrun',
                           self.cfg.get_log_path(),
                           self.cfg.get_log_level())
            self.cfg.set_log(self.log)

            self.workbook = Workbook(self.log,args[1],self.cfg.get_env())
            self.workbook.build_pipeline()

            self.show_env()
        else:
            # Log is not available
            print('Error - args must be provided for workbook, config, and log level')
            raise Exception

    def run(self):
        self.workbook.run()

    def getenv(self,env_var):
        try:
            return os.environ[env_var]
        # Swallow any exceptions because of missing env variable names.
        except:
            return ''

    def show_env(self):
        self.log.log('info','zTron Workbook cyborg',None)
        now = datetime.now()
        self.log.log('info','  Workbook name: %s',(self.workbook.get_desc_name()))
        self.log.log('info','      %s',(self.workbook.get_file_name()))
        self.log.log('info','  Configuration name: %s',(self.cfg.get_desc_name()))
        self.log.log('info','      %s',(self.cfg.get_file_name()))
        self.log.log('info','  Date, time: %s',(now.strftime("%d/%m/%Y, %H:%M:%S")))
        self.log.log('info','  Current working dir: %s',(self.getenv('PWD')))
        self.log.log('info','  Userid: %s',(self.getenv('USERNAME')))
        self.log.log('info','  Shell: %s',(self.getenv('SHELL')))
        self.log.log('info','\nReady to run workbook\n',None)

    def show(self):
        self.log.log('info','\nMCP:',None)
        self.cfg.show()
        self.workbook.show()
        self.log.show()
        self.log.log('info','\n',None)

    def finish(self):
        # Tell the user where their results are, and how long the pipeling took
        # to process.
        self.log.log('info','Finishing up: %s',(self.workbook.get_desc_name()))
        self.log.log('info','  Complete results logged in: %s',(self.log.get_full_path()))

        # Show the results of each task executed:
        self.workbook.show_results()
        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time()-self.start_time))
        self.log.log('info','  Total elapsed time: %s',(elapsed_time))

        # If run from a notebook, copy it to the log for this instance.

        self.workbook.cleanup()
        self.cfg.cleanup()
        self.log.cleanup()

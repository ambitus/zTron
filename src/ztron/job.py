"""
  job.py - all resources associated with a zTron job

  Author: Joe Bostian

  Copyright Contributors to the Ambitus Project.

  SPDX-License-Identifier: Apache-2.0
"""
import os
import subprocess
import time
import argparse
import yaml
import pprint as pp
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


class Job():
    '''
    '''
    def __init__(self, argc=0, argv=None):
        self.job_desc_fn = ''
        self.name = ''
        self.desc = ''
        self.env_userid = ''
        self.env_home = ''
        self.env_home_logs_path = ''
        self.env_home_spool_path = ''
        self.env_log_lvl = ''
        self.appl_name = ''
        self.appl_args = {}

        self.log = None
        self.ts_start = None

        # Get all input from the command line and job descriptor.
        self.job_desc = self.get_job_desc(argc, argv)

        # Build the job from the specified input.
        self.job_desc_fn = self.job_desc['filename']
        self.name = self.job_desc['name']
        self.desc = self.job_desc['description']
        self.pgm = self.job_desc['program']
        self.env_userid = self.job_desc['environment']['userid']
        self.env_home = self.job_desc['environment']['home']['root']
        self.env_home_logs_path = self.env_home+'/'+self.job_desc['environment']['home']['logs']
        self.env_home_spool_path = self.env_home+'/'+self.job_desc['environment']['home']['spool']
        self.env_log_lvl = self.job_desc['environment']['log_lvl']
        self.appl_name = self.job_desc['application']['name']
        self.appl_args = self.job_desc['application']['args']
        self.log = Log('ztron.log', self.env_home_logs_path, self.env_log_lvl)
        self.print()
        return

    def run(self):
        print(('--- Running %s ...' % (self.name)))
        os.environ['PATH'] += ':' + self.env_home
        subprocess.run(['python', self.env_home+'/'+self.pgm], shell=False)
        return

    def finish(self):
        print(('--- Clean up from %s ...' % (self.name)))
        return

    def get_job_desc(self, argc, argv):
        """
        Input can be provided from the command line or in the job descriptor.  Parse 
        the command line to get the name of the job descriptor file, acquire settings 
        from there, and then override settings with command line settings where specified.
        Return the merged settings in an input dictionary for later use.
        """
        ap = argparse.ArgumentParser('Run a series of tasks and manage the output')
        ap.add_argument('--job', default=self.job_desc_fn)
        ap.add_argument('--userid', default=self.env_userid)
        ap.add_argument('--log_lvl', default=self.env_log_lvl)
        cli_args = ap.parse_args().__dict__
        print('--- cli args: ')
        pp.pprint(cli_args)

        if 'job' not in cli_args.keys():
            log_err('No job descriptor specified.')
            raise Exception

        # Load the job descriptor file with environment settings and application 
        # arguments.
        print('--- job descriptor name: %s' % (cli_args['job']))
        with open(cli_args['job'], 'r') as file:
            try:
                job_yml_dict = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(e)
                return None
        
        job_desc = {}
        job_desc['filename'] = cli_args['job']

        # Lower the case of all keys to be case invariant.
        for key in job_yml_dict.keys():
            job_desc[key.lower()] = job_yml_dict[key]

        # Handle the environment and application sections of the descriptor.
        job_desc.update(environment=self.get_jd_env(job_desc, cli_args))
        job_desc.update(application=self.get_jd_appl(job_desc)) 

        print('--- job descriptor after merge:')
        pp.pprint(job_desc)
        return job_desc

    def get_jd_env(self, job_desc, cli_args):
        # The Environment section is required.
        if 'environment' not in job_desc.keys():
            log_err('No environment section in job descriptor.')
            raise Exception

        jd_env = {}
        for key in job_desc['environment'].keys():
            jd_env[key.lower()] = job_desc['environment'][key]

        jd_env.update(home=self.get_jd_env_home(jd_env))

        # Override job descriptor settings with command line args.
        # job_desc.update(cli_args)
        if ('userid' in cli_args) and (len(cli_args['userid']) > 0):
            jd_env['userid'] = cli_args['userid']
        if ('log_lvl' in cli_args) and (len(cli_args['log_lvl']) > 0):
            jd_env['log_lvl'] = cli_args['log_lvl']
        return jd_env

    def get_jd_env_home(self, jd_env):
        # Home is required in the environment.
        if 'home' not in jd_env.keys():
            log_err('No home section in job descriptor environment.')
            raise Exception

        jd_env_home = {}
        for key in jd_env['home'].keys():
            jd_env_home[key.lower()] = jd_env['home'][key]

        if 'root' not in jd_env_home.keys():
            log_err('No root path in home section of job descriptor environment.')
            raise Exception

        return jd_env_home

    def get_jd_appl(self, job_desc):
        # The Application section is required.
        if 'application' not in job_desc.keys():
            log_err('No application section in job descriptor.')
            raise Exception

        # Application name and arguments are required.
        if 'name' not in job_desc['application'].keys():
            log_err('No application name in job descriptor.')
            raise Exception
        if 'args' not in job_desc['application'].keys():
            log_err('No application args in job descriptor.')
            raise Exception

        # Args are application-defined, so don't fold the case of any keys.  Just pass
        # the args to the application as they are defined in the job descriptor.
        jd_appl = {}
        jd_appl['name'] = job_desc['application']['name']
        jd_appl['args'] = job_desc['application']['args']
        return jd_appl

    def get_job_name(self):
        return self.name

    def get_userid(self):
        return self.userid

    def get_log_level(self):
        return self.log_lvl

    def print(self):
        print('Job:  %s' % (self.job_desc_fn))
        print('   name:  %s' % (self.name))
        print('   description:  %s' % (self.desc))
        print('   program:  %s' % (self.pgm))
        print('   userid:  %s' % (self.env_userid))
        print('   home: %s' % (self.env_home))
        print('   logs path: %s' % (self.env_home_logs_path))
        print('   spool path: %s' % (self.env_home_spool_path))
        print('   log level: %s\n' % (self.env_log_lvl))
        print('   application: %s\n' % (self.appl_name))
        print('   args: \n      ', self.appl_args)
        return



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
        # Tell the user where their results are, and how long the job took to run.
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

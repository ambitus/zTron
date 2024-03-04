"""
  job.py - all resources associated with a zTron job

  Author: Joe Bostian

  Copyright Contributors to the Ambitus Project.

  SPDX-License-Identifier: Apache-2.0
"""
import argparse
import yaml

from ztron.mvs import command
from ztron.mvs import dataset
from ztron.uss import file
from ztron.uss import user
from ztron.log import Log

# Log method wrappers for easy access.  These are for application use - you won't
# be able to import them from internal ztron code.
def log_info(mcp,fmt,args=None):
    ztron.log.log('info',fmt,args)
def log_warn(mcp,fmt,args=None):
    ztron.log.log('warn',fmt,args)
def log_err(mcp,fmt,args=None):
    ztron.log.log('err',fmt,args)
def log_trc(mcp,fmt,args=None):
    ztron.log.log('trace',fmt,args)


class Job():
    '''
    '''
    def __init__(self, argc=0, argv=None):
        self.job_desc_fn = ''
        self.name = ''
        self.desc = ''
        self.env_userid = ''
        self.env_home = ''
        self.env_home_log_path = ''
        self.env_home_spool_path = ''
        self.env_log_lvl = ''
        self.env_keep_spool = True
        self.appl_name = ''
        self.appl_args = {}

        # Resources allocated during the execution of a job.
        self.DD_list = []
        self.temp_datasets = []
        self.temp_files = []
        self.log = None
        self.ts_start = None

        # Get all input from the command line and job descriptor.
        self.job_desc = self.parse_job_desc(argc, argv)

        # Build the job from the specified input.
        self.job_desc_fn = self.job_desc['filename']
        self.name = self.job_desc['name']
        self.desc = self.job_desc['description']
        self.env_userid = self.job_desc['environment']['userid']
        self.env_home = self.job_desc['environment']['home']['root']
        self.env_home_log_path = self.env_home+'/'+self.job_desc['environment']['home']['logs']
        self.env_home_spool_path = self.env_home+'/'+self.job_desc['environment']['home']['spool']
        self.env_log_lvl = self.job_desc['environment']['log_lvl']
        self.env_keep_spool = self.job_desc['environment']['keep_spool']
        self.appl_name = self.job_desc['application']['name']
        self.appl_args = self.job_desc['application']['args']
        self.log = Log('ztron.log', self.env_home_log_path, self.env_log_lvl)
        return

    def finish(self):
        return

    # Methods to acquire and process the job descriptor from input args.
    def parse_job_desc(self, argc, argv):
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

        if 'job' not in cli_args.keys():
            log_err('No job descriptor specified.')
            raise Exception

        # Load the job descriptor file with environment settings and application 
        # arguments.
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
        job_desc.update(environment=self.parse_jd_env(job_desc, cli_args))
        job_desc.update(application=self.parse_jd_appl(job_desc)) 
        return job_desc

    def parse_jd_env(self, job_desc, cli_args):
        # The Environment section is required.
        if 'environment' not in job_desc.keys():
            log_err('No environment section in job descriptor.')
            raise Exception

        jd_env = {}
        for key in job_desc['environment'].keys():
            jd_env[key.lower()] = job_desc['environment'][key]

        jd_env.update(home=self.parse_jd_env_home(jd_env))

        # Override job descriptor settings with command line args.
        if ('userid' in cli_args) and (len(cli_args['userid']) > 0):
            jd_env['userid'] = cli_args['userid'].upp[[er()]]
        if ('log_lvl' in cli_args) and (len(cli_args['log_lvl']) > 0):
            jd_env['log_lvl'] = cli_args['log_lvl']

        # Make sure there is a userid and is upper case.
        if 'userid' in jd_env:
            jd_env['userid'] = jd_env['userid'].upper()
        else:
            jd_env['userid'] = get_userid()
        return jd_env

    def parse_jd_env_home(self, jd_env):
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

    def parse_jd_appl(self, job_desc):
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

    def run(self, cmd: str='', DD_list: list=[]) -> dict:
        print(f'--- Running {cmd}, DDs:')
        for dd in self.DD_list:
            print(f'      {dd.get_mvscmd_string()}')
        return command.run(cmd, self.DD_list)

    # Methods for managing MVS resources.
    def append_temp_dataset_list(self, dataset_name: str) -> None:
        self.temp_datasets.append(dataset_name)
        return

    def create_DD_dataset(self, name: str, resource: str) -> None:
        print('--- Creating %s for %s' % (name, resource))
        self.DD_list.append(dataset.create_DD(name, resource))
        return

    def create_DD_file(self, name: str, resource: str) -> None:
        print('--- Creating %s for %s' % (name, resource))
        self.DD_list.append(file.create_DD(name, resource))
        return

    def create_spool_DD(self) -> None:
        spool_dataset = dataset.create_spool_dataset(self.env_userid)
        self.temp_datasets.append(spool_dataset['name'])
        self.create_DD_dataset('SYSPRINT', spool_dataset['name'])
        return

    def create_task_DD(self, task: list) -> None:
        task_file = file.build_task_file(task)
        self.temp_files.append(task_file)
        self.create_DD_file('SYSIN', task_file)
        return

    # Conventional getter routines
    def get_DD_list(self):
        return self.DD_list

    def get_job_name(self):
        return self.name

    def get_userid(self):
        return self.userid

    def get_log_level(self):
        return self.log_lvl

    def get_appl_args(self):
        '''
        get_appl_args - get zTron application arguments
        '''
        return self.appl_args

    def show(self):
        '''
        show - Show a job and all of the logs for it from previous runs.
        '''
        self.print()
        return

    def print(self):
        print('Job:  %s' % (self.job_desc_fn))
        print('Environment:')
        print('   name:  %s' % (self.name))
        print('   description:  %s' % (self.desc))
        print('   userid:  %s' % (self.env_userid))
        print('   home: %s' % (self.env_home))
        print('   log path: %s' % (self.env_home_log_path))
        print('   spool path: %s' % (self.env_home_spool_path))
        print('   log level: %s' % (self.env_log_lvl))
        print('   keep spool: ', self.env_keep_spool, '\n')
        print('Application: %s' % (self.appl_name))
        print('   args:')
        for arg_key, arg_val in self.appl_args.items():
            print('         %s: %s' % (arg_key, arg_val))
        print('\nResources:')
        print('   Temp dataset names:')
        for temp_ds in self.temp_datasets:
            print('      %s' % temp_ds)
        print('   Temp file names:')
        for temp_file in self.temp_files:
            print('      %s' % temp_file)
        print('   Data definitions in use:')
        for dd in self.DD_list:
            print('      %s' % (dd.get_mvscmd_string()))
        return

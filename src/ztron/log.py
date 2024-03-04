"""
  log.py - the zTron Log class.  A log is a timestampted directory that contains
           a collection of log files.

  Author: Joe Bostian

  Copyright Contributors to the Ambitus Project.

  SPDX-License-Identifier: Apache-2.0
"""
import subprocess, time, os, sys

from ztron.log_file import LogFile

# Levels of logging output
LOG_TYPES = ['minimal', 'verbose', 'debug']
LOG_MINIMAL = 0
LOG_VERBOSE = 1
LOG_DEBUG = 2

class Log:
    def __init__(self, log_name, log_path, log_type):
        self.log_name = ''
        self.abs_log_path = ''
        self.main_log_file = None
        self.stage_log_file = None
        self.main_log_file_name = ''
        self.log_level = self.get_log_level(log_type)
        self.f_staged = False

        # Work with the absolute path to the log directory.
        try:
            if log_path != None:
                if log_path[0] == '/':
                    self.abs_log_path = log_path
                else:
                    self.abs_log_path = os.path.abspath(log_path)
            else:
                self.log('err','Error - no log path specified.',None)
                raise exception
        except:
            print('---- abspath exception')
            raise Exception

        # Assemble the full path to the log directory
        self.log_name = log_name + '_' + time.strftime('%Y%m%d-%H%M%S')
        self.abs_log_path = self.abs_log_path + '/' + self.log_name

        # Make sure we don't overwrite a log that already exists.
        if self.abs_log_path != '':
            if not os.path.exists(self.abs_log_path):
                try:
                    cp = subprocess.run(args=['mkdir', '-p', self.abs_log_path])
                    cp.check_returncode()
                except:
                    print('---- subprocess run exception')
                    raise Exception

            # Create the pipeline log, which is the root log that points to
            # everything else.
            # try:
            #     self.main_log_f = open(self.abs_log_path+'/'+self.main_log_file_name, 'w+')
            # except:
            #     print('---- open failed for %s/%s' % (self.full_path, self.pipeline_log_name))
            #     raise Exception
            self.main_log_file = LogFile('main', self.abs_log_path, self.log_level)
        return

    # Close the current log file, and open a new one to log the next stage in the
    # pipeline.
    def new_log_file(file_prefix):
        if self.stage_log_file != None:
            self.stage_log_file.cleanup()
        self.stage_log_file = LogFile(file_prefix, self.abs_log_path, self.log_level)

    def cleanup(self):
        if self.main_log_file != None:
            self.main_log_file.cleanup()
        if self.stage_log_file != None:
            self.stage_log_file.cleanup()
        return

    # Log to the appropriate file - the main log file if this is a single-stage
    # pipeline, or to the current stage log file if multi-stage.
    def log(self, level, fmt, args):
        if self.f_staged:
            self.stage_log_file.log(level, fmt, args)
        else:
            self.main_log_file.log(level, fmt, args)
        return


    # Getters
    def get_full_path(self):
        return self.abs_log_path

    def get_log_level(self, log_type=None):
        """
        Get the log level for the specified log type, or the current log level
        setting if no type is provided.
        """
        if log_type is None:
            return self.log_level
        else:
            return LOG_TYPES.index(log_type.lower())

    def get_log_type(self):
        return LOG_TYPES[self.log_level]


    # Setters
    def set_log_level(self, log_type):
        if log_type.lower() not in LOG_TYPES:
            raise ValueError(f'Error - {log_type} is not a supported log level.')
        return log_types.index(LOG_TYPES.lower())


    # Show ourselves
    def show(self):
        print('-- Log (%s) -------------------------' % self.pipeline_log_name)
        print('     full log path: %s' % (self.full_path))
        print('     log level: %s' % (self.level))

"""
  log_file.py - the zTron LogFile class.  Log files contain the output of
                tasks that run during a pipeline stage.

  Author: Joe Bostian

  Copyright Contributors to the Ambitus Project.

  SPDX-License-Identifier: Apache-2.0
"""
import subprocess, time, os, sys

LEVELS = {'trace': 1, 'info': 2, 'warn': 3, 'err': 4}

class LogFile:
    def __init__(self, file_prefix, abs_log_path, log_level):
        print('---- Creating log file %s' % (file_prefix))
        self.log_file_prefix = 'cmd_' if file_prefix == None else file_prefix
        self.log_file_name = file_prefix + '_' + time.strftime('%Y%m%d-%H%M%S') + '.log'
        self.abs_log_path = abs_log_path
        self.abs_log_file_path = ''
        self.log_f = None
        self.log_level = log_level

        # Caller ensures all pathnames are absolute.
        if self.abs_log_path == None:
            print('Error - no log path specified.')
            raise exception
        self.abs_log_file_path = self.abs_log_path + '/' + self.log_file_name

        # Create and open the log file.
        try:
            self.log_f = open(self.abs_log_file_path, 'w+')
        except:
            print('---- open failed for %s' % (self.abs_log_file_path))
            raise Exception
        return

    def log(self, level, fmt, args):
        if LEVELS[level] >= LEVELS[self.log_level]:
            self.print(level, fmt, args)
            self.write(level, fmt, args)
        return

    def print(self, level, fmt, args):
        if LEVELS[level] >= LEVELS[self.log_level]:
            # This is more complicated than printing, but the flush is needed
            # to keep output in sync with the command text when running a pipeline.
            if args == None:
                if LEVELS[level] >= LEVELS['err']:
                    sys.stderr.write(fmt)
                    sys.stderr.write('\n')
                    sys.stderr.flush()
                else:
                    sys.stdout.write(fmt)
                    sys.stdout.write('\n')
                    sys.stdout.flush()
            else:
                if LEVELS[level] >= LEVELS['err']:
                    sys.stderr.write(fmt % args)
                    sys.stderr.write('\n')
                    sys.stderr.flush()
                else:
                    sys.stdout.write(fmt % args)
                    sys.stdout.write('\n')
                    sys.stdout.flush()
        return

    def write(self, level, fmt, args):
        if LEVELS[level] >= LEVELS[self.log_level]:
            if args == None:
                self.log_f.write(fmt+'\n')
            else:
                # Can't seem to accomplish this is 1 write request ...
                self.log_f.write(fmt % args)
                self.log_f.write('\n')
        return

    def cleanup(self):
        self.log_f.close()
        self.log_f = None
        return

    # Getters

    # Setters

    # Show ourselves
    def show(self):
        print('-- Log file (%s) -------------------------' % self.log_file_name)
        print('     absolute log file path: %s' % (self.abs_log_file_path))
        if self.log_f == None:
            print('     log file is open')
        else:
            print('     log file is closed')
        print('     log level: %s' % (self.log_level))

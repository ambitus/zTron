"""
  log.py - the zTron Log class.  A log is a timestamped directory that contains
           a collection of log files.

    Here is what each of the logging levels mean:
        info - write to STDOUT and the log file.  Messages about the normal operation
               of the application.
        warning - write to STDOUT and the log file.  Messages about a condition that
                  the user needs to be aware of. 
        error - write to STDERR and the log file.  Messages about a failure in the 
                application.  Application may terminate
        critical - write to STDERR and the log file.  A more serious error indicating
                   that the application is terminating.
        debug - write to STDERR and the log file.  Extended debug information about 
                the application.  Avoids cleaning up any resources allocated during 
                the run of the application.

    These log levels match those of the Python logging module.  This code 
    implements the processing model of the logging module.  Please see the logging
    facility for Python for more information:
        https://docs.python.org/3/library/logging.html#formatter-objects

  Author: Joe Bostian

  Copyright Contributors to the Ambitus Project.

  SPDX-License-Identifier: Apache-2.0
"""
import subprocess, time, os, sys
import logging as pylogging


class Log:
    def __init__(self, log_name, log_path, log_type, logger_name):
        self.logger = None
        self.log_name = log_name
        self.log_path = log_path
        self.logger_name = logger_name

        # Wrap the Python logging levels with mnemonics.
        self.log_types = {}
        self.log_types['info'] = pylogging.INFO
        self.log_types['warning'] = pylogging.WARNING
        self.log_types['error'] = pylogging.ERROR
        self.log_types['critical'] = pylogging.CRITICAL
        self.log_types['debug'] = pylogging.DEBUG
        self.log_level = self.log_types[log_type]

        # Work with the absolute path to the log directory.
        try:
            if self.log_path != None:
                if self.log_path[0] != '/':
                    self.log_path = os.path.abspath(self.log_path)
            else:
                sys.stderr.write('Error - no log path specified.')
                raise

        except RuntimeError as err:
            sys.stderr.write('Error - log path is not valid')
            raise

        # Timestamp the log file name, preserving the '.log' suffix.
        self.log_name = log_name.removesuffix('.log') + '_' + time.strftime('%Y%m%d-%H%M%S') + '.log'
        self.full_log_name = self.log_path + '/' + self.log_name

        # Make sure we don't overwrite a log that already exists.
        if self.log_path != '':
            if not os.path.exists(self.log_path):
                try:
                    cp = subprocess.run(args=['mkdir', '-p', self.log_path])
                    cp.check_returncode()

                except:
                    sys.stderr.write('---- subprocess run exception')
                    raise

        self.logger = self.create_logger(self.full_log_name, self.logger_name)
        return

    def create_logger(self, log_name, logger_name):
        pylogger = pylogging.getLogger(logger_name)
        pylogger.setLevel(self.log_level)

        pylogging_cons = pylogging.StreamHandler()
        pylogging_cons.setLevel(self.log_level)
        pylogging_file = pylogging.FileHandler(self.full_log_name, mode='a', encoding='utf-8')
        pylogging_file.setLevel(self.log_level)

        pylogging_fmt = pylogging.Formatter(fmt='%(name)s %(levelname)s: %(message)s',
                                            style='%')
        pylogging_cons.setFormatter(pylogging_fmt)
        pylogging_file.setFormatter(pylogging_fmt)

        pylogger.addHandler(pylogging_cons)
        pylogger.addHandler(pylogging_file)
        return pylogger

    # logger method wrappers
    def info(self, fmt, args=None):
        if args == None:
            self.logger.info(fmt)
        else:
            self.logger.info(fmt, args)
        return

    def warning(self, fmt, args=None):
        if args == None:
            self.logger.warning(fmt)
        else:
            self.logger.warning(fmt, args)
        return

    def error(self, fmt, args=None):
        if args == None:
            self.logger.error(fmt)
        else:
            self.logger.error(fmt, args)
        return

    def debug(self, fmt, args=None):
        if args == None:
            self.logger.debug(fmt)
        else:
            self.logger.debug(fmt, args)
        return

    def critical(self, fmt, args=None):
        if args == None:
            self.logger.critical(fmt)
        else:
            self.logger.critical(fmt, args)
        return

    # Getters
    def get_full_name(self):
        return self.full_log_name

    def get_log_level(self, log_type=None):
        """
        Get the log level for the specified log type, or the current log level
        setting if no type is provided.
        """
        if log_type is None:
            return self.log_level
        elif log_type in self.log_types:
            return self.log_types[log_type]
        else:
            sys.stderr.write('Error - unrecognized log type: {log_type}')
            raise

    def get_log_type(self):
        return list(self.log_types.keys())[list(self.log_types.values()).index(self.log_level)]


    # Setters
    def set_log_level(self, log_type):
        if log_type.lower() not in LOG_TYPES:
            raise ValueError(f'Error - {log_type} is not a supported log level.')
        return self.log_types(log_type)[0]


    # Show ourselves
    def loglog(self):
        self.logger.info(f'Log: {self.log_name}')
        self.logger.info(f'   log file path: {self.log_path}')
        self.logger.info(f'   log type: {self.get_log_type()}')

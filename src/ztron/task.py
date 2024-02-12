"""
  task.py - the zTron Task class.  This is the unit of work to perform for a given
           task.  Collections of commands form a stage of a pipeline.

  Author: Joe Bostian

  Copyright Contributors to the Ambitus Project.

  SPDX-License-Identifier: Apache-2.0
"""
import sys
import subprocess

# A wrapper class to ensure that we have proper exception handling in place when
# running commands.
class Task:
    def __init__(self,log,task):
        self.log = log
        self.task = task;
        self.out = None
        self.err = None
        self.rc = 0;
        return

    def cleanup(self):
        return

    # Run a task in the pipeline.  Peek at the task to see what kind of command
    # it is, and handle it accordingly.
    def run(self, cmd_env):
        if self.task.split(' ')[0] == 'TSO':
            rc = self.run_tso(cmd_env)
        else:
            rc = self.run_linux(cmd_env)
        return rc

    # TSO commands run through the ISPF Gateway.  This is an interactive interface,
    # so we route the command itself through STDIN
    def run_tso(self, cmd_env):
        self.log.log('info','[TSO]> %s',self.task.replace('TSO ', ''))

        # Need to run in the shell to get the env we want to set up.
        proc = subprocess.Popen(args='ISPZINT',
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                env=cmd_env,
                                shell=True)

        try:
            self.out, self.err = proc.communicate(input=bytes(self.task, 'utf-8'))
            self.rc = proc.returncode

            # The gateway is very verbose by default, but the actual output of the
            # TSO command is returned in an XML object <ISPINFO/>.  Skip over all
            # other text in STDOUT and return just the good stuff.
            if self.rc == 0:
                stdout = self.out.decode()
                i_out_start = stdout.find('<ISPINFO>')
                i_out_end = stdout.find('</ISPINFO>') + len('</ISPINFO>')
                self.log.log('info', '%s', (stdout[i_out_start:i_out_end]))
                return 0
            else:
                if len(self.err) > 0:
                   self.log.log('err','%s',self.err.decode())
                self.log.log('err','retcode: %d',self.rc)
                return self.rc
        except OSError as e:
            self.log.log('err',
                'OSError: output = %s, error code = %s',
                (e.output, e.returncode))
        except subprocess.CalledProcessError as e:
            self.log.log('err',
                'CalledProcessError: output = %s, error code = %s',
                (e.output, e.returncode))
        except subprocess.SubprocessError as e:
            self.log.log('err',
                'SubprocessError: output = %s, error code = %s',
                (e.output, e.returncode))
        except:
            e = sys.exc_info()[0]
            self.log.log('err',
                'Error - exception type: %s',
                (e))
        return 1

    # Vanilla Unix/Linux command, so run this through the shell.
    def run_linux(self, cmd_env):
        self.log.log('info','[Shell]> %s',self.task)

        # Need to run in the shell to get the env we want to set up.
        proc = subprocess.Popen(args=self.task,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                env=cmd_env,
                                shell=True)

        try:
            self.out, self.err = proc.communicate()
            self.rc = proc.returncode
            if self.rc == 0:
                self.log.log('info','%s',self.out.decode())
                return 0
            else:
                if len(self.err) > 0:
                   self.log.log('err','%s',self.err.decode())
                self.log.log('err','retcode: %d',self.rc)
                return self.rc
        except OSError as e:
            self.log.log('err',
                'OSError: output = %s, error code = %s',
                (e.output, e.returncode))
        except subprocess.CalledProcessError as e:
            self.log.log('err',
                'CalledProcessError: output = %s, error code = %s',
                (e.output, e.returncode))
        except subprocess.SubprocessError as e:
            self.log.log('err',
                'SubprocessError: output = %s, error code = %s',
                (e.output, e.returncode))
        except:
            e = sys.exc_info()[0]
            self.log.log('err',
                'Error - exception type: %s',
                (e))
        return 1

    def get_cmd(self):
        return self.task

    def show(self):
        self.log.log('info', '       task: %s',self.task)
        return

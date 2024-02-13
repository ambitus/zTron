import argparse
import yaml
from ztron import mcp


# Input arguments to the zTron CLI
class Job():
    def __init__(self):
        self.jobname = ''
        self.userid = ''
        self.loglvl = False
        self.config = None

        arg_parser = argparse.ArgumentParser('Run a series of tasks and manage the output')
        arg_parser.add_argument('--job', default=self.jobname)
        arg_parser.add_argument('--userid', default=self.userid)
        arg_parser.add_argument('--loglvl', default=self.loglvl)

        # Update this object from the input args.
        args = arg_parser.parse_args()
        self.__dict__.update(args.__dict__)

        if not self.jobname:
            print_err('No job name specified.')
            raise Exception

        # The jobname represents a configuration file for a corresponding 
        # python application.  Load the yaml from this file for future reference.
        with open(self.jobname, 'r') as file:
            self.config = yaml.safe_load(file)

        self.print()

    def get_jobname(self):
        return self.jobname

    def get_userid(self):
        return self.userid

    def get_log_level(self):
        return self.loglvl

    def print(self):
        print('Args:')
        print('   job name:  %s' % (self.jobname))
        print('   userid:  %s' % (self.userid))
        print('   log level: %s\n' % (self.loglvl))
        print('Job config: ', self.config)


def run():
    job = Job()
    mcp = Mcp(job)
    mcp.run()
    mcp.finish()
import sys
from ztron.run import run_job

if __name__ == '__main__':
    sys.exit(run_job(sys.argv, len(sys.argv)))

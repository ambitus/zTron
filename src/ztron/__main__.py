import sys
from ztron.run import run_job

if __name__ == '__main__':
    sys.exit(run_job(len(sys.argv), sys.argv))

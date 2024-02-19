import sys
from ztron.job import Job
import ztron.mvs.dataset

SUCCESS=0
FAILURE=1

def main(argc=0, argv=None):
    rc = SUCCESS

    print('*** Hi Bubba, from PDSMCopy ***')
    job = Job(argc, argv)
    job.finish()
    return rc

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
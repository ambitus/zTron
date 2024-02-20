import sys
from ztron.job import Job
from ztron.mvs.dataset import create_temp_dataset

SUCCESS=0
FAILURE=1

def main(argc=0, argv=None):
    rc = SUCCESS

    job = Job(argc, argv)
    zargs = job.get_zargs()
    job.create_DD('SYSUT1', zargs['from_pds'])
    job.create_DD('SYSUT2', zargs['to_pds'])
    job.create_spool_DD()
    # job.create_task_DD('COPY', 'SYSUT1', 'SYSUT2', zargs['members'])
    # job.run('IEBCOPY', job.get_DD_list())
    job.show()
    job.finish()
    return rc

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
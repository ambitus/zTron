import sys
from ztron.job import Job


def main(argc=0, argv=None):
    job = Job(argc, argv)
    appl_args = job.get_appl_args()
    job.create_DD_dataset('SYSUT1', appl_args['from_pds'])
    job.create_DD_dataset('SYSUT2', appl_args['to_pds'])
    job.create_spool_DD()

    # The core task that the job performs.
    if ('members' in appl_args) and (len(appl_args['members'])> 0):
        members = ','.join(appl_args['members'])
        task = [' COPY OUTDD=SYSUT2,INDD=((SYSUT1,R))',
               f' SELECT MEMBER=({members})'
               ]
        job.create_task_DD(task)

    job.run('IEBCOPY', job.get_DD_list())
    job.show()
    job.finish()
    return

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
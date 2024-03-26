
from ztron.job import Job

def run_job():
    job = Job()
    job.log_job_desc()
    appl_args = job.get_appl_args()
    job.create_DD_dataset('SYSUT1', appl_args['from_pds'])
    job.create_DD_dataset('SYSUT2', appl_args['to_pds'])
    job.create_spool_DD()

    # Build the copy job, including the PDS members to copy.
    if ('members' in appl_args) and (len(appl_args['members'])> 0):
        # TODO: chunk this into 80 char strings so we don't exceed
        # the limit when adding PDS members to the list.
        members = ','.join(appl_args['members'])
        task = [' COPY OUTDD=SYSUT2,INDD=((SYSUT1,R))',
               f' SELECT MEMBER=({members})'
               ]
        job.create_task_DD(task)

        # Now perform the member copy.
        job.run('IEBCOPY', job.get_DD_list())
        job.show()
    
    job.term()
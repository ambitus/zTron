
from ztron.job import Job

def run_job(argc=0, argv=None):
    job = Job(argv, argc)
    job.run()
    job.finish()
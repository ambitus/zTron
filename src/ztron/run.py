
from ztron.job import Job

def run_job(argc=0, argv=None):
    job = Job(argc, argv)
    job.show()
    job.finish()
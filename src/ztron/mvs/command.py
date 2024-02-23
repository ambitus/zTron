from zoautil_py import mvscmd
from pprint import pprint


def run(cmd: str='', DD_list: list=[]) -> dict:
    '''
    Run an mvs command.

    Params:
        command: The MVS command to execute
        DD_list: List of Data Definitions (DDs) to reference
    Returns:
        results: A dictionary of results from the job
    ''' 
    results = {}

    try:
        results = mvscmd.execute(pgm=cmd, dds=DD_list).to_dict()
    except Exception as e:
        print(f'Error - failed to run {cmd} command')
        print(f'{e.message}')
        print(f'{e.args}')

    print(f'--- Results:')
    pprint(results)
    return results


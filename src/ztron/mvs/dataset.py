from ztron.uss.user import get_userid

from zoautil_py import datasets
from zoautil_py.ztypes import DDStatement, DatasetDefinition


def create_dataset(prefix: str='', parms: dict=None) -> dict:
    """
    Create a dataset and return the info about it as a dictionary.  

    Params:
        prefix: The prefix of the dataset name.
        parms : All the parameters to pass to ZOAU to create a dataset.
    Returns:
        attributes - A dictionary of all the attributes for the created dataset.
    """
    # If a prefix is specified, use it to have ZOAU create a dataset name.  If 
    # there is no prefix, look in the parms for a name field, and use that for
    # the prefix.  If that isn't specified, just default to '<userid>.TEMP'.
    if len(prefix) > 0:
        hlq = prefix
    else:
        if (parms is not None) and ('name' in parms) and (len(parms['name'] > 0)):
            hlq = parms['name'] + '.TEMP'
        else:
            hlq = get_userid() + '.TEMP'

    # High level qualifier for zoau-generated temp names are max 17 characters.
    if len(hlq) > 17:
        raise ValueError(f'Dataset high level qualifier {hlq} must be 17 characters or less')
    dataset_name = datasets.tmp_name(hlq)

    if parms is None:
        dataset_object = datasets.create(dataset_name,"SEQ",)
    else:
        dataset_object = datasets.create(dataset_name, **parms)
    return dataset_object.to_dict()


def create_spool_dataset(userid):
    if len(userid) > 0:
        prefix = userid + '.ZTSPOOL'
    else:
        prefix = get_userid() + '.ZTSPOOL'
    return create_dataset(prefix)


def create_DD(name: str, dataset: str) -> DDStatement:
    '''Create a Data Definition (DD) for a dataset

    Args:
        name - DD name to associate with a dataset
        dataset - the dataset to associate with a DD name

    Return - a ZOAU DDStatement
    '''
    return DDStatement(name.upper(), DatasetDefinition(dataset))
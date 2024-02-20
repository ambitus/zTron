from ztron.uss.user import get_userid

from zoautil_py import datasets, mvscmd
from zoautil_py.ztypes import DDStatement, FileDefinition, DatasetDefinition


def create_temp_dataset(parms: dict=None) -> dict:
    """Create a temporary dataset.
       Create a temporary dataset and return all the necessary info about it 
       as a dictionary.  Keep track of the dataset to it can be cleaned up at 
       ztron termination.

    Paramters:
        parms - (optional): All the parameters to create a dataset in ZOAU.
    Return:
        attributes - A dictionary of all the attributes for the created dataset.
    """
    if (parms is None) or ('name' not in parms) or (len(parms['name'] == 0)):
        dataset_name = datasets.tmp_name(get_userid().upper()+'.TEMP')
    else:
        # High level qualifier for zoau-generated temp names are max 17 characters.
        if len(parms[name]) > 17:
            raise ValueError('Dataset high level qualifier %s must be 17 characters or less' %
                             (parms[name]))
        dataset_name = datasets.tmp_name(parms['name'])

    if parms is None:
        dataset_object = datasets.create(dataset_name,"SEQ",)
    else:
        dataset_object = datasets.create(dataset_name, **parms)
    return dataset_object.to_dict()

    # Remember this dataset for cleanup at termination.
    job.append_temp_dataset_list(dataset_name)
    return dataset_object.to_dict()


def create_DD(name: str, resource: str) -> DDStatement:
    return DDStatement(name, DatasetDefinition(resource['name'].upper()))
def create_temp_dataset(options: dict=None) -> dict:
    """Create a temporary dataset.
       Create a dataset and return all the necessary info about it as a dictionary

    Paramters:
        options - <dict> (optional): All of the options that one could set to create
                                     a dataset in ZOAU. Defaults to None.
    Return:
        dataset_dictionary - <dict>: A complete dictionary contains info of the
                                     created temporary dataset
    """
    zos_userid = get_zos_userid()
    dataset_name = f"{zos_userid}.TEMPRARY"
    dataset_name = datasets.tmp_name(dataset_name)
    _mcs_data_set_list.append(dataset_name)
    if options is None:
        dataset_object = datasets.create(dataset_name,"SEQ",)
    else:
        dataset_object = datasets.create(dataset_name, **options)
    return dataset_object.to_dict()


def create_non_temp_dataset(options: dict=None) -> dict:
    """Create a temporary dataset.
       Create a dataset and return all the necessary info about it as a dictionary

    Paramters:
        options - <dict> (optional): All of the options that one could set to create
                                     a dataset in ZOAU. Defaults to None.
    Return:
        dataset_dictionary - <dict>: A complete dictionary contains info of the
                                     created temporary dataset
    """
    if options is None or "name" not in options:
        zos_userid = get_zos_userid()
        dataset_name = datasets.tmp_name(zos_userid)
    else:
        dataset_name = datasets.tmp_name(options["name"])
    if options is None:
        dataset_object = datasets.create(dataset_name,"SEQ")
    else:
        dataset_object = datasets.create(dataset_name, **options)

    # Keep track of datasets you create in a global variable
    _mcs_data_set_list.append(dataset_name)

    return dataset_object.to_dict()
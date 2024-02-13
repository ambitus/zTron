
def create_unique_output_file(filename:str)->str:
    """Create a unique ouput file based on the filename

    Args:
        filename (str): The base filename

    Returns:
        str: a unique version of the filename
    """
    cwd = os.getcwd()  # need explicit paths for dds
    static_time = str(datetime.now().timestamp())

    # This will hold any MVS messages
    outfile = f"{cwd}/{filename}.{static_time}"

    return outfile


def get_temp_file_name(name : str=None, working_directory : str="/tmp") -> str:
    """Define a temporary filename to be used the filesystem

    Parameters:
        name - <str> (optional): A string containing the name of the file. 
                                Defaults to None
        working_directory - <str>(optional): A directory where the file can live. 
                                            Defaults to tmp
    Return:
        filename - <str>: The name of the created file
    """
    # First lets make sure the name has the word TEMPORARY in it
    if name is None:
        name = "TEMPRARY"
    else:
        name = f"{name}.TEMPRARY"

    # We get a data and timestamp to ensure that the file name is unique
    static_time = str(datetime.now().timestamp())
    temp_file_name = f"{working_directory}/{name}.{static_time}"

    # Keep track of all the files in our global _mcs_data_set_list too
    _mcs_data_set_list.append(temp_file_name
                            )
    # Now we can return the generated name
    return temp_file_name



def create_input_file(input_list : list, input_file_name : str, codepage : str="cp1047"):
    """Create the input file that will be used for an input DD. It is meant to
       fit the 72 character limit that is in JCL card decks

    Parameters:
        input_list - <list>: List of strings containing the input
        input_file_name - <str>: The name of the file
        codepage - <str> (optional): The codepage to use when writing the data.
                                     Defaults to "cp1047".
    """
    # (make sure it's EBCDIC and less than 72 bytes)
    with open(input_file_name, "w", encoding=codepage) as sysin:
        for listitem in input_list:
            if len(listitem) > 72:
                print("Input lines must be less than 72 chars\n")
                print(f"{listitem} is length: {len(listitem)} and is ignored")

            else:
                sysin.write(f"{listitem}\n")
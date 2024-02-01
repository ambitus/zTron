#!/usr/bin/env python3
"""Provide support for mvscmd dds
"""
import os
import sys
import subprocess
from datetime import datetime
from zoautil_py import datasets, mvscmd
from zoautil_py.types import DDStatement, FileDefinition, DatasetDefinition

_mcs_data_set_list=[]

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

def get_zos_userid() -> str:
    """Get the z/OS userid from the system.
    Parameters: None
    Return:
        user_id - <str>: The z/OS user id of the caller
    """
    uid = str(subprocess.run(["id"], shell=True, capture_output=True, check=False).stdout)
    user_id = uid[(uid.find("(")+1):uid.find(")")]
    return user_id


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


def create_input_dd(input_list : list, ddname : str="SYSIN")->DDStatement:
    """Create an input DD basedd on a list

    Parameters:
        input_list - <list>: A list of strings which is input to the DD
        ddname - <str> (optional): The DDName used for input. Defaults to "SYSIN".
    Return:
        <DDStatement>: The created DD statement 
    """
    # First we need to create the name of the temporary file
    # Use the ddname in the file
    temporary_file_name = get_temp_file_name(ddname)

    # Now create the file that will hold the input
    create_input_file(input_list, temporary_file_name)

    # Now create the DD that will hold the input

    return DDStatement(ddname, FileDefinition(temporary_file_name))


def cleanup_temporaries(debugging :bool=False):
    """Remove any temporary files or datasets

    Args:
        debugging - <bool> (optional): Debug flag. If set keep files around
        _mcs_data_set_list - <list> (implicit): Global variable that is updated
                                                whenever a dataaet or file is created
    Return:
        None
    """
    for dataset in _mcs_data_set_list:
        if "TEMPRARY" in dataset:
            if "/" in dataset:
                if debugging:
                 print(f"Temporary file: {dataset} has not been erased")
                else:
                    os.remove(dataset)
            else:
                if debugging:
                    print(f"Temporary Dataset: {dataset} has not been erased")
                else:
                    # All uppercase names are DATASETS
                    return_code = datasets.delete(dataset)
                    if return_code != 0:
                        print(f"Error erasing {dataset}")

def main():
    """Test this with a Dataset Member Copy

    Args:
         input (String):  The input dataset
         output (String): The output dataset
         members (List):  A list of members that need to be coppied
    """
    # If I don't have 2 arguments then I can't do anything
    if len(sys.argv) < 3:
        print("You must provide an input and output dataset")
        sys.exit(1)

    # Identify input and output datasets
    input_dataset = sys.argv[1]
    output_dataset = sys.argv[2]
    member_list = sys.argv[3:]
    list_of_members = ",".join(member_list)
    
    # First define a list of DD statements
    dd_list=[]
    
    # Define the input dataset (SYSUT1) and the output dataset (sysut2)
    dd_list.append(DDStatement("SYSUT1", DatasetDefinition(input_dataset.upper())))
    dd_list.append(DDStatement("SYSUT2", DatasetDefinition(output_dataset.upper())))
    
    # Define a sysprint dataset
    output_dataset_dictionary=create_non_temp_dataset()
    dd_list.append(DDStatement("SYSPRINT",DatasetDefinition(output_dataset_dictionary["name"])))
    
    # Create an input dd to list the Global Zone
    dd_list.append(create_input_dd([" COPY OUTDD=SYSUT2,INDD=((SYSUT1,R))",
                          f" SELECT MEMBER=({list_of_members.upper()})"]))

    # Now run the Command
    command_return_dictionary = mvscmd.execute(pgm="IEBCOPY", dds=dd_list).to_dict()
    print(command_return_dictionary)


    if command_return_dictionary['rc']>0:
        print(f"Command failed with a return code of: {command_return_dictionary['rc']}")
    else:
        print(f"Command succeeded. Output can be found in: {output_dataset_dictionary['name']}")

    # Remove the temporary file and Dataset
    cleanup_temporaries(False)

if __name__ == "__main__":
    main()
    

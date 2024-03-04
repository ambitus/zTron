import os
from datetime import datetime

from ztron.uss.user import get_userid

from zoautil_py.ztypes import DDStatement, FileDefinition


def create_file(name: str='', codepage=None) -> None:
    """
    Create an empty file.

    Params:
        name: A string containing the name of the file. 
        codepage: Encoding of file contents.  Defaults to UTF-8.
    Returns:
        None
    """
    if len(name) == 0:
        print('Error - please supply a name for the file to create.')
        raise Exception

    try:
        # Create the file with the proper tag.
        if codepage is not None:
            f = open(name, 'x', encoding=codepage)
        else:
            f = open(name, 'x')
        f.close()

    except Exception as e:
        print(f'Error - failed to create {name}')
        print(f'{e.message}')
        print(f'{e.args}')
    return


def create_temp_txt_file(prefix:str='', 
                         qualifier:str='ZTTEMP', 
                         working_dir:str='/tmp',
                         codepage=None) -> str:
    """
    Create a temporary file in the specified working directory.  The 
    file will be created at this location:
       <working_dir>/<prefix>_<qualifier>'_yyyymmdd_hhmmss.txt

    Params:
        prefix: The prefix of the file (defaults to userid).
        qualifier: second component of the name, indicates file use (temp, 
                   sysin, other).
        working_dir: A directory where the file can live. 
        codepage: Encoding of file contents.  Defaults to UTF-8.
    Returns:
        temp_file_path: An absolute temp file path name
    """
    if len(prefix) == 0:
        if len(qualifier) == 0:
            file_name = get_userid() + '_' + 'ZTTEMP' + '_'
        else:
            file_name = get_userid() + '_' + qualifier + '_'
    else:
        if len(qualifier) == 0:
            file_name = prefix + '_' + 'ZTTEMP' + '_'
        else:
            file_name = prefix + '_' + qualifier + '_'

    # Create a human-readable date and time to build the rest of the file name.
    now = datetime.now()
    suffix = str(now.year).zfill(4)+str(now.month).zfill(2)+str(now.day).zfill(2)+'_'
    suffix += str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
    file_path = f"{working_dir}/{file_name}{suffix}.txt"

    create_file(file_path, codepage)
    print(f'--- File {file_path} created')
    return file_path


def create_DD(name: str, file: str) -> DDStatement:
    '''Create a Data Definition (DD) for a USS file

    Args:
        name - DD name to associate with a file
        file - the file to associate with a DD name

    Return - a ZOAU DDStatement
    '''
    return DDStatement(name.upper(), FileDefinition(file))


def build_task_file(deck: list, codepage: str='cp1047') -> str:
    """
    Create a file containing the text pointed to by a JCL input DD.  Each line 
    of the file adheres to the rules of a JCL card, including leading blanks 
    and the 72 character limit.  Since it's native z/OS that will be running
    this job deck, the text for it has to be in EBCDIC.

    Params:
        deck - The list of strings corresponding to cards in a JCL deck.
        codepage - The codepage to use when writing the data.  Defaults to 
                   "cp1047".
    """
    task_file_name = create_temp_txt_file('', 'ZTSYSIN', '/tmp', codepage)

    # Add the content of the deck to the task file.
    try:
        with open(task_file_name, "w", encoding=codepage) as sysin:
            for card in deck:

                if len(card) <= 72:
                    sysin.write(f"{card}\n")

                else:
                    print("Error - Input lines must be less than 72 chars")
                    print(f"   {card:40}... is length: {len(card)} and is ignored")
                    
    except:
        os.remove(task_file_name)
        task.file = ''
    return task_file_name
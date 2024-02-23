import os
import pwd

def get_userid() -> str:
    """
    Get the z/OS userid from the system

    Params:
        None
    Returns:
        user_id: The user id of the caller
    """
    return pwd.getpwuid(os.getuid())[0].upper()
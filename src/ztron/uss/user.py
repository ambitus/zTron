import subprocess

def get_userid() -> str:
    """Get the z/OS userid from the system.
    Parameters: None
    Return:
        user_id - <str>: The z/OS user id of the caller
    """
    uid = str(subprocess.run(["id"], shell=True, capture_output=True, check=False).stdout)
    user_id = uid[(uid.find("(")+1):uid.find(")")]
    return user_id
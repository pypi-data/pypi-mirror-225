# Miscellaneous functions
import os

from common import logfile

def delete_logs():
    """
    Delete the logfile if it exists
    """

    # delete any previous log file
    try:
        os.remove(logfile)
    except OSError:
        pass

    
class FileAlreadyLoadedException(Exception):
    """
    Raise when a file is already loaded but .load() is called again
    """

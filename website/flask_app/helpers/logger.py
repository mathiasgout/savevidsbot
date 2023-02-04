import logging
import os
from sys import stdout
from functools import wraps


def get_logger(logger_name: str) -> logging.Logger:

    # Create log folder
    LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "log")
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

    # Création du logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG) # Modification du niveau de criticité du logger

    # Création d'un formatteur
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s/%(filename)s - %(funcName)s() - %(message)s")

    # Création d'un StreamHandler pour afficher la log dans la console
    stream_handler = logging.StreamHandler(stdout)
    stream_handler.setFormatter(formatter) # Liaison le formatteur au handler   
    logger.addHandler(stream_handler)
    
    file_handler = logging.FileHandler(os.path.join(LOG_PATH, "app.log"))
    file_handler.setFormatter(formatter) # Liaison le formatteur au handler
    logger.addHandler(file_handler)

    return logger

def exception(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                issue = "exception in "+func.__name__+"\n"
                issue = issue+"=============\n"
                logger.exception(issue)
                raise
        return wrapper
    return decorator
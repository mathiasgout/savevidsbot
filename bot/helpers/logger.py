import logging
from sys import stdout
from functools import wraps


def get_logger(logger_name: str) -> logging.Logger:

    # Création du logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG) # Modification du niveau de criticité du logger

    # Création d'un formatteur
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s/%(filename)s - %(funcName)s() - %(message)s")

    # Création d'un StreamHandler pour afficher la log dans la console
    stream_handler = logging.StreamHandler(stdout)
    stream_handler.setFormatter(formatter) # Liaison le formatteur au handler   
    logger.addHandler(stream_handler)

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
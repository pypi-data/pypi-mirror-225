import logging


def get(name, file="./log.log"):
    from opaw.util import mkdirs
    """
    Gets a logger with the given name (singleton)
    :param name: logger name
    :param file: the file logs will be saved (default: ./log.log)
    """
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        # make parent dirs if needed
        mkdirs(file)
        logger.setLevel(logging.INFO)

        # stream handler
        stream_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(stream_formatter)
        stream_handler.setLevel(logging.INFO)
        logger.addHandler(stream_handler)

        # file handler
        file_handler = logging.FileHandler(file, mode="w", encoding="utf-8")
        file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s(%(name)s) %(message)s")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

    return logger

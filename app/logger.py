import logging

def create_logger():
    logger = logging.getLogger("basik")
    logger.setLevel("DEBUG")

    file_handler = logging.FileHandler("logs.basik.txt")
    logger.addHandler(file_handler)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)

    return logger
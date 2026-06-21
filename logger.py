import logging
import os


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    # Create a console handler and set the level to INFO
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    path = os.environ.get("EDENRED_LOG_DIR", "logs")
    try:
        os.makedirs(path, exist_ok=True)
        fh = logging.FileHandler(os.path.join(path, "app.log"))
    except OSError:
        logger.warning("File logging disabled: cannot write to %s", path)
    else:
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)


    return logger

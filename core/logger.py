import logging, os
os.makedirs("logs", exist_ok=True)

def setup_logger():
    logger = logging.getLogger("api"); logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler("logs/api.log", mode="a")
        fmt = logging.Formatter("%(asctime)s | [%(levelname)s] | %(message)s")
        fh.setFormatter(fmt); logger.addHandler(fh)
    return logger

logger = setup_logger()

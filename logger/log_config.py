import logging
def setup_logging():
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

setup_logging()
logger = logging.getLogger(__name__)
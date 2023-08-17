from loguru import logger
from datetime import datetime

logger.add(f"logs/api_{datetime.now().strftime('%Y_%m_%d')}.log", rotation="1 day", enqueue=True, encoding='UTF-8')


def log_info(message):
    logger.info(message)

def log_error(message):
    logger.error(message)

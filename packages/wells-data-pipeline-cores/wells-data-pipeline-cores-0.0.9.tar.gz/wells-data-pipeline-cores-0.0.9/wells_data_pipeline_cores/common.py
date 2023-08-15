import sys
import logging

# Create a logging mechanism
def enable_logging(level=logging.INFO):
    # Set the logging level for all azure-* libraries
    logger = logging.getLogger('azure')
    logger.setLevel(logging.ERROR)
    logger = logging.getLogger("snowflake")
    logger.setLevel(logging.ERROR)
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [stdout_handler]
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

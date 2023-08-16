import logging
import os

LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = (
    "[%(asctime)s][%(levelname)s][%(name)s][%(funcName)s]"
    + "[%(filename)s:%(lineno)d] %(message)s"
)

# Create a logger
logger = logging.getLogger()
logger.handlers = []

# Add console handler with INFO level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
logger.addHandler(console_handler)

if os.path.exists("gpt4docs.debug.log"):
    os.remove("gpt4docs.debug.log")

# Add file handler with DEBUG level
file_handler = logging.FileHandler("gpt4docs.debug.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
logger.addHandler(file_handler)

logger.setLevel(logging.DEBUG)

# Ignore logs from packages
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("chromadb.segment.impl.vector.local_persistent_hnsw").setLevel(
    logging.CRITICAL
)
logging.getLogger("blib2to3.pgen2.driver").setLevel(logging.CRITICAL)

import logging
import logging.config

logging.config.fileConfig("loggingconf/logging.conf")
logger = logging.getLogger("root")


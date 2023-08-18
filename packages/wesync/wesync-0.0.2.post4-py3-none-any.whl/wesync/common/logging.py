import logging
import os
import sys
from copy import copy

LOG_FILE_PATH = "/var/log/wlkstash.log"


class ColorFormatter(logging.Formatter):
    def format(self, record):
        record = copy(record)
        if record.levelname == "INFO":
            record.msg = '\033[1;36m' + str(record.msg) + '\033[0m'
        elif record.levelname == "WARNING":
            record.msg = '\033[1;33m' + str(record.msg) + '\033[0m'
        elif record.levelname == "ERROR":
            record.msg = '\033[1;31m' + str(record.msg) + '\033[0m'
        elif record.levelname == "DEBUG":
            record.msg = '\033[0;95m' + str(record.msg) + '\033[0m'
        elif record.levelname == "CRITICAL":
            record.msg = '\033[1;41m' + str(record.msg) + '\033[0m'
        elif record.levelno <= 5 and record.levelno > 1:
            record.msg = '\033[0;32m' + str(record.msg) + '\033[0m'
        elif record.levelno <= 1:
            record.msg = '\033[0;94m' + str(record.msg) + '\033[0m'

        return super().format(record)


globalLogger = logging.getLogger()
globalLogger.setLevel(1)

# Log everything to file
if os.access(LOG_FILE_PATH, os.W_OK):
    fileLogging = logging.FileHandler(LOG_FILE_PATH)
    fileLogging.setFormatter(logging.Formatter("%(asctime)s : %(name)s/%(processName)s/%(threadName)s %(levelname)s in %(funcName)s -> %(message)s"))
    fileLogging.setLevel(5)
    globalLogger.addHandler(fileLogging)

# Set colored logging for console (stdout)
consoleLogging = logging.StreamHandler(sys.stdout)
# consoleLogging.setFormatter(ColorFormatter("\033[1;37m%(asctime)s\033[0m: %(levelname)s in \033[1;37m%(funcName)s\033[0m -> %(message)s"))
consoleLogging.setFormatter(ColorFormatter("> %(message)s"))

consoleLogging.setLevel(logging.INFO)
globalLogger.addHandler(consoleLogging)


from os import path
import logging
from logtail import LogtailHandler
import coloredlogs
import inspect
from datetime import date, timedelta

logger = logging.getLogger(' ')


basepath = path.dirname(__file__)
log_file_name = "log/" + str(date.today())  +"-console.log"
new_file_path= path.abspath(
    path.join(basepath, "..", "..", "..", log_file_name))
filepath = path.abspath(
    path.join(basepath, "..", "..", "..", "log/console.log"))


consoleFile = new_file_path  # '/home/pi/Desktop/log/console.log'
message_format = "%(asctime)s %(name)s %(levelname)s %(message)s"
date_strftime_format = "%H:%M:%S"
formatter = logging.Formatter(fmt=message_format, datefmt=date_strftime_format)

message_format_logtail = "%(levelname)s %(message)s"
logtailFormatter = logging.Formatter(fmt=message_format_logtail)
logtailToken = '9Hh7JWJWbPiHioWKhqLj6MJR'

#logging.basicConfig(level=logging.DEBUG, format=message_format, datefmt=date_strftime_format)
coloredlogs.install(level=logging.INFO, logger=logger,
                    fmt=message_format, datefmt=date_strftime_format)

try:
    with open(consoleFile, 'a+') as consoleFileWrapper:
        # consoleFileWrapper.truncate(0)
        pass
except Exception:
    with open(consoleFile, 'w') as consoleFileWrapper:
        pass

logtailHandler: logging.Handler = LogtailHandler(source_token=logtailToken)
logtailHandler.setFormatter(logtailFormatter)
logtailHandler.setLevel(logging.DEBUG)

consoleFileHandler = logging.FileHandler(filename=consoleFile, mode="a")
consoleFileHandler.setFormatter(formatter)
consoleFileHandler.setLevel(logging.DEBUG)

logger.addHandler(logtailHandler)
logger.addHandler(consoleFileHandler)

logger.info(f"new_file_path = {new_file_path}")

def getLineInfo():
    return inspect.stack()[1][1] + ":" + inspect.stack()[1][2] + ":" + inspect.stack()[1][3]

# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import with_statement 

import os
import threading

import logging

import sickbeard

from sickbeard import classes


# Filename of the log
LOG_FILE='sickbeard.log'

# number of log files to keep
NUM_LOGS = 3

# log size in bytes
LOG_SIZE = 10000000 # 10 megs

ERROR = logging.ERROR
WARNING = logging.WARNING
MESSAGE = logging.INFO
DEBUG = logging.DEBUG

reverseNames = {u'ERROR': ERROR,
                u'WARNING': WARNING,
                u'INFO': MESSAGE,
                u'DEBUG': DEBUG}


class UILoggingHandler(logging.Handler):
    def emit(self, record):
        classes.ErrorViewer.add(classes.UIError(record.message))

# Set up the logger
logger = logging.getLogger('sickbeard')
logger.setLevel(logging.DEBUG)

# Add errors to the UI logger
ui_handler = UILoggingHandler()
ui_handler.setLevel(logging.ERROR)
logger.addHandler(ui_handler)

# Set up a RotatingFileHandler
log_file = os.path.join(sickbeard.LOG_DIR, LOG_FILE)
rotating_handler = logging.handlers.RotatingFileHandler(log_file
        maxBytes=LOG_SIZE, backupCount=NUM_LOGS)
rotating_handler.setLevel(logging.DEBUG)
rotating_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%b-%d %H:%M:%S'))
logger.addHandler(rotating_handler)

# define a Handler which writes INFO messages or higher to the sys.stderr
if consoleLogging:
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    console.setFormatter(logging.Formatter('%(asctime)s %(levelname)s::%(message)s', '%H:%M:%S'))

    # add the handler to the root logger
    logger.addHandler(console)


def log(toLog, logLevel=MESSAGE):
    logger.log(toLog, logLevel)

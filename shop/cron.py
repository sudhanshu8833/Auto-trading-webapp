import logging
from .models import *
import os
import traceback
from .strategy.Volume_stoploss import *

logger = logging.getLogger('dev_log')



def my_scheduled_job():
    logged_errors = set()

    try:
        start_stoploss_for_volume()

    except Exception as e:

        if str(e) not in logged_errors:
            logger.info(str(traceback.format_exc()))



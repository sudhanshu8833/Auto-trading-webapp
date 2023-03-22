import logging
from .models import *
import os
import traceback
from .strategy.Volume_stoploss import *
from .strategy.PPM_BTST_CLOSE import *
logger = logging.getLogger('dev_log')



def my_scheduled_job():
    logged_errors = set()

    try:
        logger.info("testing about the cron")
        start_stoploss_for_volume()

    except Exception as e:

        if str(e) not in logged_errors:
            logger.info(str(traceback.format_exc()))


def PPM_BTST_scheduled():
    logged_errors = set()
    try:
        logger.info("PPM BTST Close Position initiated")
        close_position_for_ppm_btst()
    except Exception as e:

        if str(e) not in logged_errors:
            logger.info(str(traceback.format_exc()))
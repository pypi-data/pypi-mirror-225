import datetime
import logging


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger("Parser")


def schedule_date_parser(date):
    today_raw = datetime.datetime.now()
    today = today_raw.strftime("%Y-%m-%d")
    if date.upper() == "TODAY":
        day = today_raw.strftime("%Y-%m-%d")
        day_of_week = today_raw.weekday() + 2
    elif date.upper() == "TOMORROW":
        day = (today_raw + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        day_of_week = (today_raw + datetime.timedelta(days=1)).weekday() + 2
    else:
        try:
            day_raw = datetime.datetime.strptime(date, "%d/%m/%Y")
            day = day_raw.strftime("%Y-%m-%d")
            day_of_week = day_raw.weekday() + 2
        except Exception as e:
            logger.info(e)
            today, day, day_of_week = None, None, None
    return today, day, day_of_week

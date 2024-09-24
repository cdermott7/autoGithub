import schedule
import time
from datetime import datetime
import pytz
from src.utils.logger import scheduler_logger

class Scheduler:
    def __init__(self, creation_time, timezone):
        self.creation_time = creation_time
        self.timezone = pytz.timezone(timezone)
        scheduler_logger.info(f"Initialized Scheduler with creation time: {creation_time} {timezone}")

    def schedule_daily(self, job):
        schedule.every().day.at(self.creation_time).do(self._run_job, job)
        scheduler_logger.info(f"Scheduled daily job at {self.creation_time}")

    def run(self):
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                scheduler_logger.error(f"Error in scheduler loop: {str(e)}")
                # Continue running even if there's an error

    def _run_job(self, job):
        current_time = self._get_current_time()
        scheduler_logger.info(f"Running scheduled job at {current_time}")
        try:
            job()
            scheduler_logger.info(f"Completed scheduled job at {self._get_current_time()}")
        except Exception as e:
            scheduler_logger.error(f"Error running scheduled job: {str(e)}")

    def _get_current_time(self):
        return datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S %Z")

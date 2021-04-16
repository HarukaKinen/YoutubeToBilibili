import schedule
import time
from basic_modules.youtube import monitor

schedule.every(5).minutes.do(monitor.download_videos_from_task)

while True:
    schedule.run_pending()
    time.sleep(1)
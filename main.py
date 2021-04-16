import os
from basic_modules.config import config
from basic_modules.youtube import monitor
from basic_modules.database import status

config.read()

#monitor.check_videos()

monitor.download_videos_from_task(status.new.value)
monitor.download_videos_from_task(status.error.value)
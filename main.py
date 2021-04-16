import os
from basic_modules.config import config
from basic_modules.youtube import monitor
from basic_modules.database import status

config.read()

if not os.path.exists("videos"):
    os.mkdir("videos")

if not os.path.exists("thumbnail"):
    os.mkdir("thumbnail")

#monitor.check_videos()

monitor.download_videos_from_task(status.new.value)
monitor.download_videos_from_task(status.error.value)
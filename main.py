import os
from config import config
from youtube import monitor
from database import status

if not os.path.exists("videos"):
    os.mkdir("videos")

if not os.path.exists("thumbnail"):
    os.mkdir("thumbnail")

config.read()

monitor.check_videos()

monitor.download_videos_from_task(status.new.value)
monitor.download_videos_from_task(status.error.value)
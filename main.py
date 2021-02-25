import os
from config import config
from youtube import monitor
from database import status

config.read()

if not os.path.exists("videos"):
    os.mkdir("videos")

if not os.path.exists("thumbnail"):
    os.mkdir("thumbnail")

monitor.check_videos()

monitor.download_videos_from_task(status.new.value)
monitor.download_videos_from_task(status.error.value)
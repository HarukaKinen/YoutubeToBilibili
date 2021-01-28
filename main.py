from config import config
from youtube import monitor
from database import status

config.read()

monitor.check_videos()

monitor.download_videos_from_task(status.new.value)
monitor.download_videos_from_task(status.error.value)
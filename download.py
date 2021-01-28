from youtube import monitor
from database import status

monitor.download_videos_from_task(status.new.value)
monitor.download_videos_from_task(status.error.value)
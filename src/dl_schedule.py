import schedule
import time
from modules.database import task
from modules.video import download

def download_from_tasks():
    new = task.get_task_status(1)
    count = 0
    for t in new:
        url = "https://www.youtube.com/watch?v={}".format(t.get_video_id())
        print("[-] downloading {} | status: {}".format(t.get_video_id(), t.get_video_status()))
        download(url)
        count += 1
        if len(new) > 1 and count == len(new) - 1:
            # in case we submmit videos too fast
            time.sleep(20)

    failed = task.get_task_status(4)
    count = 0
    for t in failed:
        url = "https://www.youtube.com/watch?v={}".format(t.get_video_id())
        print("[-] downloading {} | status: {}".format(t.get_video_id(), t.get_video_status()))
        download(url)
        count += 1
        if len(failed) > 1 and count == len(failed) - 1:
            # in case we submmit videos frequently
            time.sleep(20)

schedule.every(5).minutes.do(download_from_tasks)

while True:
    schedule.run_pending()
    time.sleep(1)
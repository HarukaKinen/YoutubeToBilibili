from youtube import downloader
from database import se, task

print("url: ")
url = input()
id = url.replace("https://www.youtube.com/watch?v=", "")
if se.query(task).filter(task.id==id).first() is None:
    print("None")
    task.add_task(id=id)

downloader.download(url)
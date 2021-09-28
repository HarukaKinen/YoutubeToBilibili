from modules.video import download, se, task

print("url: ")
url = input()
if url.find("youtube.com/watch?v=") == -1 and url.find("youtu.be/") == -1:
    print("[!] not a valid youtube video link")
    exit()

if url.find("youtube.com/watch?v=") != -1:
    id = url.replace("https://www.youtube.com/watch?v=", "")
elif url.find("youtu.be/") != -1:
    id = url.replace("https://youtu.be/", "")

if se.query(task).filter(task.id==id).first() is None:
    print(f"[-] {id} is not in database, adding.")
    task.add_task(id=id)

download(url)
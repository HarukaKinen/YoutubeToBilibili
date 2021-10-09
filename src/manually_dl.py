import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--db", help="use db", action='store_true')
args = parser.parse_args()

from modules.video import download
print("url: ")
url = input()
if url.find("youtube.com/watch?v=") == -1 and url.find("youtu.be/") == -1:
    print("[!] not a valid youtube video link")
    exit()

if url.find("youtube.com/watch?v=") != -1:
    id = url.replace("https://www.youtube.com/watch?v=", "")
elif url.find("youtu.be/") != -1:
    id = url.replace("https://youtu.be/", "")

download(url, id, args.db)
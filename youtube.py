import youtube_dl
import os
import json
import requests
import datetime
from database import channel, task, se, status
from bilibili import bilibili
from PIL import Image
from config import config

class downloader:

    sid = ""

    @classmethod
    def download(self, url):
        options = {
            'format': "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
            'forcethumbnail': False,
            'forcetitle': False,
            'forcedescription': False,
            'logger': logger(),
            'outtmpl': u'./videos/%(id)s.%(ext)s',
        }

        print("[Download] Start downloading")

        with youtube_dl.YoutubeDL(options) as dl:
            try:
                dl.cache.remove()
                info = dl.extract_info(url, download=True)
                title = info['title']
                thumbnail_url = info['thumbnail']
                description = info['description']
                id = info['id']
                sid = id
                # https://stackoverflow.com/a/37821542
                img_data = requests.get(thumbnail_url).content
                with open("thumbnail/temp.webp", "wb") as handler:
                    handler.write(img_data)

                im = Image.open("thumbnail/temp.webp").convert("RGB")
                im.save("thumbnail/temp.jpg", "jpeg")
                print("[Download] All done")

                print("[Upload] Start uploading")
                
                if os.path.exists("videos/{}.mp4".format(id)):
                    print("[DEBUG] yes")
                else:
                    print("[DEBUG] no")

                bilibili.upload("videos/{}.mp4".format(id), title, url, "thumbnail/temp.jpg", description)
                os.remove("videos/{}.mp4".format(id))
                os.remove("thumbnail/temp.jpg".format(id))
                os.remove("thumbnail/temp.webp".format(id))
                print("[Upload] Removed video file and thumbnail files.")
                se.query(task).filter(task.id==id).update({'status': status.uploaded.value})
            except Exception as e:
                id = url.replace("https://www.youtube.com/watch?v=", "")
                se.query(task).filter(task.id==id).update({'status': status.error.value})
                print(e.args)

class logger(object):

    def debug(self, msg):
        print(msg)
        #pass

    def warning(self, msg):
        pass

    def error(self, msg):
        se.query(task).filter(task.id==downloader.sid).update({'status': status.error.value})
        print(msg)

class monitor:
    
    @staticmethod
    def check_videos():
        channels = se.query(channel).all()
        for c in channels:   
            body = requests.get("https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&order=date&maxResults=10&type=video".format(config.api_key, c.url))
            print("[Main] Checking "+ c.name)
            videos = json.loads(body.text)['items']
            for i in range(0, len(videos) - 1):
                publish_time = videos[i]['snippet']['publishedAt']
                publish_time_timestamp = datetime.datetime.fromisoformat(publish_time.replace("Z", "+00:00")).timestamp()
                setup_date = datetime.datetime.fromisoformat(config.setup_time).timestamp()
                video_id = videos[i]['id']['videoId']
                # 2020-12-23-20-36-30
                if publish_time_timestamp > setup_date:
                    if se.query(task).filter(task.id == video_id).first() is None:
                        print("[Monitor] A new video from {} is found, adding to the list. ID: {}".format(c.name, video_id))
                        task.add_task(id=video_id)

    @staticmethod
    def download_videos_from_task(value):
        undownloaded_videos = task.get_task_status(value)
        count = 0
        for t in undownloaded_videos:
            url = "https://www.youtube.com/watch?v={}".format(t.get_video_id())
            print("downloading video. id: {} status:{}".format(t.get_video_id(), t.get_video_status()))
            downloader.download(url)
            count += 1
            if len(undownloaded_videos) > 1 and count == len(undownloaded_videos) - 1:
                # in case we submmit videos frequently
                time.sleep(31)
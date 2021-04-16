import youtube_dl
import os
import json
import requests
import datetime
from .database import channel, task, se, status
from .bilibili import bilibili
from PIL import Image
from .config import config

config.read()

class downloader:

    sid = ""

    @classmethod
    def download(self, url):
        if len(url) == 0:
            return

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
                upload_date = info['upload_date']
                uploader = info['uploader']
                id = info['id']

                # ghetto way to implement, i blame youtubedl for shitty formation
                upload_date = upload_date[:4] + '-' + upload_date[4:6] + '-' + upload_date[6:8]
                sid = id

                # https://stackoverflow.com/a/37821542
                img_data = requests.get(thumbnail_url).content
                with open("thumbnail/{}.webp".format(id), "wb") as handler:
                    handler.write(img_data)

                im = Image.open("thumbnail/{}.webp".format(id)).convert("RGB")
                im.save("thumbnail/{}.jpg".format(id), "jpeg")
                print("[Download] All done")

                print("[Upload] Start uploading")
                bilibili.upload("videos/{}.mp4".format(id), title[0:79], url, "thumbnail/{}.jpg".format(id), description, uploader, upload_date)
                se.query(task).filter(task.id==id).update({'status': status.uploaded.value})
                if os.path.exists("videos/{}.mp4".format(id)):
                    os.remove("videos/{}.mp4".format(id))

                if os.path.exists("thumbnail/{}.jpg".format(id)):
                    os.remove("thumbnail/{}.jpg".format(id))

                if os.path.exists("thumbnail/{}.webp".format(id)):
                    os.remove("thumbnail/{}.webp".format(id))
                
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
        if len(config.api_key) == 0:
            print("[Error] API Key is empty. Exiting")
            exit()
        
        '''
        channels = se.query(channel).all()
        for c in channels:   
            body = requests.get("https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&order=date&maxResults=10&type=video".format(config.api_key, c.url))
            print("[Main] Checking "+ c.channel_name)
            videos = json.loads(body.text)['items']
            for i in range(0, len(videos) - 1):
                publish_time = videos[i]['snippet']['publishedAt']
                publish_time_timestamp = datetime.datetime.fromisoformat(publish_time.replace("Z", "+00:00")).timestamp()
                setup_date = datetime.datetime.fromisoformat(config.setup_time).timestamp()
                video_id = videos[i]['id']['videoId']
                # 2020-12-23-20-36-30
                if publish_time_timestamp > setup_date:
                    if se.query(task).filter(task.id == video_id).first() is None:
                        print("[Monitor] A new video from {} is found, adding to the list. ID: {}".format(c.channel_name, video_id))
                        task.add_task(id=video_id)
        '''
    
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

import youtube_dl
import os
import requests
from PIL import Image
from bilibili_api import sync, video_uploader
from .config import config
from .database import se, task, status

class dl_logger(object):
    def debug(self, msg):
        print(msg)
        #pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def remove_stuff(id):
    if os.path.exists(f"videos/{id}.mp4"):
        os.remove(f"videos/{id}.mp4")

    if os.path.exists(f"thumbnail/{id}.jpg"):
        os.remove(f"thumbnail/{id}.jpg")

    if os.path.exists(f"thumbnail/{id}.webp"):
        os.remove(f"thumbnail/{id}.webp")

async def upload(url, title, description, video, thumbnail, video_id):
    credential = video_uploader.VideoUploaderCredential(access_key=config.cookie_access_key)
    
    '''
    {
        "copyright": "int, 投稿类型。1 自制，2 转载。",
        "source": "str, 视频来源。投稿类型为转载时注明来源，为原创时为空。",
        "desc": "str, 视频简介。",
        "desc_format_id": 0,
        "dynamic": "str, 动态信息。",
        "mission_id": "int, 参加活动 ID，若不参加不要提供该项",
        "interactive": 0,
        "open_elec": "int, 是否展示充电信息。1 为是，0 为否。",
        "no_reprint": "int, 显示未经作者授权禁止转载，仅当为原创视频时有效。1 为启用，0 为关闭。",
        "subtitles": {
            "lan": "str: 字幕投稿语言，不清楚作用请将该项设置为空",
            "open": "int: 是否启用字幕投稿，1 or 0"
        },
        "tag": "str, 视频标签。使用英文半角逗号分隔的标签组。示例：标签1,标签2,标签3",
        "tid": "int, 分区ID。可以使用 channel 模块进行查询。",
        "title": "str: 视频标题",
        "up_close_danmaku": "bool, 是否关闭弹幕。",
        "up_close_reply": "bool, 是否关闭评论。",
        "dtime": "int?: 可选，定时发布时间戳（秒）"
    }
    '''

    meta = {
        "copyright": 2,
        "source": url,
        "desc": description[0:config.bilibili_desc_len - 1 - len(url)], # x个字符限制，视频源链接还算进去就挺离谱的，但每个分区的限制长度不一样就更离谱了
        "desc_format_id": 0,
        "dynamic": "",
        "interactive": 0,
        "open_elec": 1,
        "no_reprint": 1,
        "subtitles": {
            "lan": "",
            "open": 0
        },
        "tag": config.bilibili_tag,
        "tid": config.bilibili_tid,
        "title": title,
        "up_close_danmaku": False,
        "up_close_reply": False
    }

    # 所有分区的视频标题应该都是80个字符吧..?
    page = video_uploader.VideoUploaderPage(video_stream=open(video, "rb"), title=title[0:79], description=description)
    uploader = video_uploader.VideoUploader([page], meta, credential, threads=1, cover_stream=open(thumbnail, "rb"))

    @uploader.on("__ALL__")
    async def event(data):
        print(data)

    await uploader.start()

def download(url):
    if len(url) == 0:
        return

    if not os.path.exists("videos"):
        os.mkdir("videos")

    if not os.path.exists("thumbnail"):
        os.mkdir("thumbnail")

    options = {
        'format': "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        'forcethumbnail': False,
        'forcetitle': False,
        'forcedescription': False,
        'logger': dl_logger(),
        'outtmpl': u'videos/%(id)s.%(ext)s',
    }

    print("[-] Downloading video")

    with youtube_dl.YoutubeDL(options) as dl:
        try:
            dl.cache.remove()
            info = dl.extract_info(url, download=True)
            title = info['title']
            thumbnail_url = info['thumbnail']
            description = info['description']
            #upload_date = info['upload_date']
            #uploader = info['uploader']
            id = info['id']

            # TODO: 放在简介里？
            #upload_date = upload_date[:4] + '-' + upload_date[4:6] + '-' + upload_date[6:8]
            # https://stackoverflow.com/a/37821542
            img_data = requests.get(thumbnail_url).content
            with open(f"thumbnail/{id}.webp", "wb") as handler:
                handler.write(img_data)

            im = Image.open(f"thumbnail/{id}.webp").convert("RGB")
            im.save(f"thumbnail/{id}.jpg", "jpeg")
            print("[+] Finished downloading")

            print("[-] Uploading")
            sync(upload(url=url, title=title, description=description, video=f"videos/{id}.mp4", thumbnail=f"thumbnail/{id}.jpg", video_id=id))
            se.query(task).filter(task.id == id).update({"status": status.uploaded.value})
            print("[+] Successfully uploaded")
            remove_stuff(id)
        except Exception as e:
            error_msg = e.__str__()
            if error_msg.find("代码：21012") != -1: #消息：请不要反复提交相同标题的稿件（虽然我觉得不会有就是了...
                se.query(task).filter(task.id == id).update({"status": status.uploaded.value})
                remove_stuff(id)
            else:
                se.query(task).filter(task.id == id).update({"status": status.error.value})
            print(e)

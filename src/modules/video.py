import youtube_dl
import os
import requests
from PIL import Image
from bilibili_api import sync, video_uploader, Credential
from .config import config
from .database import se, task, status, channel, channel_type

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

async def upload(url, title, description, video, thumbnail, description_length, tags, category_id):
    credential = Credential(sessdata=config.cookie_sessdata, bili_jct=config.cookie_jct)

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
        "desc": description[0:description_length - len(url)], # x个字符限制，视频源链接还算进去就挺离谱的，但每个分区的限制长度不一样就更离谱了
        "desc_format_id": 0,
        "dynamic": "",
        "interactive": 0,
        "open_elec": 1,
        "no_reprint": 1,
        "subtitles": {
            "lan": "",
            "open": 0
        },
        "tag": tags,
        "tid": category_id,
        "title": title,
        "up_close_danmaku": False,
        "up_close_reply": False
    }

    # 所有分区的视频标题应该都是80个字符吧..?
    page = video_uploader.VideoUploaderPage(path=video, title=title[0:80], description=description)
    uploader = video_uploader.VideoUploader([page], meta, credential, cover_path=thumbnail)

    @uploader.on("__ALL__")
    async def event(data):
        print(data)

    await uploader.start()

def download(url, id_src, database=True):
    if len(url) == 0:
        return

    if database == True:
        if se.query(task).filter(task.id==id_src).first() is None:
            print(f"[-] {id_src} is not in database, adding.")
            task.add_task(id=id_src)

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

    print("[-] 开始下载视频及相关信息")

    with youtube_dl.YoutubeDL(options) as dl:
        try:
            dl.cache.remove()
            info = dl.extract_info(url, download=True)
            #print(info)
            title = info['title']
            thumbnail_url = info['thumbnail']
            description = info['description']
            channel_id = info['channel_url'].replace("https://www.youtube.com/channel/", "")
            video_id = info['id']

            if config.bilibili_video_info == True:
                upload_date = info['upload_date']
                upload_date = upload_date[:4] + '-' + upload_date[4:6] + '-' + upload_date[6:8]
                uploader = info['uploader']
                description = "频道:" + uploader + " 日期:" + upload_date + "\n" + description

            img_data = requests.get(thumbnail_url).content
            with open(f"thumbnail/{video_id}.webp", "wb") as handler:
                handler.write(img_data)

            im = Image.open(f"thumbnail/{video_id}.webp").convert("RGB")
            im.save(f"thumbnail/{video_id}.jpg", "jpeg")
            print("[+] 下载部分已完成")

            tags = config.bilibili_tag
            category_id = config.bilibili_tid
            description_length = config.bilibili_desc_len

            if database == True:
                print("[-] 获取频道信息中")
                query_result = se.query(channel).filter(channel.channel_id == channel_id).first()
                if query_result is not None:
                    t = query_result.type
                    type_info = se.query(channel_type).filter(channel_type.row_ == t).first()
                    if type_info is not None:
                        tags = type_info.tag
                        category_id = type_info.category_id
                        description_length = type_info.description_length
                    else:
                        raise Exception("找到了频道但找不到对应的类型，请更新表")
                else:
                    print("[-] 无法从数据库里获取频道信息，使用配置文件里的上传信息（分区，标签，简介长度）")

            print("[-] 上传中")
            sync(upload(url=url, title=title, description=description, video=f"videos/{video_id}.mp4", thumbnail=f"thumbnail/{video_id}.jpg", tags=tags, category_id=category_id, description_length=description_length))
            if database == True:
                se.query(task).filter(task.id == video_id).update({"status": status.uploaded.value})

            print("[+] 上传成功")
            remove_stuff(video_id)
        except Exception as e:
            error_msg = e.__str__()
            if database == True:
                if error_msg.find("代码：21012") != -1: #消息：请不要反复提交相同标题的稿件（虽然我觉得不会有就是了...
                    se.query(task).filter(task.id == video_id).update({"status": status.uploaded.value})
                    remove_stuff(video_id)
                else:
                    se.query(task).filter(task.id == video_id).update({"status": status.error.value})
            print("[!] 上传失败 原因：" + error_msg)

from .config import config
from bilibili_api import Verify
from bilibili_api import user
from bilibili_api import video
from bilibili_api import channel

config.read()

class bilibili:
    
    def upload(video_path, title, source_link, thumbnail_path, description, uploader, upload_date):
        verify = Verify(config.cookie_sessdata, config.cookie_jct)
        print(video_path)
        print(thumbnail_path)
        try:
            video_file = video.video_upload(path=video_path, verify=verify)
            print("[Upload] Uploaded video file successfully.")
        except Exception as e:
            raise(Exception(f"[Upload] Failed to upload video file. Make sure the video file exists / the connection to bilibili is available / bili_jct is valid. Reason:{e.args}"))
            return

        try:
            thumbnail_file = video.video_cover_upload(path=thumbnail_path, verify=verify)
            print("[Upload] Uploaded thubmnail successfully.")
        except Exception as e:
            raise(Exception("[Upload] Failed to upload thubmnail. Make sure the thubmnail file exists / the connection to bilibili is available / bili_jct is valid"))
            return

        description = "频道: {} 上传日期:{}\n".format(uploader, upload_date) + description

        data = {
            "copyright": 2,
            "source": source_link,
            "cover": thumbnail_file,
            "desc": description[0:1999-len(source_link)],
            "desc_format_id": 0,
            "dynamic": "",
            "interactive": 0,
            "no_reprint": 1,
            "subtitles": {
                "lan": "语言",
                "open": 0
            },
            "tag": config.bilibili_tag,
            "tid": config.bilibili_tid,
            "title": title,
            "videos": [
                {
                    "desc": "",
                    "filename": video_file,
                    "title": "1"
                }
            ]
        }
            
        print("[Upload] Submitting")
        try:
            result = video.video_submit(data, verify)
            print("[Upload] Submitted")
        except Exception as e:
            raise Exception(e.args.__str__())

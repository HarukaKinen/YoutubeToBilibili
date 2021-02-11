from config import config
from bilibili_api import Verify
from bilibili_api import user
from bilibili_api import video
from bilibili_api import channel

config.read()

class bilibili:
    
    def upload(video_path, title, source_link, thumbnail_path, description, uploader, upload_date):
        verify = Verify(config.cookie_sessdata, config.cookie_jct)
        try:
            video_file = video.video_upload(video_path, verify=verify)
            print("[Upload] Uploaded video file successfully.")
        except Exception as e:
            raise("[Upload] Failed to upload video file. Make sure the video file exists or the connection to bilibili is available")
            return

        try:
            thumbnail_file = video.video_cover_upload(thumbnail_path, verify=verify)
            print("[Upload] Uploaded thubmnail successfully.")
        except Exception as e:
            raise("[Upload] Failed to upload thubmnail. Make sure the video file exists or the connection to bilibili is available")
            return

        data = {
            "copyright": 2,
            "source": source_link,
            "cover": thumbnail_file,
            "desc": "视频作者: {} 视频上传日期:{}\n".format(uploader, upload_date) + description,
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

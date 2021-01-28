from config import config
from bilibili_api import Verify
from bilibili_api import user
from bilibili_api import video
from bilibili_api import channel

config.read()

class bilibili:
    
    def upload(video_path, title, source_link, thumbnail_path, description):
        try:
            verify = Verify(config.cookie_sessdata, config.cookie_jct)
            video_file = video.video_upload(video_path, verify=verify)
            print("[Upload] Uploaded video file successfully.")

            thumbnail_file = video.video_cover_upload(thumbnail_path, verify=verify)
            print("[Upload] Uploaded thubmnail successfully.")

            data = {
                "copyright": 2,
                "source": source_link,
                "cover": thumbnail_file,
                "desc": "本视频由python搬运上传,有能力还请支持原作者.\n" + description,
                "desc_format_id": 0,
                "dynamic": "",
                "interactive": 0,
                "no_reprint": 1,
                "subtitles": {
                    "lan": "语言",
                    "open": 0
                },
                "tag": "标签改这里,多个标签使用英文半角逗号隔开",
                "tid": 17,
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
            result = video.video_submit(data, verify)
            print(result)
        except Exception as e:
            print(e.args)
                
# YoutubeToBilibili
一个自动搬运youtube视频到哔哩哔哩的python脚本

# 使用前注意事项

**注意：仅在python3.8.6环境下测试过，其他版本需要自己摸索**

 1. 所需依赖项
    - pillow
    - bilibili_api
    - youtube-dl
    - mysql-connector
    - sqlalchemy

2. 更改 ``config.ini`` 里的配置文件
    - ``sessdata`` 与 ``bili_jct`` 的获取方法[看这里](https://github.com/Passkou/bilibili_api#获取-sessdate-和csrf)
    - Youtube API 密钥的获取方法[看这里](https://developers.google.com/youtube/v3/getting-started)
    - 数据库表结构可以参考 ``database.py`` 进行创建或导入 [db.sql](https://github.com/deadw1nter/YoutubeToBilibili/blob/master/db.sql)
    - （可选）更改 ``setup_time`` 以过滤在指定日期前上传的视频

3. 根据[文档](https://github.com/Passkou/bilibili_api/blob/master/docs/模块/video.md#上传视频)对 ``bilibili.py`` 里的 ``data`` 进行更改

3. 设置代理
    - 在 ``youtube.py`` 中找到 ``download`` 这一method, 往 ``option`` 里添加 [proxy](https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L211)

4. 确保有安装 [ffmpeg](https://ffmpeg.org/download.html)
    - Windows 用户可能即使安装了也会出错，这时候需要把相应的 ``.exe`` 文件放在 ``python安装路径/Scripts`` 目录下
    - Linux 用户可通过自己的 package manager 进行安装

# 感谢

* [Freak](https://github.com/Fre-ak) - 为我写该脚本时所提供的帮助
* Revolution - 在数据结构上的指点
* [Passkou](https://github.com/Passkou) - 集成b站的api
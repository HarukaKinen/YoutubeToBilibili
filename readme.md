# YoutubeToBilibili
一个自动搬运youtube视频到哔哩哔哩的python脚本

# 使用前注意事项
**注意：仅在python3.8.6环境下测试过，其他版本需要自己摸索**

1. 使用 `` pip install -r requirements.txt`` 安装依赖项

2. 更改 ``config.ini`` 里的配置文件
    - ``sessdata`` 与 ``bili_jct`` 的获取方法[看这里](https://github.com/Passkou/bilibili_api#获取-sessdate-和csrf)
    - Youtube API 密钥的获取方法[看这里](https://developers.google.com/youtube/v3/getting-started)
    - 数据库表结构可以参考 ``database.py`` 进行创建或导入 [db.sql](https://github.com/deadw1nter/YoutubeToBilibili/blob/master/db.sql)
    - （可选）更改 ``setup_time`` 以过滤在指定日期前上传的视频
    - 更改 ``tid`` 以指定上传视频的分区
    - 更改 ``tag`` 以指定上传视频的标签
    - 更改 ``callback_server`` 的值 如: ``https://deadwinter.cc/feed/``( 要带``/feed/``, 不带的话改一下源码也行 )

3. 设置代理
    - 在 ``youtube.py`` 中找到 ``download`` 这一method, 往 ``option`` 里添加 [proxy](https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L211)

4. 确保有安装 [ffmpeg](https://ffmpeg.org/download.html)
    - Windows 用户可能即使安装了也会出错，这时候需要把相应的 ``.exe`` 文件放在 ``python安装路径/Scripts`` 目录下
    - Linux 用户可通过自己的 package manager 进行安装

5. 确保 ``config.ini`` 中的 ``cookie`` 是最新的
    - B站的cookie似乎每3个月就会变一次（如果有错请指出），所以最好每3个月检查更新一次 

# 关于订阅服务器

由于我自己是本地使用所以我用 [ngrok](https://ngrok.com/) 把内网暴露给外网

# 文件解释
- ``app.py`` 管理订阅服务器
- ``main.py`` 检查是否有新视频 有则下载
- ``download.py`` 下载上次任务 未下载/出错 的视频
- ``download_schedule.py`` 每5分钟试图下载并上传未上传成功的视频
- ``manually_download.py`` 下载指定链接的视频
- ``subscribe_channel.py`` 订阅频道

# 关于PR
由于我自己对 python 不太熟悉，如果觉得代码有改进的地方可以提交PR

# 感谢

* [Freak](https://github.com/Fre-ak) - 为我写该脚本时所提供的帮助
* Revolution - 在数据结构上的指点
* [Passkou](https://github.com/Passkou) - 集成b站的api
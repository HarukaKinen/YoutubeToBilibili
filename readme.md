# YoutubeToBilibili
一个自动搬运youtube视频到哔哩哔哩的python脚本

# 使用前注意事项
**注意：仅在python3.8.6环境下测试过，其他版本需要自己摸索**

**由于使用了bilibili_api库，如果出现无法使用的情况请回滚到8.1.0版本** 

1. 使用 ``pip install -r requirements.txt --upgrade`` 安装依赖项

2. 更改 ``config.ini`` 里的配置文件
    - ``sessdata`` 与 ``bili_jct`` 的获取方法[看这里](https://github.com/Passkou/bilibili_api#获取-sessdate-和csrf)   
    - 数据库表结构可以参考 ``database.py`` 进行创建或输入以下指令创建
        ```
        create database youtube_video character set utf8mb4 collate utf8mb4_unicode_ci;

        use youtube_video;

        create table channel (channel_id varchar(255), subscribe_mode varchar(255), primary key(channel_id));

        create table task (id varchar(255), status int, primary key(id));
        ```
    - 更改 ``tid`` 以指定上传视频的分区
    - 更改 ``tag`` 以指定上传视频的标签
    - 如果需要使用订阅服务器的话，更改 ``callback_server`` 的值

3. 确保有安装 [ffmpeg](https://ffmpeg.org/download.html)
    - Windows 用户可能即使安装了也会出错，这时候需要把相应的 ``.exe`` 文件放在 ``python安装路径/Scripts`` 目录下
    - Linux 用户可通过自己的 package manager 进行安装

4. 确保 ``config.ini`` 中的 ``cookie`` 是最新的
 
# 关于订阅服务器
由于我自己是本地使用所以我用 [ngrok](https://ngrok.com/) 把内网暴露给外网

# 感谢

* [Freak](https://github.com/Fre-ak) - 为我写该脚本时所提供的帮助
* Revolution - 在数据结构上的指点
* [MoyuScript](https://github.com/MoyuScript) - 集成b站的api

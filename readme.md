# YoutubeToBilibili
一个自动搬运youtube视频到哔哩哔哩的python脚本

# 声明
如果遇到不能用的情况请自行排查, 请勿跟图下这个人一样到别的repository开无关issue. 目前脚本可以正常运行(2022-04-26 12:32 UTC+8)

![不要当这个人](https://i.imgur.com/uNhrUPC.png)
![不要当这个人](https://i.imgur.com/TQK6FHF.png)

# 使用前注意事项

**请在 config.ini 的所在目录下运行py文件**

1. 使用 ``pip install -r requirements.txt --upgrade`` 安装依赖项

2. 更改 ``config.ini`` 里的配置文件
    - ``sessdata`` 与 ``bili_jct`` 的获取方法[看这里](https://github.com/Passkou/bilibili_api#获取-sessdate-和csrf)  
    - 如果你想通过数据库来管理视频请看下面 
        - 数据库表结构可以参考 ``database.py`` 进行创建 或 在连接到数据库服务器后，输入以下指令进行创建
            ```
            create database youtube_video character set utf8mb4 collate utf8mb4_unicode_ci;

            use youtube_video;

            create table channel (channel_id varchar(255), subscribe_mode varchar(255), type int, primary key(channel_id));

            create table task (id varchar(255), status int, primary key(id));

            create table channel_type (row_ int not null auto_increment, tag varchar(255), category_id int not null, description_length int not null, primary key(row_)); 
            
            如果已经有channel这个表则输入这个指令:
            alter table channel add type int;
            ```
        - 更改 ``tid`` 以指定上传视频的分区
        - 更改 ``tag`` 以指定上传视频的标签
        - 更改 ``desc_len`` 以指定简介最大长度（这个怪b站，因为每个分区的简介长度都不一样）
        - 同时在数据库里给 ``channel_type`` 插入数据，以指定上传时的信息（如果有则优先用数据库里的）
        - 如果需要使用订阅服务器的话，更改 ``callback_server`` 的值
    - 如果你只想手动用脚本完成下载上传就用 [src/manually_dl.py](https://github.com/HorizonKinen/YoutubeToBilibili/blob/master/src/manually_dl.py)，如果需要数据库管理则加 ``--db 或 -d (比如python3 src/manually_dl.py -d）``

3. 确保有安装 [ffmpeg](https://ffmpeg.org/download.html)
    - Windows 用户可能即使安装了也会出错，这时候需要把相应的 ``.exe`` 文件放在 ``python安装路径/Scripts`` 目录下
    - Linux 用户可通过自己的 package manager 进行安装

4. 确保 ``config.ini`` 中的 ``cookie`` 是最新的
 
# 关于订阅服务器
由于我自己是本地使用所以我用 [ngrok](https://ngrok.com/) 把内网暴露给外网，你也可以把订阅服务器架设在服务器上之类的（反正只是拿一个订阅信息，国内服务器应该不会被gfw拦截吧..)


# 感谢

* [Freak](https://github.com/Fre-ak) - 为我写该脚本时所提供的帮助
* Revolution - 在数据结构上的指点
* [MoyuScript](https://github.com/MoyuScript) - 集成b站的api

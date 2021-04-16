import feedparser
from flask import Flask
from flask import request

from basic_modules.youtube import downloader
from basic_modules.config import config
from flask_stuffs.database import db, channel, tasks

config.read()

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}:3306/{}'.format(config.database_user, config.database_password, config.database_host, config.database_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/feed/", methods=['GET', 'POST'])
def feed():
    if request.method == 'POST':
        feed = feedparser.parse(request.get_data(parse_form_data=True))
        if feed:
            print('[-] Successfully parsed feed.')
            for data in feed['entries']:
                video_id = data['yt_videoid']
                if tasks.query.filter(tasks.id == video_id).first() is None:
                    print(f"[!] Failed to find video id {video_id} in database, adding.")
                    db.session.add(tasks(id=video_id))
                    db.session.commit()
                '''
                # Note: aabandoned due to multithreading thing, please make a pr if you know how to fix
                    downloader.download(data["link"])
                elif se.query(task).filter(task.id==video_id).filter(task.status != status.uploaded.value):
                    print(f"[-] Found video id '{video_id}' in database, but it was failed to download / upload, trying to download and upload it again")
                    downloader.download(data["link"])
                #print("[-] Link: ", data["link"])
                '''

    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        mode = request.args.get('hub.mode')
        topic = request.args.get('hub.topic')

        if challenge and topic and mode:
            id = topic[-24:]
            query = channel.query.filter(channel.channel_id == id).first()

            if query is None:
                if  mode == 'subscribe':
                    print(f"[!] Failed to find channel id {id} in database, adding.")
                    db.session.add(channel(channel_id=id, subscribe_mode=mode))
                    db.session.commit()
            else:
                if mode == 'unsubscribe':
                    print(f"[!] Unsubscribe mode was found, deleting channel id {id} from database.")
                    db.session.delete(query)
                    db.session.commit()

            # returning challenge for authorization
            return challenge

    return '', 204

app.run()
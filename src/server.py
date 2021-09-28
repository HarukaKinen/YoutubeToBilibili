import feedparser
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from modules.config import config

config.read()

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}:3306/{}'.format(config.database_user, config.database_password, config.database_host, config.database_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

class channel(db.Model):
    channel_id = db.Column(db.String(255), primary_key=True)
    subscribe_mode = db.Column(db.String(255))

class tasks(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    status = db.Column(db.Integer, default=1)

db.init_app(app)
db.create_all(app=app)

@app.route("/feed/", methods=['GET', 'POST'])
def feed():
    if request.method == 'POST':
        feed = feedparser.parse(request.get_data(parse_form_data=True))
        if feed:
            print('[-] Successfully parsed video feed.')
            for data in feed['entries']:
                video_id = data['yt_videoid']
                if tasks.query.filter(tasks.id == video_id).first() is None:
                    print(f"[!] Failed to find video id {video_id} in database, adding.")
                    db.session.add(tasks(id=video_id))
                    db.session.commit()

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
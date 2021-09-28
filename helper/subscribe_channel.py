import argparse
import requests
import configparser


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--id", help="channel id to subscribe")
parser.add_argument("-u", "--unsubscribe", help="unsubscribe this channel", action="store_true")
parser.add_argument("-ls", "--lease_seconds", help="time of subscribing a channel in second, 5 days if empty", action="count")

args = parser.parse_args()

if args.id is None:
    print("[!] channel id cannot be empty.")
    exit()

mode = "subscribe"
if args.unsubscribe:
    mode = "unsubscribe"

if args.lease_seconds is None:
    args.lease_seconds = 60*60*24*5

def setup_subscription(callback_server, channel_id, mode, lease_seconds: int):
    r = requests.post('https://pubsubhubbub.appspot.com/subscribe', data={
        'hub.mode': mode,
        'hub.topic': 'https://www.youtube.com/xml/feeds/videos.xml?channel_id={}'.format(channel_id),
        'hub.callback': callback_server,
        "hub.lease_seconds": lease_seconds,
        "hub.verify": 'async',
    }, headers={"content-type": "application/x-www-form-urlencoded"})
    return r.status_code

config = configparser.RawConfigParser()
config.read("config.ini", encoding="utf-8")
callback_server = config.get("server", "callback_server")

code = setup_subscription(callback_server, args.id, mode, args.lease_seconds)

if code in range(200, 204):
    print(f"[+] Successfully {mode}d the channel")
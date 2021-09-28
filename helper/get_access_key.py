from bilibili_api import sync, video_uploader

print("acc:")
acc = input()
print("pw:")
pw = input()

credential = video_uploader.VideoUploaderCredential(account=acc, password=pw)
print(sync(credential.get_access_key()))
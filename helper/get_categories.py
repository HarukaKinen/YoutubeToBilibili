from bilibili_api import channel

print("输入分区id")
tid = input()
print(channel.get_channel_info_by_tid(int(tid)))

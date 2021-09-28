import asyncio
from bilibili_api import video
from bilibili_api import aid2bvid

async def main():
    # 实例化 Video 类
    print("输入bv号")
    video_id = input()

    v = video.Video(bvid=video_id)
    # 获取信息
    info = await v.get_info()
    # 打印信息
    print(f"分区ID: {info['tid']} - 分区名字: {info['tname']}")

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
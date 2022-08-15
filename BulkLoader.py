import asyncio
import threading
import time

from config import VK_API_KEY
import vk_api

api_session = vk_api.VkApi(token=VK_API_KEY)

upload_session = vk_api.upload.VkUpload(api_session)

photos = ['photos/1.jpg'] * 100


def upload():
    upload_session.photo(photos=photos,
                         album_id=284573738,
                         caption='⛈')


for _ in range(100):
    threads = [threading.Thread(target=upload) for _ in range(30)]
    print('# run')
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('# end')
    time.sleep(1)

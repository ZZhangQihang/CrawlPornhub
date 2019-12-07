import json
import logging
import os
import random
import sys
import time
from threading import Thread, Event, currentThread
from pornhubSpider.settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, REDIS_KEY
from redis import StrictRedis
import requests
from tqdm import tqdm


class DownloadsVideo(object):

    def __init__(self):
        pass

    def down_from_url(self, url, dst):
        response = requests.get(url, stream=True)  # (1)
        file_size = int(response.headers['content-length'])  # (2)
        if os.path.exists(dst):
            first_byte = os.path.getsize(dst)  # (3)
        else:
            first_byte = 0
        if first_byte >= file_size:  # (4)
            return file_size

        header = {"Range": "bytes={first_byte}-{file_size}".format(first_byte=first_byte, file_size=file_size)}

        pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=dst)
        req = requests.get(url, headers=header, stream=True)
        with open(dst, 'ab') as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        pbar.close()
        return file_size

    def run(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s: %(message)s')
        logging.info("Thread:{} started".format(currentThread().getName()))
        conn = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
        count = 0
        while True:
            if not conn.exists(REDIS_KEY):
                if count > 3:
                    break
                logging.info("Thread:{} Listening on key:{}, No message currently".format(currentThread().getName(), REDIS_KEY))
                time.sleep(random.randint(8, 10))
                count += 1
                continue
            data_json = conn.rpop(REDIS_KEY)
            try:
                data_json = json.loads(data_json.decode())
            except AttributeError as e:
                if count > 3:
                    break
                logging.info("Thread:{} Listening on key:{}, No message currently".format(currentThread().getName(), REDIS_KEY))
                time.sleep(random.randint(8, 10))
                count += 1
                continue
            self.down_from_url(data_json['seed_url'], data_json['title'].replace('.', ' ')+'.mp4')


if __name__ == '__main__':
    sentinel = Event()
    sentinel.set()
    dv = DownloadsVideo()
    thread_li = []
    for i in range(5):
        t = Thread(target=dv.run)
        t.start()
        thread_li.append(t)
    for thread in thread_li:
        thread.join()
    logging.info("Download video finish, All threads close")
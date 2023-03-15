import asyncio
import json
import numpy as np
import os
import time
from threading import Thread
from tqdm import tqdm

import aiohttp
import cv2


apps = []
removed = 0


def filter(single_block=False):
    global apps

    temp_apps = []

    for file_name in tqdm(os.listdir("gplay"), desc="Loading files"):
        if "example" in file_name:
            continue

        if "images" in file_name:
            continue

        with open('gplay/' + file_name, encoding="utf-8") as f:
            temp_apps += json.load(f)

            if single_block:
                break

    for entry in temp_apps:
        entry["images"] = []

    def filter_games(temp_apps):
        return_list = []

        for app in tqdm(temp_apps, desc="Filtering apps"):
            if "GAME" in app["genreId"]:
                return_list.append(app)
        
        return return_list

    temp_apps = filter_games(temp_apps)

    apps = temp_apps


def print_start():
    total = 0

    for app in apps:
        total += len(app['screenshots'])

    print(f'Downloading {total} screenshots from {len(apps)} apps. Average {total / len(apps)} per app.')


async def save_image(session, app, screenshot, j):

    file_name = app['appId'] + '_' + str(j) + '.png'

    app['images'].append(file_name)

    async with session.get(screenshot) as resp:
        with open('gplay/images/' + file_name, 'wb') as f:
            f.write(await resp.read())


async def main():
    async with aiohttp.ClientSession() as session:
        chunk_size = 100

        for i in tqdm(range(0, len(apps), chunk_size), desc="Downloading images"):
            tasks = []

            for app in apps[i:i+chunk_size]:
                for j, screenshot in enumerate(app['screenshots']):
                    tasks.append(asyncio.create_task(save_image(session, app, screenshot, j)))

            await asyncio.gather(*tasks)


def verify(start_index, end_index):
    global apps

    for app in apps[start_index:end_index]:
        for image_id in range(len(app['images']) - 1, -1, -1):
            file_name = app['images'][image_id]

            try:
                img = cv2.imread('gplay/images/' + file_name, cv2.IMREAD_COLOR)
                if img is None:
                    raise Exception('Image is None')
                cv2.imwrite('gplay/images/' + file_name, img)
            except:
                print(f'Image {file_name} is corrupt. Removing.')
                os.remove('gplay/images/' + file_name)
                app['images'].pop(image_id)


def remove_duplicates(start_index, end_index):
    global apps, removed

    loc_removed = 0

    for _, app in enumerate(apps[start_index:end_index]):
        images = {}

        for image_id in range(len(app['images'])):
            images[image_id] = cv2.imread('gplay/images/' + app['images'][image_id])

        image_len = len(images)

        for image_id in range(image_len):
            if image_id not in images:
                continue
            image1 = images[image_id]

            for other_id in range(image_len - 1, image_id, -1):
                if other_id not in images:
                    continue
                image2 = images[other_id]

                if np.array_equal(image1, image2):
                    loc_removed += 1
                    os.remove('gplay/images/' + app['images'][other_id])
                    images.pop(other_id)

        for image_id in range(len(app['images']) - 1, -1, -1):
            if image_id not in images:
                app['images'].pop(image_id)

    removed += loc_removed


def remove_empty():
    global apps

    for app_id in range(len(apps) - 1, -1, -1):
        if len(apps[app_id]['images']) == 0:
            apps.pop(app_id)


def save_json():
    with open('gplay/apps.json', 'w', encoding="utf-8") as f:
        json.dump(apps, f, indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    start_time = time.time()

    filter()
    print_start()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

    thread_count = 32
    threads = []

    for i in range(thread_count):
        threads.append(Thread(target=verify, args=(i * len(apps) // thread_count, (i + 1) * len(apps) // thread_count)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    threads = []

    for i in range(thread_count):
        threads.append(Thread(target=remove_duplicates, args=(i * len(apps) // thread_count, (i + 1) * len(apps) // thread_count)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f'Removed {removed} duplicates.')

    remove_empty()
    save_json()

    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")

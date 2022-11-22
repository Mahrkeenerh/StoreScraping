import asyncio
import json
import time

import aiohttp


apps = []


def print_start():
    total = 0

    for app in apps:
        total += len(app['screenshots'])

    print(f'Downloading {total} screenshots from {len(apps)} apps. Average {total / len(apps)} per app.')


async def save_image(session, app, screenshot, j):
    async with session.get(screenshot) as resp:
        with open('gplay/images/' + app['appId'] + '_' + str(j) + '.png', 'wb') as f:
            f.write(await resp.read())


async def main():
    start_time = time.time()
    print(f'0/{len(apps)} apps done. 0.00%')

    async with aiohttp.ClientSession() as session:
        chunk_size = 100

        for i in range(0, len(apps), chunk_size):
            tasks = []

            for app in apps[i:i+chunk_size]:
                for j, screenshot in enumerate(app['screenshots']):
                    tasks.append(asyncio.create_task(save_image(session, app, screenshot, j)))

            await asyncio.gather(*tasks)

            eta = (time.time() - start_time) / (i + chunk_size) * (len(apps) - i - chunk_size)
            print(f'\033[F{i+chunk_size}/{len(apps)} apps done. '
                f'{round((i+chunk_size) / len(apps) * 100, 2)}% ETA {eta}s\033[K')


if __name__ == '__main__':
    with open('gplay/apps_0.json', encoding="utf-8") as f:
        apps = json.load(f)

    print_start()

    start_time = time.time()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

    end_time = time.time()

    print(f"Time: {end_time - start_time} seconds")

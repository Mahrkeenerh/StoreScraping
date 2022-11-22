import json
import os
import time

import PIL
from PIL import Image


screenshots = 0

with open("gplay/apps_0.json", encoding="utf-8") as f:
    apps = json.load(f)

for app in apps:
    screenshots += len(app["screenshots"])

print(f'Apps: {len(apps)} | Screenshots: {screenshots} | Average: {screenshots / len(apps)}')
print(f'Real: {len(os.listdir("gplay/images"))}')


total_screenshots = 0
total_apps = 0

for batch in os.listdir("gplay"):
    if "examples" in batch or "images" in batch:
        continue

    with open(f"gplay/{batch}", encoding="utf-8") as f:
        apps = json.load(f)
    
    total_apps += len(apps)
    
    for app in apps:
        total_screenshots += len(app["screenshots"])

print(f'Total apps: {total_apps} | Total screenshots: {total_screenshots} | Average: {total_screenshots / total_apps}')

exit()


# Analyze images
min_x = 10000
min_y = 10000
max_x = 0
max_y = 0
avg_x = 0
avg_y = 0

start_time = time.time()

print(f'0/{screenshots} screenshots done. 0.00%')

for i, image in enumerate(os.listdir("gplay/images")):
    try:
        with Image.open(f"gplay/images/{image}") as img:
            x, y = img.size

            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

            avg_x += x
            avg_y += y

        if i % 100 == 0:
            eta = (time.time() - start_time) / (i + 100) * (screenshots - i - 100)
            print(f'\033[F{i+100}/{screenshots} screenshots done. '
                f'{round((i+100) / screenshots * 100, 2)}% ETA {eta}s\033[K')

    except PIL.UnidentifiedImageError:
        print(f"Error: {image}\n")
        os.remove(f"gplay/images/{image}")

avg_x /= len(os.listdir("gplay/images"))
avg_y /= len(os.listdir("gplay/images"))

print(f'Minimum: {min_x}x{min_y} | Maximum: {max_x}x{max_y} | Average: {avg_x}x{avg_y}')
print(f'Time: {time.time() - start_time} seconds')

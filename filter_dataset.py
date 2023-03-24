import json
import os

dataset_path = r"D:\Datasets\Games"

with open(os.path.join(dataset_path, "apps.json"), encoding="utf-8") as f:
    apps = json.load(f)


def filter(downloads, rating):
    global apps

    filtered_apps = []

    for app in apps:
        if app["minInstalls"] is not None and app["minInstalls"] > downloads:
            filtered_apps.append(app)

    apps = filtered_apps

    filtered_apps = []

    for app in apps:
        try:
            if app["score"] is not None and app["score"] > rating:
                filtered_apps.append(app)
        except KeyError:
            pass

    apps = filtered_apps


if __name__ == "__main__":
    filter(10000, 4)
    
    with open(os.path.join(dataset_path, "apps_filtered.json"), "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=4, sort_keys=True, ensure_ascii=False)

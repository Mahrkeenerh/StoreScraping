import json
import os
from tqdm import tqdm

import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector


dataset_path = r"/home/xbuban1/Games"

with open(os.path.join(dataset_path, "apps_filtered.json"), encoding="utf-8") as f:
    apps = json.load(f)


def filter(downloads, rating):
    global apps

    filtered_apps = []

    for app in apps:
        if app["minInstalls"] is not None and app["minInstalls"] > downloads:
            filtered_apps.append(app)

    apps = filtered_apps

    filtered_apps = []

    for app in tqdm(apps, desc="Filtering Rating"):
        try:
            if app["score"] is not None and app["score"] > rating:
                filtered_apps.append(app)
        except KeyError:
            pass

    apps = filtered_apps

    print(f"Filtered {len(apps)} apps")


def filter_english():
    global apps

    def get_lang_detector(nlp, name):
        return LanguageDetector()

    nlp = spacy.load("en_core_web_sm")
    Language.factory("language_detector", func=get_lang_detector)
    nlp.add_pipe('language_detector', last=True)

    filtered_apps = []

    for app in tqdm(apps, desc="Filtering English"):
        doc = nlp(app["description"])

        if doc._.language["language"] == "en":
            filtered_apps.append(app)

    apps = filtered_apps

    print(f"Filtered {len(apps)} apps")


if __name__ == "__main__":
    # filter(500000, 4.4)
    filter_english()

    with open(os.path.join(dataset_path, "apps_filtered_en.json"), "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=4, sort_keys=True, ensure_ascii=False)

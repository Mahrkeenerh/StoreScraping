# Google Play store

## Getting apps
First general scrape, searching by individual categories and collections yields about **50k unique app** results, made by **30k unique developers**. This took **35 seconds**.

Second by-developer scrape adds another **138k unique app** results, for a total of **188k applications**.
This task was performed in chunks of 250 requests, to ensure highest possible throughput, while trying to minimize server load, and took **11 minutes and 40 seconds**.

Third by-app scrape is used to get specific application information, their preview images, and other useful information. Nested chunking is required, otherwise **out of memory error** occurs. First chunking splits all apps into blocks of **10k ids**, which are saved at the end in a single file, with the chunk id. Then, second nested chunking, with size of 250 requests, is used, which takes **43 minutes and 40 seconds**.


## Preview images
First batch was downloaded to analyze the time and size requirements. This batch consists of **10k apps** with **111k images**, that is on average **11 images** per app. All of the images were successfully downloaded, with only 3 being corrupted.

Alltogether, it took about **20 minutes** to download these images, and they take up about **9 GiB** of space.

Minimal x, y resolution is **223 pixels**, maximal x, y resolution is **512 pixels**, and the average resolution is **346 x 471 pixels**. This analysis was done independently for x and y.

These images are scraped from the previews, not the original full resolutions, which can be way bigger in size and resolution (but are not provided by the scraper).

## Full dataset
The full dataset consists of **188k apps**, with **2.1m images**, so on average, **11 images** per app.

Based on the sample batch, the full dataset would take about **6 hours** to download, and take up around **170 GiB** of disk space.

Further statistics are avaialble in the [stats.ipynb](stats.ipynb) notebook.

# Apple store

The process is the same as with Google Play apps.

First scrape yields **11k unique apps** by **8k unique developers**, which took **15 seconds**.

Second by-developer scrape added **2k unique apps** for a total of **13k applications**.

Third by-app scrape encountered huge data loss. Out of the **13k apps**, only **2k detailed results** were obtained.

We made multiple attempts, trying to receive more records, lowering the chunk size, but nothing helped.


# How to run

Install dependencies
```
npm install
pip install -r requirements.txt
```

Prepare data directories
```
mkdir gplay/images
```

Run app scraper
```
node ./gplay_scrape.js
```

Run image collector
```
python gplay_images.py
```

Run dataset filtering
```
python filter_dataset.py
```

# Hardware
- processor: AMD Ryzen 7 5800x
- RAM: 32 GB, 3066 MHz


Internet speed: up to 30 Mbps

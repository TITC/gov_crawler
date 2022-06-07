import random
from constant import headers
from handytools import op
import os
import urllib.request
from numpy import extract
from tqdm import tqdm
from constant import url_log_path
project_path = op.parent_dir(path=__file__)


def download_file(url, filename):
    if os.path.exists(filename):
        return
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": random.choice(headers)})
        f = urllib.request.urlopen(req, timeout=5)
        open(filename, "wb").write(f.read())
    except Exception as e:
        print(e, url)


def download_city_assets(city_name, assets):
    for category in assets:
        asset_path = "%s/assets/%s/%s" % (project_path, city_name, category)
        os.makedirs(asset_path, exist_ok=True)
        for url in tqdm(assets[category], desc="downloading %s" % category):
            if city_name not in url:
                continue
            filename = url.split("/")[-1]
            download_file(url, "%s/assets/%s/%s/%s" % (project_path, city_name, category, filename))


def sort_assets(url_file_path):
    urls = op.readlines(path=url_file_path)
    assets = {"pdf": [], "word": [], "excel": []}
    for url in urls:
        if url.endswith(".pdf"):
            assets["pdf"].append(url)
        elif url.endswith(".doc") or url.endswith(".docx"):
            assets["word"].append(url)
        elif url.endswith(".xls") or url.endswith(".xlsx"):
            assets["excel"].append(url)
    return assets


if __name__ == '__main__':
    assets = sort_assets(url_file_path="%s/%s" % (project_path, url_log_path))
    download_city_assets(city_name="wuhan", assets=assets)
    download_city_assets(city_name="wuhu", assets=assets)

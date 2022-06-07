# gov_crawler
used for crawl China's government document and analysis policy trend.

## Installation

```shell
git clone https://github.com/TITC/gov_crawler.git
cd gov_crawler
pip install -e .
```

## Usage

```shell
# collect related url
python govcrawl/bfs_crawler.py
# download assets
python govcrawl/assets_manage.py
# analysis(util now is a simple ngram count)
python govcrawl/analysis.py
```



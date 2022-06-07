from ast import keyword
from queue import PriorityQueue
from collections import namedtuple
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from handytools import op
import traceback
import random
from tqdm import tqdm
from constant import headers, url_log_path


project_path = op.parent_dir(path=__file__)
debug_file = open("%s/log/debug.log" % project_path, 'w')
url_save_path = "%s/%s" % (project_path, url_log_path)


Node = namedtuple("Node", ["url", "depth", "parent"])


class LayerQueue(PriorityQueue):
    def __init__(self, *args):
        super(LayerQueue, self).__init__(*args)

    def put(self, item):
        super().put((item.depth, item))

    def get(self):
        return super().get(self.queue)[1]


def url_process(url, back_num=0):
    """
        >>> url_process("http://www.wuhan.gov.cn/sy/tswh/index.html", back_num=1)
        http://www.wuhan.gov.cn/sy/tswh/
        >>> url_process("http://tjj.wuhan.gov.cn/zfxxgk/fdzdgknr/tjsj", back_num=2)
        http://tjj.wuhan.gov.cn/zfxxgk/
        >>> url_process("http://www.wuhan.gov.cn/zwgk/zdly/ggzypz", back_num=3)
        http://www.wuhan.gov.cn/
    """
    if back_num == 0:
        return url
    prefix, domain = url.split("//")
    layer_num = max(1, len(domain.split("/")) - back_num)
    return prefix+"//"+"/".join(domain.split("/")[:layer_num])


def get_neighbors(node: Node):
    if any([ele in node.url for ele in [".pdf", ".doc", ".xls", ".flv", ".mp4", ".rar"]]):
        return []
    try:
        req = Request(node.url, headers={"User-Agent": random.choice(headers)})
        html = urlopen(req, timeout=5).read()
        html = html.decode("utf-8")
    except Exception as e:
        # traceback.print_exc()
        # print(e, node.url)
        return []
    parent_url = node.url.split("?")[0]  # remove parameters
    parent_url = parent_url[:-1] if parent_url.endswith("/") else parent_url
    soup = BeautifulSoup(html, features='html.parser')
    neighbors = []
    for candidate_tag in [("a", "href"), ('li', "src"), ("a", "src")]:
        tags = soup.find_all(candidate_tag[0])
        for tag in tags:
            url = str(tag.get(candidate_tag[1])).strip()
            if not url.startswith('http') and not url.startswith('.'):
                continue
            if url.startswith(".") and url != ".":  #only process ./xx/xxxx and ../../xx
                suffix = url
                url = parent_url
                # print("="*100, file=debug_file)
                # print("suffix: ", suffix, "url: ", url, file=debug_file)
                if suffix.startswith('./'):
                    suffix = "/"+suffix.replace('./', '')
                    if "#" in url and len(url.split("#")) > 1 and url.split("#")[0].split("/")[-1].endswith("html") and "#" in suffix:
                        old_suffix = url.split("#")[0].split("/")[-1]
                        url = url[:url.index(old_suffix)-1]
                    url = url_process(url, back_num=1) + suffix if url.endswith("html") else url+suffix
                elif suffix.startswith('../'):
                    url = url_process(url, back_num=suffix.count('../'))+"/"+suffix.replace("../", "")
                # print("url: ", url, file=debug_file)
                # print("="*100, file=debug_file)
            neighbors.append(Node(url, node.depth+1, node))
    return neighbors


def run(keywords: list, url="http://www.wuhan.gov.cn/", num_stop=10000):
    """
    Breadth-first search algorithm.
    """
    visited = set()
    seen = set()
    queue = LayerQueue()
    start_node = Node(url, 0, None)
    queue.put(start_node)
    seen.add(start_node.url)
    pbar = tqdm(total=num_stop)
    while not queue.empty():
        node = queue.get()
        if node.url not in visited:
            visited.add(node.url)
            # update pbar
            pbar.update(1)
            pbar.set_description(desc=url)
            if len(visited) > num_stop:
                break
            for neighbor in get_neighbors(node):
                neighbor = Node(neighbor.url, 0, node) if any(["%s" % keyword in neighbor.url for keyword in keywords]) else neighbor
                if neighbor.url not in visited and neighbor.url not in seen:
                    # visited is those url excuted after get_neighbors, seen is those url collected but before get_neighbors
                    queue.put(neighbor)
                    seen.add(neighbor.url)
                    op.append_list2file(obj=[neighbor.url], path=url_save_path)


if __name__ == '__main__':
    keyword = ["wuhan", "wuhu"]
    run(keyword, url="http://www.wuhan.gov.cn/")
    run(keyword, url="https://www.wuhu.gov.cn/")

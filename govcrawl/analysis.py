import math
import os
import textract
from handytools import op
from tqdm import tqdm
project_path = op.parent_dir(path=__file__)


def extract_txt(savepath: str, city_name: str):
    assert_type = ["pdf", "word"]
    long_str = []
    for atype in assert_type:
        folder_path = "%s/assets/%s/%s" % (project_path, city_name, atype)
        filenames = os.listdir(folder_path)
        for i, filename in tqdm(enumerate(filenames), desc="%s" % atype, total=len(filenames)):
            abs_path = "%s/%s" % (folder_path, filename)
            try:
                text = textract.process(abs_path).decode('utf-8')
            except Exception as e:
                text = ""
            long_str.append(text)
    op.savelist(obj=long_str, path=savepath)
    return long_str


def word_count(texts: str, savepath, max_ngram=10):
    ngram = {}
    length = len(texts)
    for i in tqdm(range(length), desc="word_count"):
        for n in range(max_ngram):
            word = texts[i:i+n+1].replace(" ", "")
            zhs, _ = op.extract(word, type="zh")
            if word == "":
                continue
            if len("".join(zhs))/len(word) < 0.5:
                continue
            ngram[word] = 1 if word not in ngram else ngram[word] + 1
    op.save2pkl(obj=ngram, path=savepath)
    return ngram


def postprocess(city_name):
    longstr_path = "%s/assets/%s/long_str.log" % (project_path, city_name)
    pkl_path = "%s/assets/%s/ngram.pkl" % (project_path, city_name)
    if not os.path.exists(longstr_path):
        extract_txt(longstr_path, city_name)
    if not os.path.exists(pkl_path):
        long_str = op.readlines(longstr_path)
        long_str = " ".join(long_str)
        ngram = word_count(long_str, savepath=pkl_path)
    else:
        ngram = op.rpkl(pkl_path)
    return op.sort_dict_by_value(d=ngram, increase=False)


def show_topk(ngram, num=10):
    for k, v in ngram.items():
        if len(k) < 2:
            continue
        print(k, v)
        num -= 1
        if num < 0:
            break


if __name__ == '__main__':
    word = "疫情"
    wuhan_ngram = postprocess(city_name="wuhan")
    wuhu_ngram = postprocess(city_name="wuhu")
    print(wuhan_ngram[word])
    print(wuhu_ngram[word])
    show_topk(ngram=wuhan_ngram, num=20)
    print("==========================================================")
    show_topk(ngram=wuhu_ngram, num=20)

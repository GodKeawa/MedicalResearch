import jieba
import jieba.analyse
import json
import math
from collections import Counter

ARTICLES = 748

# 自定义词典
jieba.load_userdict(r"custom_words.txt")

# 使用一个全局词典统计所有文章的词
word_dic = dict()


with open(r"datalist.json", "r", encoding="utf-8") as f:
    dic = json.loads(f.read())

def isNum(s):  # 加强版数字判断逻辑
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def article_cut():
    global word_dic
    with open(r"stop_words.txt", "r", encoding="utf-8") as f:
        stop_words = f.read().splitlines()
    stop_words.append("\n")
    stop_words.append(" ")
    stop_words.append(" ")  # ocr产生的异常字符

    for item in dic:
        path = "articles/" + item["index"] + "/"
        with open(path + "text.txt", "r", encoding="utf-8") as f:
            text = f.read()
        rawwords = jieba.cut(text)
        words = [word for word in rawwords if word not in stop_words]
        single_dict = Counter(words)
        temp = single_dict.items()
        sorted_temp = sorted(temp, key=lambda x: x[1], reverse=True)
        single_dict = {k: v for k, v in sorted_temp}

        # DEBUG
        # for wd, ct in single_dict.items():
        #     print(wd + ": " + str(ct))

        # 为每篇文章单独加一个json存数据
        with open(path + "words_dict.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(single_dict, ensure_ascii=False))

        # 添加一个热门词语字段
        hot_dict = {}
        keys = list(single_dict.keys())
        for i in range(10):
            key = keys[i]
            hot_dict.update({key: single_dict[key]})
        item.update({"hotwords": hot_dict})

        # 加入到全局字典里
        for wd, ct in single_dict.items():
            word_dic[wd] = word_dic.get(wd, 0) + ct

        print(item["index"] + " Finished!")
    # 写入全局词典
    temp = word_dic.items()
    sorted_temp = sorted(temp, key=lambda x: x[1], reverse=True)
    word_dic = {k: v for k, v in sorted_temp}
    with open(r"overal_dict.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(word_dic, ensure_ascii=False))

    # 写入完全datalist
    with open(r"full_datalist.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(dic, ensure_ascii=False))


def IDF_gen():
    IDF_dic = {}
    with open(r"overal_dict.json", "r", encoding="utf-8") as f:
        overal_dic = json.loads(f.read())
    # 初始置为0
    for wd, ct in overal_dic.items():
        IDF_dic.update({wd: 0})
    # 遍历每篇文章的words_dict，计算词在文章中出现的次数
    for item in dic:
        path = "articles/" + item["index"] + "/"
        with open(path + "words_dict.json", "r", encoding="utf-8") as f:
            single_dict = json.loads(f.read())
        for wd, ct in single_dict.items():
            IDF_dic[wd] += 1
    for wd, ct in IDF_dic.items():
        IDF_dic[wd] = math.log10(ARTICLES / (ct + 1))
    with open(r"IDF.txt", "w", encoding="utf-8") as f:
        for wd, ct in IDF_dic.items():
            # 调整数字权重，如有需要可以打开
            if isNum(wd):
                f.write(wd + " " + "-1" + "\n")
            else:
                f.write(wd + " " + str(ct) + "\n")


def theme_extract():
    jieba.analyse.set_idf_path(r"IDF.txt")
    jieba.analyse.set_stop_words(r"stop_words.txt")
    with open(r"full_datalist.json", "r", encoding="utf-8") as f:
        full_dic = json.loads(f.read())
    for item in full_dic:
        path = "articles/" + item["index"] + "/"
        with open(path + "text.txt", "r", encoding="utf-8") as f:
            text = f.read()
        keywords = jieba.analyse.extract_tags(text, topK=10, withWeight=True)
        key_dic = {}
        for keyword in keywords:
            key_dic.update({keyword[0]: keyword[1]})
        item.update({"theme": key_dic})
        print(item["index"] + " Finished!")
    with open(r"full_datalist.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(full_dic, ensure_ascii=False))


if __name__ == "__main__":
    # article_cut()  # 已完成，文件已生成
    # IDF_gen()  # 已完成，文件已生成 IDF.txt
    # theme_extract() # 已完成，写入full_datalist.json
    print("Finished!")

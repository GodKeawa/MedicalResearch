import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from wordcloud import WordCloud
import json
import PySimpleGUI as sg
from os import listdir
from cv2 import imread


def word_cloud_gen_simple(s: str):
    if s == "all":
        path = "overal_dict.json"
    else:
        path = "articles/" + s + "/words_dict.json"
    with open(path, "r", encoding="utf-8") as f:
        word_dic = json.loads(f.read())
    wc = WordCloud(
        font_path=r"font\SourceHanSansCN-Light.otf",
        width=1920,
        height=1080,
        background_color="white",
    )
    wc.generate_from_frequencies(word_dic)
    plt.figure(figsize=(12.8, 7.2), dpi=100)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    print("closed")


def word_cloud_gen_list(l: list):
    word_dic = {}
    for s in l:
        path = "articles/" + s + "/words_dict.json"
        with open(path, "r", encoding="utf-8") as f:
            single_dict = json.loads(f.read())
        for wd, ct in single_dict.items():
            word_dic[wd] = word_dic.get(wd, 0) + ct
    wc = WordCloud(
        font_path=r"font\SourceHanSansCN-Light.otf",
        width=1920,
        height=1080,
        background_color="white",
    )
    wc.generate_from_frequencies(word_dic)
    plt.figure(figsize=(12.8, 7.2), dpi=100)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    print("closed")


current_image_index = -1


def show_img(s: str):
    global current_image_index
    current_image_index = -1
    path = "articles/" + s + "/"
    filelist = [file for file in listdir(path) if "jpg" in file or "png" in file]
    imgs = []
    for file in filelist:
        img = imread(path + file)
        imgs.append(img)

    def show_image():
        global current_image_index
        current_image_index += 1
        plt.imshow(imgs[current_image_index%len(filelist)])
        plt.axis("off")
        plt.draw()

    def next_image(event):
        plt.clf()
        show_image()

    # 创建图形和按钮
    plt.subplots(figsize=(10, 9), dpi=100)
    plt.subplots_adjust(left=0.15, right=0.85, top=0.99, bottom=0.01)  # 减少边距
    plt.axis("off")
    show_image()  # 显示第一张图片

    # 添加按钮
    axnext = plt.axes([0.9, 0.1, 0.1, 0.075])
    bnext = Button(axnext, "Next")
    bnext.on_clicked(next_image)

    plt.show()


# 全局字典
with open(r"full_datalist.json", "r", encoding="utf-8") as f:
    dic = json.loads(f.read())
searchmethods = ["查询序号", "标题", "时间", "单词", "热门词", "关键词", "全文"]
method_dic = {
    "查询序号": "index",
    "标题": "title",
    "时间": "time",
    "单词": "words",
    "热门词": "hotwords",
    "关键词": "theme",
    "全文": "whole",
}
namelist = [
    "index",
    "title",
    "url",
    "number",
    "time",
]
searchlist = []

leftlayout = [
    [sg.Text("请按顺序操作", size=(32, 1), font=(None, 18))],
    [
        sg.Drop(
            searchmethods,
            default_value="选择查询方式",
            key="methods",
            size=(25, 1),
            font=(None, 18),
        ),
        sg.Button("选择", font=(None, 18), size=(6, 1)),
        sg.Button("重置", font=(None, 18), size=(6, 1), disabled=True),
    ],
    [
        sg.InputText(
            default_text="输入查询的内容",
            key="keys",
            disabled=True,
            size=(25, 1),
            font=(None, 18),
        ),
        sg.Button("查询", font=(None, 18), size=(6, 1), disabled=True),
        sg.Button("重输入", font=(None, 18), size=(6, 1), disabled=True),
    ],
    [
        sg.Drop(
            searchlist,
            default_value="选择文章",
            key="articles",
            size=(32, 1),
            font=(None, 18),
        )
    ],
    [
        sg.Button("查询数据", font=(None, 18), size=(10, 1), disabled=True),
        sg.Button("生成词云", font=(None, 18), size=(10, 1)),
        sg.Button("重选", font=(None, 18), size=(8, 1), disabled=True),
    ],
    [sg.Text("\n", size=(30, 1), font=(None, 6))],
    [sg.Text("基本信息如下：", size=(30, 1), font=(None, 18))],
    [
        sg.Text("查询序号", size=(8, 1), font=(None, 18)),
        sg.Multiline(
            "",
            key="index",
            font=(None, 16),
            background_color="white",
            text_color="black",
            size=(38, 1),
        ),
    ],
    [
        sg.Text("标题", size=(8, 1), font=(None, 18)),
        sg.Multiline(
            "",
            key="title",
            font=(None, 16),
            background_color="white",
            text_color="black",
            size=(45, 2),
        ),
    ],
    [
        sg.Text("原始网址", size=(8, 1), font=(None, 18)),
        sg.Multiline(
            "",
            key="url",
            font=(None, 16),
            background_color="white",
            text_color="black",
            size=(45, 2),
        ),
    ],
    [
        sg.Text("编号", size=(8, 1), font=(None, 18)),
        sg.Multiline(
            "",
            key="number",
            font=(None, 16),
            background_color="white",
            text_color="black",
            size=(38, 1),
        ),
    ],
    [
        sg.Text("发布时间", size=(8, 1), font=(None, 18)),
        sg.Multiline(
            "",
            key="time",
            font=(None, 16),
            background_color="white",
            text_color="black",
            size=(38, 1),
        ),
    ],
    [
        sg.Text("热词", size=(8, 1), font=(None, 18)),
        sg.Multiline(
            "",
            key="hotwords",
            font=(None, 16),
            background_color="white",
            text_color="black",
            size=(45, 8),
        ),
    ],
    [
        sg.Text("关键词", size=(8, 1), font=(None, 18)),
        sg.Multiline(
            "",
            key="theme",
            font=(None, 16),
            background_color="white",
            text_color="black",
            size=(45, 8),
        ),
    ],
]
rightlayout = [
    [
        sg.Text("文章内容", font=(None, 18), size=(10, 1)),
        sg.Text("Tips:按钮一直在那个位置，渲染有问题->", font=(None, 16), size=(36, 1)),
        sg.Button("查看原始图片", font=(None, 18), size=(16, 1), disabled=True),
    ],
    [sg.Multiline("", key="fulltext", size=(66, 30), font=(None, 18))],
]
left = sg.Column(leftlayout)
right = sg.Column(rightlayout)
mainlayout = [[left, right]]


def updatelist(method: str, key: str):
    global searchlist, method_dic
    searchlist = []
    method = method_dic[method]
    if key == "all":
        for item in dic:
            searchlist.append(item["index"])
    else:
        if method in ["index", "title"]:
            for item in dic:
                if key in item[method]:
                    searchlist.append(item["index"])
        else:
            match method:
                case "time":
                    for item in dic:
                        if key in item["time"]:
                            searchlist.append(item["index"])
                case "words":
                    for item in dic:
                        path = "articles/" + item["index"] + "/words_dict.json"
                        with open(path, "r", encoding="utf-8") as f:
                            words = json.loads(f.read())
                        for wd in list(words.keys()):
                            if key == wd or key in wd:
                                searchlist.append(item["index"])
                case "hotwords":
                    for item in dic:
                        hotwords = list(item["hotwords"].keys())
                        for wd in hotwords:
                            if key == wd or key in wd:
                                searchlist.append(item["index"])
                case "theme":
                    for item in dic:
                        for wd in item["theme"]:
                            if key == wd or key in wd:
                                searchlist.append(item["index"])
                case "whole":
                    for item in dic:
                        path = "articles/" + item["index"] + "/text.txt"
                        with open(path, "r", encoding="utf-8") as f:
                            text = f.read()
                        if key in text:
                            searchlist.append(item["index"])


def find_article(key: str):
    global dic
    for item in dic:
        if item["index"] == key:
            return item
    return False


def main():
    global searchlist
    window = sg.Window("DATABASE", mainlayout)
    window.Resizable = True
    while True:
        event, values = window.read()
        match event:
            case "选择":
                window["查看原始图片"].Update(disabled=True)
                if values["methods"] not in searchmethods:
                    continue
                window["methods"].Update(disabled=True)
                window["keys"].update("")
                window["选择"].Update(disabled=True)
                window["重置"].Update(disabled=False)
                window["查询"].Update(disabled=False)
                window["keys"].Update(disabled=False)
            case "重置":
                window["查看原始图片"].Update(disabled=True)
                window["methods"].Update(disabled=False)
                window["选择"].Update(disabled=False)
                window["重置"].Update(disabled=True)
                window["查询"].Update(disabled=True)
                window["重输入"].Update(disabled=True)
                window["重选"].Update(disabled=True)
                window["keys"].update("")
                window["keys"].Update(disabled=True)
                window["查询数据"].Update(disabled=True)
                searchlist = []
                window["articles"].Update(values=searchlist)
                window["articles"].Update(disabled=True)
                window["fulltext"].Update("")
            case "查询":
                window["查看原始图片"].Update(disabled=True)
                if values["keys"] == "输入查询的内容" or values["keys"] == "":
                    if values["methods"] in ["查询序号", "标题", "时间"]:
                        key = "all"
                    else:
                        continue
                else:
                    key = values["keys"]
                window["查询"].Update(disabled=True)
                window["keys"].Update(disabled=True)
                updatelist(values["methods"], key)
                window["articles"].Update(values=searchlist)
                window["articles"].Update(disabled=False)
                window["重输入"].Update(disabled=False)
                window["查询数据"].Update(disabled=False)
                window["重选"].Update(disabled=False)
            case "重输入":
                window["查看原始图片"].Update(disabled=True)
                window["查询"].Update(disabled=False)
                window["keys"].update("")
                window["keys"].Update(disabled=False)
                window["查询数据"].Update(disabled=True)
                window["重选"].Update(disabled=True)
                searchlist = []
                window["articles"].Update(values=searchlist)
                window["articles"].Update(disabled=True)
                window["重输入"].Update(disabled=True)
                window["fulltext"].Update("")
            case "查询数据":
                window["查看原始图片"].Update(disabled=True)
                if values["articles"] == "选择文章" or values["articles"] == "":
                    continue
                window["重选"].Update(disabled=False)
                find_dic = find_article(values["articles"])
                if find_dic:
                    for name in namelist:
                        window[name].Update(find_dic[name])
                    hotwords = ""
                    for wd, ct in find_dic["hotwords"].items():
                        hotwords += wd + ": " + str(ct) + "\n"
                    window["hotwords"].Update(hotwords)
                    theme = ""
                    for wd, ct in find_dic["theme"].items():
                        theme += wd + ": " + str(ct) + "\n"
                    window["theme"].Update(theme)
                    path = "articles/" + find_dic["index"] + "/text.txt"
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()
                    window["fulltext"].Update(text)
                    window["查看原始图片"].Update(disabled=False)
                else:
                    sg.popup("未找到该文章", font=(None, 18))
            case "重选":
                window["查看原始图片"].Update(disabled=True)
                window["重选"].Update(disabled=True)
                for name in namelist:
                    window[name].Update("")
                window["hotwords"].Update("")
                window["theme"].Update("")
                window["articles"].Update(values=searchlist)
                window["fulltext"].Update("")
            case "生成词云":
                window["查看原始图片"].Update(disabled=True)
                if values["articles"] != "选择文章" and values["articles"] != "":
                    find_dic = find_article(values["articles"])
                    if find_dic:
                        word_cloud_gen_simple(find_dic["index"])
                    else:
                        sg.popup("未找到该文章", font=(None, 18))
                elif values["articles"] == "":
                    if searchlist:
                        word_cloud_gen_list(searchlist)
                    else:
                        word_cloud_gen_simple("all")
                else:
                    word_cloud_gen_simple("all")
            case "查看原始图片":
                show_img(values["index"])
                print("closed")

            case None:
                break


if __name__ == "__main__":
    main()

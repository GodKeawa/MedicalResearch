import re
import requests
import json
import os
import time
from bs4 import BeautifulSoup

# 请求标头
headers = {
    "Accept": "application/xml, text/xml, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6",
    # "Cookie": "JSESSIONID=C27B6BB37937C6211508B7BBC873D1AA; https_waf_cookie=e084c96f-f066-4e18945efe8337763dcfabf3db5d7f1186eb",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
}


def get_datalist():
    datas = []
    # datastore.txt通过浏览器调试获取，直接抓取网站后端数据库传给前端的表
    with open("datas/datastore.txt", "r", encoding="utf-8") as f:
        text = f.read()
        singlelist = re.findall(re.compile(r"""<li>.*?</li>"""), text)
        for single in singlelist:
            soup = BeautifulSoup(single, "html.parser")
            url = soup.find("a")["href"]
            span = soup.find_all("span")
            datas.append(
                {
                    "index": span[0].text,
                    "title": span[1].text,
                    "url": "https://www.nhsa.gov.cn/" + url,
                    "number": span[2].text,
                    "time": span[3].text,
                }
            )
        with open("datas/datalist.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(datas, ensure_ascii=False))


def get_articles():
    with open("datas/datalist.json", "r", encoding="utf-8") as f:
        dic = json.loads(f.read())
    for item in dic:
        count = 0
        while True:
            response = requests.get(url=item["url"], headers=headers)
            if response.status_code == 200:
                response.encoding = "utf-8"
                break
            else:
                print("Article get failed at " + item["index"])
                count += 1
                time.sleep(1)
                if count > 5:
                    print("Critical error at " + item["index"])
                    break

        soup = BeautifulSoup(response.text, "html.parser")
        start = soup.find("meta", {"name": "ContentStart"})
        end = soup.find("meta", {"name": "ContentEnd"})
        path = "articles/" + item["index"] + "/"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + "text.txt", "w", encoding="utf-8") as f:
            pic_index = 0
            for content in start.next_siblings:
                if content == end:
                    break
                # 解析出来的内容可能是图片
                if content.text == "":
                    pic_url = re.findall(
                        re.compile(r"""<a href=\".*?\""""), content.__str__()
                    )
                    if pic_url:
                        for urlbase in pic_url:
                            fullurl = "https://www.nhsa.gov.cn" + urlbase[9:-1:]
                            f.write(fullurl + "\n")  # 无所谓写不写
                            with open(path + str(pic_index) + fullurl[-4::], "wb") as p:
                                count = 0
                                while True:
                                    response = requests.get(
                                        url=fullurl, headers=headers
                                    )
                                    if response.status_code == 200:
                                        break
                                    else:
                                        print("Pic get failed at " + path + fullurl)
                                        count += 1
                                        time.sleep(1)
                                        if count > 5:
                                            print("Critical error at " + path + fullurl)
                                            break
                                p.write(response.content)
                                pic_index += 1
                else:
                    f.write(content.text)
                    f.write("\n\n")

        print(item["index"] + " Finished!")
        time.sleep(0.5)


def exchange_name():
    # 由于网页特性少部分图片顺序颠倒了，这里可以手动切换一下
    # 其实也可以不切换，毕竟看的时候根据分段大致就能认出来，而且本质上这也不是用来看的
    # 如果要自动化可以通过后面ocr识别判断“医保函”和页标进行自动处理
    path = "articles/2022-05-00085/"
    jpg, jpg_0, jpg_1 = path + "temp.jpg", path + "0.jpg", path + "1.jpg"
    os.rename(jpg_0, jpg)
    os.rename(jpg_1, jpg_0)
    os.rename(jpg, jpg_1)


def ocr_process():
    from paddleocr import PaddleOCR

    ocr = PaddleOCR()

    with open("datas/datalist.json", "r", encoding="utf-8") as f:
        dic = json.loads(f.read())
    for item in dic:
        path = "articles/" + item["index"] + "/"
        files = os.listdir(path)
        if len(files) == 1: # 加速用的，第一次运行可能只有text.txt
            print(item["index"] + " Passed!")
            continue
        with open(path + "text.txt", "w", encoding="utf-8") as f:
            for i in range(len(files) - 1):
                if ("jpg" not in files[i]) and ("png" not in files[i]):
                    continue
                result = ocr.ocr(path + files[i], cls=True)
                for line in result[0]:
                    f.write(line[1][0])
                    if (
                        line[1][0][-1] == "。"
                        or line[1][0][-1] == "："
                        or line[1][0][0]
                        in ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
                    ):
                        f.write("\n\n")

        print(item["index"] + " Finished!")


if __name__ == "__main__":
    # get_datalist()  # 生成datalist.json，已经生成过了
    # get_articles() # 获取文章，已经全部获取完毕
    # exchange_name() # 手动优化部分内容
    # ocr_process()  # ocr处理图片，覆写text.txt，已初步完成

    print("Finished!")

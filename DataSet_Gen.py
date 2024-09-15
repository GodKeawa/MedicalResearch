import json

# 全局字典
#           0      1       2         3          4           5         6
labels = ['医疗', '医保', '医药', '医疗x医保', '医疗x医药', '医保x医药', '三联动']
with open(r"datas/full_datalist.json", "r", encoding="utf-8") as f:
    dic = json.loads(f.read())


def set_labels():
    with open("datas/med.train.txt", "a", encoding="utf-8") as med:
        for item in dic[126::]:
            path = "articles/" + item["index"] + "/"
            with open(path + "text.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
            rawtext = "".join(lines)
            text = ""
            for line in lines[4:-4]:
                if line != "\n":
                    text += line.strip()
            print(rawtext)
            print(item["hotwords"].keys())
            print(item["theme"].keys())
            label: int = int(input(item["index"] + "label:"))
            med.write(labels[label] + ' ' + text + '\n')


def get_random():
    with open("datas/med.train.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()[::10]
        with open("datas/med.val.txt", "w", encoding="utf-8") as val:
            val.writelines(lines)

def check():
    with open("datas/med.train.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            label, text = line.strip().split('\t')
            print(label, text)
if __name__ == "__main__":
    # set_labels()
    get_random()
    # check()
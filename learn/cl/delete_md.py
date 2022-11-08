import os


def delete_md(list, directoryName):
    for name in list:
        fileName = directoryName + name
        if (os.path.exists(fileName) and name != '.DS_Store' and name.endswith(".md")):
            file = open(fileName, "r", encoding="utf-8")
            for line in file.readlines():
                if (line.startswith("![](") and len(line) > 10):
                    picture_address = line[7:].split(")")[0]
                    # print(picture_address)
                    if (os.path.exists(picture_address)):
                        os.remove(picture_address)
            os.remove(fileName)
            print(f"{name}删除成功")


# 删除文档，并删除文档中的所有图片
if __name__ == '__main__':
    directory = "独乐乐不如众乐乐/"
    for root, dirs, files in os.walk(directory):
        delete_md(files, directory)

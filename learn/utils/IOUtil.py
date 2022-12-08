import os.path
import uuid

from learn.contants.Constant import CRAWER_1024_JISHU_FILE, CARWER_1024_WENXUE_FILE, CARWER_1024_PICTURE_FILE


# 技术写入内容信息
def writeContent(content, fileName):
    fileName = "未分类.txt" if fileName == "" else fileName
    # 判断是否有这个文件，如果没有就创建一个
    # os.mkdir("file/") if (1-os.path.exists("file/")) else 1+1
    if (1 - os.path.exists(CRAWER_1024_JISHU_FILE)):
        os.mkdir(CRAWER_1024_JISHU_FILE)
    f = open(fileName, 'a', encoding='utf-8')
    f.write(content)
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.close()


def writeContentNotRept(content, fileName):
    fileName = "未分类.txt" if fileName == "" else fileName
    # 判断是否有这个文件，如果没有就创建一个
    # os.mkdir("file/") if (1-os.path.exists("file/")) else 1+1
    # if (os.path.exists(fileName)):
    #     # 如果有这个文件，就删除重新写
    #     os.remove(fileName)
    f = open(fileName, 'a', encoding='utf-8')
    f.write(content)
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.close()


# 文学写入title
def wxWriteTitle(fileName, title):
    fileName = "未分类.txt" if fileName == "" else fileName
    if (len(fileName.split("/")[0]) != 0):
        if (1 - os.path.exists(fileName.split("/")[0])):
            os.mkdir(fileName.split("/")[0])
    file = open(fileName, 'a', encoding='utf-8')
    file.write(title)
    file.write('\n')
    file.close()


# 文学写入内容
def wxWriteContent(fileName, content):
    fileName = "未分类.txt" if fileName == "" else fileName
    if (len(fileName.split("/")[0]) != 0):
        if (1 - os.path.exists(fileName.split("/")[0])):
            os.mkdir(fileName.split("/")[0])
    file = open(fileName, 'a', encoding='utf-8')
    file.write(content)
    i = 1
    while (i <= 4):
        file.write('\n')
        i += 1
    file.close()


def writeCache(directory, name, content):
    name = "未分类" if name == "" else name
    if (1 - os.path.exists(directory)):
        os.mkdir(directory)
    file = open(directory + name + '.txt', 'a', encoding='utf-8')
    file.write(content)
    file.close()


def writePicture(fileName, content, suffix_name):
    fileName = str(uuid.uuid1()) + suffix_name if fileName == "" else fileName
    if (len(fileName.split("/")[0]) != 0):
        if (1 - os.path.exists(fileName.split("/")[0])):
            os.mkdir(fileName.split("/")[0])
    try:
        file = open(fileName, mode='wb')
        file.write(content)
        file.close()
    except Exception as err:
        print("出现异常" + str(err))
        return False
    return True

import os.path

from learn.contants.Constant import CRAWER_1024_JISHU_FILE, CARWER_1024_WENXUE_FILE


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


# 文学写入title
def wxWriteTitle(fileName,title ):
    fileName = "未分类.txt" if fileName == "" else fileName
    if (1 - os.path.exists(CARWER_1024_WENXUE_FILE)):
        os.mkdir(CARWER_1024_WENXUE_FILE)
    file = open(fileName, 'a', encoding='utf-8')
    file.write(title)
    file.write('\n')
    file.close()


# 文学写入内容
def wxWriteContent(fileName,content ):
    fileName = "未分类.txt" if fileName == "" else fileName
    if (1 - os.path.exists(CARWER_1024_WENXUE_FILE)):
        os.mkdir(CARWER_1024_WENXUE_FILE)
    file = open(fileName, 'a', encoding='utf-8')
    file.write(content)
    i = 1
    while (i <= 4):
        file.write('\n')
        i += 1
    file.close()

import os.path

from learn.contants.Constant import CRAWER_1024_JISHU_FILE


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

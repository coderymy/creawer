import os.path


def writeContent(content, fileName):
    fileName = "content1.txt" if fileName == "" else fileName
    # 判断是否有这个文件，如果没有就创建一个
    # os.mkdir("file/") if (1-os.path.exists("file/")) else 1+1
    if (1 - os.path.exists("file/")):
        os.mkdir("file/")
    f = open("file/" + fileName, 'a', encoding='utf-8')
    f.write(content)
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.close()

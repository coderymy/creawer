# 下载图片
import os.path

from bs4 import BeautifulSoup

from learn.contants.Constant import CARWER_1024_PICTURE_FILE
from learn.sql.MySqlUtils import insertContentPic
from learn.sql.Tables import Content_pic
from learn.utils.IOUtil import writePicture
from learn.utils.Md5 import MD5
from learn.utils.Response import getPicture, getSoupAndSaveCache


def getResouceAndDownloadPic(name, url, suffix_name):
    name = MD5(name)
    # 判断是否有该pic，如果有就直接返回
    if (checkPic(name, suffix_name)): return getPicFileName(str(name), suffix_name)
    content = getPicture(url)
    if (len(content) == 0): return ""
    flag = writePicture(getPicFileName(str(name), suffix_name), content, suffix_name)
    if (flag == False):
        return ""
    else:
        return getPicFileName(str(name), suffix_name)


# 判断该目录下是否有该图片，如果有就不需要重复下载了
def checkPic(name, suffix_name):
    return os.path.exists(getPicFileName(str(name), suffix_name))


def getPicFileName(name, suffix_name):
    return CARWER_1024_PICTURE_FILE + name + suffix_name


def crawer_picture(name, url, id):
    # 使用url获取该页主体内容的所有图片链接
    soup = getSoupAndSaveCache(name, url)
    div_content = soup.select('#conttpc')[0]
    img_labels = div_content.find_all("img")
    if (len(img_labels) == 0):
        return ""
    print("开始下载图片：" + name)
    i = 0
    for item in img_labels:
        i += 1
        pic_url = item['ess-data']
        suffix_name = getSuffixName(pic_url)
        download_result = getResouceAndDownloadPic(name + str(i), pic_url, suffix_name)
        if (len(download_result) == 0):
            print(name + f" 第{str(i)}张下载失败，共{str(len(img_labels))}张")
            continue
        print(name + f" 第{str(i)}张下载成功，共{str(len(img_labels))}张")
        db_content_pic = Content_pic(id, name, str(item), pic_url, MD5(pic_url), getPicFileName(str(name), suffix_name))
        insertContentPic(db_content_pic)


def getSuffixName(url):
    suffixName = url.split(".")[-1:][0]
    if (len(suffixName) > 5):
        return ".jpg"
    return "." + suffixName


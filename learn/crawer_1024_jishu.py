import ast
import hashlib
import os.path
import time

import parsel
from bs4 import BeautifulSoup

from learn.utils.IOUtil import writeContent
from learn.utils.Response import getResponse, getSoup

# content的前缀
prefix_content = "https://cl.5837x.xyz/"


# 爬取页面列表
def crawer_List():
    pageName = "thread0806"
    fileName = getFileName(pageName)
    url_admin = prefix_content + pageName + '.php?fid=7'
    if (checkIsExistFile("file/" + getFileName(pageName))):
        f = open("file/" + fileName, 'r', encoding='utf-8')
        return ast.literal_eval(f.read())
    html = getResponse(url_admin)
    if (len(html) == 0):
        return ""
    soup = BeautifulSoup(html, "html.parser")  # BeautifulSoup解析html
    title_text = soup.title.text
    if (title_text == " 無法找到頁面 草榴社區 " or title_text == "403 Forbidden"):
        print("下载失败：首页列表:404")
        return ""
    contents = soup.select("#tbody")[0]
    urlList = {}
    for item in contents:
        if (item == "\n"):
            continue
        a_label = item.select('.tal')[0].a
        url = prefix_content + a_label['href']
        name = a_label.text
        name = name.replace('\xa0', '').replace('/', '-')
        urlList[name] = url
        # print("url:" + url + "\n" + "name:" + name)
    print(urlList)
    writeContent(str(urlList), fileName)
    return urlList


# 爬取具体的列表的内容信息
def crawer_content(name, url):
    html = getHtml(name, url)
    if (len(html) == 0 or len(html.replace('\n', '')) == 0):
        return ""
    soup = BeautifulSoup(html, "html.parser")  # BeautifulSoup解析html
    title_text = soup.title.text
    if (title_text == " 無法找到頁面 草榴社區 "):
        print("下载失败：" + name + "：404")
        return ""
    if (title_text == "403 Forbidden"):
        print("下载失败：" + name + "：403 Forbidden")
        return ""
    content = soup.select(".tpc_content.do_not_catch")[0].text
    # https://cl.5837x.xyz/htm_data/2210/7/5334981.html
    return content


def checkIsExistFile(name):
    return os.path.exists(name)


def getFileName(name):
    return name + ".txt"


def encodeName(name):
    return hashlib.md5(name)


def getHtml(name, url):
    html = ''
    if (checkIsExistFile("file/" + getFileName(name))):
        file = open("file/" + getFileName(name), 'r', encoding='utf-8')
        html = file.read()
    else:
        html = getResponse(url)
        writeContent(html, getFileName(name))
    return html


def download_page():
    # 获取下载列表的url
    urlList = crawer_List()
    if (len(urlList) == 0):
        print("获取首页列表失败")
        return
    totalNum = len(urlList)
    print("开始下载，下载数量为[" + str(len(urlList)) + "]")
    succNum = 0
    for (name, url) in urlList.items():
        if (url[-4:] == 'html'):
            content = crawer_content(name, url)
            if (len(content) == 0):
                # 获取的字符串为空
                continue
            writeContent(getFileName(name), "")
            writeContent(content, "")
            succNum += 1
            print("下载成功【" + name + "】：" + url)
        else:
            print("下载失败：不识别该url：" + url)
    print(f"下载完成，成功数量：[{succNum}]，失败数量[{totalNum - succNum}]")


if __name__ == '__main__':
    download_page()

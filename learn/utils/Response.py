import os.path
import time
import requests
from bs4 import BeautifulSoup
from requests import ReadTimeout, ConnectTimeout
from urllib3.exceptions import InsecureRequestWarning
from learn.utils.IOUtil import writeContent, wxWriteContent, writeCache
import urllib3

from learn.utils.Md5 import MD5

urllib3.disable_warnings()

MAX_TIME = 5
CURRENT_TIME = 1
CACHE_DIRECTORY = "cache/"


def getResponse(baseurl):
    global CURRENT_TIME, MAX_TIME
    head = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
    }
    html = ''
    try:
        time.sleep(1)
        response = requests.get(baseurl, headers=head, timeout=1, verify=False)  # 获取网页信息
        response.encoding = 'utf-8'
        html = response.text
    except (ReadTimeout, InsecureRequestWarning, ConnectTimeout):
        # 判断超时，重复调用，最多五次
        print("链接访问失败：该链接超时 " + baseurl + " 当前第[" + str(CURRENT_TIME) + "]次")
        CURRENT_TIME += 1
        if (CURRENT_TIME <= MAX_TIME):
            getResponse(baseurl)
    except(BaseException):
        print("链接访问失败 未知异常")

    CURRENT_TIME = 1
    return html


# 查看本地是否有该文件，如果有就返回，没有就访问url并保存之后返回
def getHtml(fileName, url):
    if (os.path.exists(fileName)):
        return open(fileName, 'r', encoding='utf-8')
    else:
        html = getResponse(url)
        if (len(html) != 0):
            wxWriteContent(fileName, html)
            return html
        else:
            return ""


def getSoupAndSaveCache(name, url):
    name = MD5(name)
    global CACHE_DIRECTORY
    if (os.path.exists(CACHE_DIRECTORY + name + ".txt")):
        html = open(CACHE_DIRECTORY + name + ".txt", 'r', encoding='utf-8')
        soup = BeautifulSoup(html, "html.parser")  # BeautifulSoup解析html
        return soup
    else:
        html = getResponse(url)
        if (len(html) == 0 or len(html.replace('\n', '')) == 0):
            return ""
        soup = BeautifulSoup(html, "html.parser")  # BeautifulSoup解析html
        if (soup.title.text == " 無法找到頁面 草榴社區 " or soup.title.text == "403 Forbidden"):
            print("下载失败：" + name + soup.title.text)
            return ""
        writeCache(CACHE_DIRECTORY, name, html)
        return soup


def Get(url, params):
    global CURRENT_TIME, MAX_TIME
    head = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
    }
    result = ''
    try:
        time.sleep(1)
        response = requests.get(url, headers=head, params=params)
        response.encoding = 'utf-8'
        result = response.text
    except(BaseException):
        CURRENT_TIME += 1
        if (CURRENT_TIME <= MAX_TIME):
            Get(url, params)
        print("链接访问失败 未知异常")
    return result


def getPicture(url):
    global CURRENT_TIME, MAX_TIME
    head = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
    }
    result = ''
    try:
        time.sleep(1)
        # timeout=(10, 27) 表示10秒的链接超时时间，27秒的读取超时时间（读取超时时间没有默认值，如果不给就一直等待直到读取完）
        response = requests.get(url, headers=head, timeout=(5, 100))
        result = response.content
    except BaseException:
        # if (CURRENT_TIME <= MAX_TIME):
        #     getPicture(url)
        # print("链接访问失败 未知异常")
        return ''
    return result

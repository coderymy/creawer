import time

import requests
from bs4 import BeautifulSoup
from requests import ReadTimeout
from urllib3.exceptions import InsecureRequestWarning

MAX_TIME = 5
CURRENT_TIME = 1


def getResponse(baseurl):
    global CURRENT_TIME, MAX_TIME
    head = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
    }
    html = ''
    try:
        time.sleep(3)
        response = requests.get(baseurl, headers=head, timeout=1, verify=False)  # 获取网页信息
        response.encoding = 'utf-8'
        html = response.text
        CURRENT_TIME = 0
    except (ReadTimeout, InsecureRequestWarning):
        # 判断超时，重复调用，最多五次
        print("下载失败：该链接超时" + baseurl + "当前第[" + str(CURRENT_TIME) + "]次")
        CURRENT_TIME += 1
        if (CURRENT_TIME <= MAX_TIME):
            getResponse(baseurl)

    return html


def getSoup(url):
    html = getResponse(url)
    soup = BeautifulSoup(html, "html.parser")  # BeautifulSoup解析html
    return soup

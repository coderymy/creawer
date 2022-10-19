import os.path

from bs4 import BeautifulSoup
from learn.contants.Constant import CARWER_1024_WENXUE_FILE
from learn.utils.IOUtil import wxWriteTitle, wxWriteContent
from learn.utils.Response import getResponse, getHtml

# 列表页：https://cl.5837x.xyz/thread0806.php?fid=20
# 详情页：https://cl.5837x.xyz/htm_data/2210/20/5323656.html

# 多篇： https://cl.5837x.xyz/htm_data/2210/20/5325290.html
#       https://cl.5837x.xyz/read.php?tid=5325290&page=2&fpage=1
# https://cl.5837x.xyz/read.php?tid=5325290&page=3&fpage=1

LIST_NAME = "文学列表页面"
prefix_content = "https://cl.5837x.xyz/"
REQUEST_PAGE_NAME = "thread0806.php"
LIST_URL = prefix_content + REQUEST_PAGE_NAME + "?fid=20"

MAX_REQUEST_NUM = 100

CONTENT_FILE_NAME = "[合集] " + REQUEST_PAGE_NAME


def getFileName(name):
    return CARWER_1024_WENXUE_FILE + name + ".txt"


def getCollectFileName(name):
    return CARWER_1024_WENXUE_FILE + "【汇总】" + name + ".txt"


# 爬取列表页所有的地址信息对应的name等
def crawer_list(name, url):
    result_list = []
    html = getHtml(getFileName(name), url)
    if (len(str(html)) == 0):
        print("下载失败 列表页下载失败")
        return ""
    soup = BeautifulSoup(html, "html.parser")  # BeautifulSoup解析html
    list_HTML = soup.find_all("tbody")[1].select(".tal")
    for item_HTML in list_HTML:
        wx_admin_page_url = item_HTML.a["href"]
        wx_name = item_HTML.a.text
        chapter_urls = []
        chapter_spans = item_HTML.select(".thread_page")
        if (len(chapter_spans) != 0):
            chapter_span = chapter_spans[0]
            chapter_a_list = chapter_span.find_all("a")
            chapter_a_urls = getChapterAUrls(chapter_a_list)
            for chapter_url in chapter_a_urls:
                chapter_urls.append(prefix_content + chapter_url)
        #         处理...分页直接跳过的情况
        record = Item(wx_name, prefix_content + wx_admin_page_url, chapter_urls)
        result_list.append(record)
    return result_list


def getCache(name):
    fileName = getCollectFileName(name)
    if (os.path.exists(fileName)):
        return str(open(fileName, "r", encoding="utf-8"))
    return ""


def setCache(name, content):
    fileName = getCollectFileName(name)
    if (os.path.exists(fileName)):
        return ""
    else:
        wxWriteContent(fileName, content)
    return ""


def getChapterAUrls(chapter_a_list):
    urls = []
    item1 = chapter_a_list[-1]
    item2 = chapter_a_list[-2]
    i1 = int(item1.text)
    i2 = int(item2.text)
    if (i1 > 5 and (i1 - 1) != i2):
        splits = str(item1["href"]).split(str("&page=" + str(i1)))
        i = 1
        while (i <= i1):
            url = splits[0] + "&page=" + str(i) + splits[1]
            urls.append(url)
            i += 1
    else:
        for item in chapter_a_list:
            urls.append(item["href"])
    return urls


def crawer_content(item):
    content = getCache(item.name)
    if (len(content) != 0):
        return content
    url = item.url
    name = item.name
    html = getHtml(getFileName(name), url)
    if (len(str(html)) == 0):
        return ""
    soup = BeautifulSoup(html, "html.parser")
    title_text = soup.title.text
    if (title_text == " 無法找到頁面 草榴社區 "):
        print("下载失败：" + name + "：404")
        return ""
    if (title_text == "403 Forbidden"):
        print("下载失败：" + name + "：403 Forbidden")
        return ""
    content = soup.select(".tpc_content")[0].text
    if (len(item.chapter_urls) == 0):
        return content
    chapter_num = 1
    for chapter_url in item.chapter_urls:
        if (chapter_num == 1):
            chapter_num += 1
            continue
        chapter_html = getHtml(getFileName(getChapterName(name, chapter_num)), chapter_url)
        if (len(str(chapter_html)) == 0):
            continue
        chapter_soup = BeautifulSoup(chapter_html, "html.parser")
        chapter_divs = chapter_soup.select(".tpc_content")
        if (len(chapter_divs) == 0):
            continue
        for chapter_div in chapter_divs:
            content = content + "\n" + "\n" + chapter_div.text
        chapter_num += 1
    setCache(item.name, content)
    return content


def getChapterName(name, chapter_num):
    return name + "第" + str(chapter_num) + "页"


def download_wx():
    global LIST_URL, LIST_NAME, MAX_REQUEST_NUM
    # 获取当前要访问的页面的所有节点记录
    result_list = crawer_list(LIST_NAME, LIST_URL)
    # print(f"下载开始 列表页共[{str(len(result_list))}]个节点")
    succNum = 1
    for item in result_list:
        if (succNum > MAX_REQUEST_NUM):
            return;
        # print(f"记录名称:[{item.name}] url:[{item.url}] 章节为:[{item.chapter_urls}]")
        content = crawer_content(item)
        if (len(content) != 0):
            print(f"下载成功 [{item.name}]")
            wxWriteTitle(getFileName(CONTENT_FILE_NAME), "[第" + str(succNum) + "章]" + item.name)
            wxWriteTitle(getFileName(CONTENT_FILE_NAME), content)
            succNum += 1
        else:
            succNum += 1
            print(f"下载失败 [{item.name}]")


# 创建一个基于列表页每条Item的一个对象，用户数据传值
class Item:
    name = ''
    url = ''
    chapter_urls = []

    def __init__(self, name, url, chapter_urls):
        self.name = name
        self.url = url
        self.chapter_urls = chapter_urls


if __name__ == '__main__':
    download_wx()
    # splits = []
    # splits.append('read.php?tid=5325290')
    # splits.append('&fpage=1')
    # str = str(splits[1])
    # print(str[1:])

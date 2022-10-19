from bs4 import BeautifulSoup

from learn.contants.Constant import CARWER_1024_WENXUE_FILE
from learn.utils.Response import getResponse, getHtml

# 列表页：https://cl.5837x.xyz/thread0806.php?fid=20
# 详情页：https://cl.5837x.xyz/htm_data/2210/20/5323656.html

# 多篇： https://cl.5837x.xyz/htm_data/2210/20/5325290.html
# https://cl.5837x.xyz/read.php?tid=5325290&page=2&fpage=1
# https://cl.5837x.xyz/read.php?tid=5325290&page=3&fpage=1

LIST_NAME = "文学列表页面"
LIST_URL = "https://cl.5837x.xyz/thread0806.php?fid=20"


def getFileName(name):
    return CARWER_1024_WENXUE_FILE + name + ".txt"


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
        # wx_chapter
        chapter_spans = item_HTML.select(".thread_page")
        if (len(chapter_spans) != 0):
            chapter_span = chapter_spans[0]
            chapter_a_list = chapter_span.find_all("a")
            for chapter_a in chapter_a_list:
                chapter_url = chapter_a["href"]
                chapter_urls.append(chapter_url)
        record = Item(wx_name, wx_admin_page_url, chapter_urls)
        result_list.append(record)
        # print(f"记录名称:[{wx_name}] url:[{wx_admin_page_url}] 章节为:[{chapter_urls}]")
    return result_list


def download_wx():
    global LIST_URL, LIST_NAME
    # 获取当前要访问的页面的所有节点记录
    result_list = crawer_list(LIST_NAME, LIST_URL)
    for item in result_list:
        print(f"记录名称:[{item.name}] url:[{item.url}] 章节为:[{item.chapter_urls}]")


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

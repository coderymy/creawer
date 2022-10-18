import ast
import hashlib
import os.path
from bs4 import BeautifulSoup

from learn.contants.Constant import CRAWER_1024_JISHU_FILE
from learn.utils.IOUtil import writeContent
from learn.utils.Response import getResponse

# content的前缀
prefix_content = "https://cl.5837x.xyz/"

MAX_REQUEST_NUM = 10


# 爬取页面列表
def crawer_List():
    pageName = "thread0806"
    url_admin = prefix_content + pageName + '.php?fid=7'
    if (checkIsExistFile(getFileName(pageName))):
        f = open(getFileName(pageName), 'r', encoding='utf-8')
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
    writeContent(str(urlList), getFileName(pageName))
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
    return CRAWER_1024_JISHU_FILE + name + ".txt"


def getHtml(name, url):
    html = ''
    if (checkIsExistFile(getFileName(name))):
        file = open(getFileName(name), 'r', encoding='utf-8')
        html = file.read()
    else:
        html = getResponse(url)
        writeContent(html, getFileName(name))
    return html


def download_page():
    global MAX_REQUEST_NUM
    # 获取下载列表的url
    urlList = crawer_List()
    if (len(urlList) == 0):
        print("获取首页列表失败")
        return
    totalNum = len(urlList)
    print("开始下载，下载数量为[" + str(len(urlList)) + "]")
    succNum = 1
    for (name, url) in urlList.items():
        # 控制访问次数
        if (succNum >= MAX_REQUEST_NUM):
            return;
        if (url[-4:] == 'html'):
            content = crawer_content(name, url)
            if (len(content) == 0):
                # 获取的字符串为空
                continue
            writeContent("【第" + str(succNum) + "章】" + name, CRAWER_1024_JISHU_FILE + "[合集].txt")
            writeContent(content, CRAWER_1024_JISHU_FILE + "[合集].txt")
            succNum += 1
            print("下载成功【" + name + "】：" + url)
        else:
            # TODO 后续增加识别
            print("下载失败：不识别该url：" + url)
    print(f"下载完成，成功数量：[{succNum}]，失败数量[{totalNum - succNum}]")


if __name__ == '__main__':
    download_page()

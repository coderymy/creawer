import os.path
from bs4 import BeautifulSoup
from learn.contants.Constant import CRAWER_1024_JISHU_FILE, CRAWER_1024_DGE_FILE, CRAWER_1024_FILE, \
    CRAWER_1024_TW_FILE
from learn.markdown.htmlToMd import htmlToMarkdown
from learn.sql.MySqlUtils import insertContent, insertContentPic
from learn.sql.Tables import Content, Content_pic
from learn.utils.IOUtil import writeContent, writeContentNotRept
from learn.utils.Md5 import MD5
from learn.utils.Response import getResponse, getHtml, getSoupAndSaveCache
from crawer_1024_pic import crawer_picture, getSuffixName, getResouceAndDownloadPic

# content的前缀
prefix_content = "https://cl.5837x.xyz/"
# 范围获取
REQUEST_RANGE = "5-100"


# 爬取页面列表
def crawer_List(url_admin):
    pageName = MD5(url_admin)
    soup = getSoupAndSaveCache("技术列表页", url_admin)
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
    return urlList


# 爬取具体的列表的内容信息
def crawer_content(name, url, currentNum, succNum, totalNum):
    soup = getSoupAndSaveCache(name, url)
    content = soup.select('#conttpc')[0].text
    writeContent("【第" + str(succNum) + "章】" + name, CRAWER_1024_JISHU_FILE + "[合集].txt")
    writeContent(content, CRAWER_1024_JISHU_FILE + "[合集].txt")
    print(f"文档下载成功，第[{str(currentNum)}]个，共[{totalNum}]个 ： [{name}]")
    db_content = Content("技术分享页面", name, soup.select(".tpc_content.do_not_catch")[0])
    id = insertContent(db_content)
    crawer_picture(name, url, id)
    return content


def crawer_content_md(name, url, path):
    # 从缓存及网络上下载整个页面的html文件
    soup = getSoupAndSaveCache(name, url)
    # 解析出来整体需要的content部分html信息
    content = soup.select('#conttpc')[0]
    # 从content中找到所有的img标签
    img_labels = content.find_all("img")
    # 替换整体content里面的&amp;，防止后续替换的时候出现找不到的问题
    html_content = str(content).replace("&amp;", "&")
    print(f"开始下载 [{name}]")
    # 保存content页到mysql中（可不要，主要是为了后续分析使用）
    db_content = Content("技术分享页面", name, soup.select('#conttpc')[0])
    id = insertContent(db_content)
    i = 0
    for img_label in img_labels:
        i += 1
        # 找到该条标签的url
        pic_url = img_label['ess-data']
        # 获取url的结尾（获取文件的后缀）
        suffix_name = getSuffixName(pic_url)

        # 从缓存获取/从网络获取并保存下来图片
        download_result = getResouceAndDownloadPic(name + str(i), pic_url, suffix_name)
        if (len(download_result) == 0):
            print(name + f" 第{str(i)}张下载失败，共{str(len(img_labels))}张")
            continue
        print(name + f" 第{str(i)}张下载成功，共{str(len(img_labels))}张")

        # 将原本html中ess-data后面的图片的网络链接替换成当前文件的本地相对路径（方便后续md文件获取使用）
        html_content = html_content.replace(pic_url, "../" + download_result)
        # 将该条图片的基本信息保存到mysql中，后于后续的分析使用
        db_content_pic = Content_pic(id, name, str(img_label), pic_url, MD5(pic_url), "../" + download_result)
        insertContentPic(db_content_pic)
    # 将img标签里面的ess-data属性替换成src，因为后续使用的html->markdown的库不认识这个属性名称
    html_content = html_content.replace("ess-data", "src")
    # 将html转换成md文件
    item_markdown = htmlToMarkdown(html_content)
    # 保存md文件
    name = name.replace(" ", "")
    writeContentNotRept(item_markdown, path + name + ".md")


def download_page(url_admin, save_path):
    global REQUEST_RANGE
    # 获取下载列表的url
    urlList = crawer_List(url_admin)
    if (len(urlList) == 0):
        return
    currentNum = 0
    succNum = 1
    min = int(REQUEST_RANGE.split("-")[0])
    max = int(REQUEST_RANGE.split("-")[1])
    print(f"开始下载，总数为为[{str(len(urlList))}]，目标下载数量为[{str(max - min)}]")
    for (name, url) in urlList.items():
        currentNum += 1
        # 控制访问次数
        if (currentNum > max or currentNum < min):
            continue
        if (url[-4:] != 'html'):
            # TODO 后续增加识别
            print("下载失败：不识别该url：" + url)
            continue
        # crawer_content(name, url, currentNum, succNum, str(len(urlList)))
        try:
            crawer_content_md(name, url, save_path)
        except BaseException as err:
            print(f"{name}下载异常")
        succNum += 1
    print(f"下载完成...共[{str(len(urlList))}]，下载成功[{str(succNum)}]")


def deleteListCache():
    os.remove("cache/" + MD5("技术列表页") + ".txt")


if __name__ == '__main__':
    # dge_url = "https://cl.5837x.xyz/thread0806.php?fid=7&search=digest&page=2"
    # # https://cl.5837x.xyz/thread0806.php?fid=7&search=digest&page=2
    # save_path = CRAWER_1024_TW_FILE
    # # url = "https://cl.5837x.xyz/thread0806.php?fid=7"
    # download_page(dge_url, "图文精华/")
    # deleteListCache()

    crawer_content_md("精心为你挑选的GIF动态图，附图片出处！","https://cl.5837x.xyz/htm_mob/1312/7/1008535.html","图文精华/")



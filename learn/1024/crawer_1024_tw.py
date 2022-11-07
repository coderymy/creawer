import os.path
import threading

from learn.markdown.htmlToMd import htmlToMarkdown
from learn.utils.IOUtil import writeContent, writeContentNotRept
from learn.utils.Md5 import MD5
from learn.utils.Response import getResponse, getHtml, getSoupAndSaveCache
from crawer_1024_pic import crawer_picture, getSuffixName, getResouceAndDownloadPic, \
    getPicFileName

# content的前缀
prefix_content = "https://cl.9706x.xyz/"
# 范围获取
REQUEST_RANGE = "0-200"

MAX_THREADS = 10


# 爬取页面列表
def crawer_List(url_admin):
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
    pictures = []
    i = 0
    for img_label in img_labels:
        i += 1
        # 找到该条标签的url
        pic_url = img_label['ess-data']
        # 获取url的结尾（获取文件的后缀）
        suffix_name = getSuffixName(pic_url)
        pic = picture(name + str(i), pic_url, suffix_name, str(len(img_labels)), str(i))
        pictures.append(pic)
        # 将原本html中ess-data后面的图片的网络链接替换成当前文件的本地相对路径（方便后续md文件获取使用）
        html_content = html_content.replace(pic_url, "../" + getPicFileName(str(MD5(name + str(i))), suffix_name))
    # 创建多个线程去获取图片集合中的数据
    parallel_download_pic(pictures)

    # 将img标签里面的ess-data属性替换成src，因为后续使用的html->markdown的库不认识这个属性名称
    html_content = html_content.replace("ess-data", "src")

    # 将html转换成md文件
    item_markdown = htmlToMarkdown(html_content)

    # 保存md文件
    name = name.replace(" ", "")
    writeContentNotRept(item_markdown, path + name + ".md")


def parallel_download_pic(pictures):
    if (len(pictures) == 0):
        return ''
    global MAX_THREADS
    # 按照设置的线程上限数量拆分成对应数组的数据
    everyThreadNums = int(len(pictures) / MAX_THREADS)
    i = 0
    thread_list = []
    while (i <= MAX_THREADS + 1):
        items = pictures[int(i * everyThreadNums):int((i + 1) * everyThreadNums)]
        thread = down_pic_thread(i, items)
        thread_list.append(thread)
        thread.start()
        i += 1
    for thread_item in thread_list:
        thread_item.join()
    return


class down_pic_thread(threading.Thread):
    def __init__(self, threadID, pictures):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.pictures = pictures

    def run(self):
        for item in self.pictures:
            download_result = getResouceAndDownloadPic(item.name, item.pic_url, item.suffix_name)
            if (len(download_result) == 0):
                print(
                    f"线程[{self.threadID}]" + item.name + f" 第{str(item.index)}张下载失败，共{str(item.total_pic)}张")
            else:
                print(
                    f"线程[{self.threadID}]" + item.name + f" 第{str(item.index)}张下载成功，共{str(item.total_pic)}张")


class picture:
    name = ''
    pic_url = ''
    suffix_name = ''
    total_pic = ''
    # 第多少张图片
    index = 0

    def __init__(self, name, pic_url, suffix_name, total_pic, index):
        self.name = name
        self.pic_url = pic_url
        self.suffix_name = suffix_name
        self.total_pic = total_pic
        self.index = index


def download_page(url_admin, save_path):
    deleteListCache()
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
        try:
            crawer_content_md(name, url, save_path)
        except BaseException as err:
            print(f"{name}下载异常")
        succNum += 1
    print(f"下载完成...共[{str(len(urlList))}]，下载成功[{str(succNum)}]")


def deleteListCache():
    if os.path.exists("cache/" + MD5("技术列表页") + ".txt"):
        os.remove("cache/" + MD5("技术列表页") + ".txt")


if __name__ == '__main__':
    # TODO 自动修改域名
    download_page("https://cl.9706x.xyz/thread0806.php?fid=7&search=599498", "车牌AV/")
    # download_page("https://cl.9706x.xyz/thread0806.php?fid=7&search=599498&page=2", "车牌AV/")
    # download_page("https://cl.9706x.xyz/thread0806.php?fid=7&search=616687", "林深时见鹿/")
    # download_page("https://cl.9706x.xyz/thread0806.php?fid=7&search=269587", "一夜精品/")
    # download_page("https://cl.9706x.xyz/thread0806.php?fid=7&search=219330", "乱世虾米/")
    # download_page("https://cl.9706x.xyz/thread0806.php?fid=7&search=281581", "番号动图/")
    # download_page("https://cl.9706x.xyz/thread0806.php?fid=7&search=569641", "趣图/")

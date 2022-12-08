# 爬取当前搜索项所有页的标题
from learn.utils.IOUtil import writeContentNotRept
from learn.utils.Response import getSoupAndSaveCache

# content的前缀
prefix_content = ""
MAX_PAGE = 100


def download_all_pages(name, url_admin, path):
    global MAX_PAGE
    global REQUEST_RANGE, prefix_content
    prefix_content = url_admin.split("thread")[0]
    # 使用url解析出来当前页面的所有url
    soup = getSoupAndSaveCache(url_admin, url_admin)
    if (len(soup) == 0):
        return
    total_page_num = int(soup.select(".w70")[0].select("input")[0]['value'].split("/")[1])
    title_list = ''
    i = 0
    while (i <= total_page_num and i <= MAX_PAGE):
        i += 1
        # https://cl.2718x.xyz/thread0806.php?fid=25&search=410491
        # https://cl.2718x.xyz/thread0806.php?fid=25&search=410491&page=2
        if (i == 1):
            url = url_admin
        else:
            url = url_admin + f"&page={int(i)}"
        print(f"开始读取第{i}页，共[{total_page_num}]页")
        try:
            page_title_list = get_page_title(url)
            if (len(page_title_list) == 0):
                continue
            title_list += page_title_list
        except BaseException:
            continue

    writeContentNotRept(str(title_list), path + name + ".txt")


def get_page_title(url):
    soup = getSoupAndSaveCache(url, url)
    if (len(soup) == 0):
        print(f"获取数据页面[{url}]失败")
        return ''
    print(f"获取数据页面[{url}]成功")
    contents = soup.select("#tbody")[0]
    urlList = ''
    for item in contents:
        if (item == "\n"):
            continue
        a_label = item.select('.tal')[0].a
        url = prefix_content + a_label['href']
        name = a_label.text
        name = name.replace('\xa0', '').replace('/', '-')
        # urlList += name + "        " + url + "\n"
        # 使用关键词获取
        if ("yy" in name) or ("侄女" in name) or ("游游" in name):
            urlList += name + "        " + url + "\n"

    return urlList


if __name__ == '__main__':
    download_all_pages("国产原创", "https://cl.2718x.xyz/thread0806.php?fid=25", "title/")
    # download_all_pages("在綫成人影院", "https://cl.2718x.xyz/thread0806.php?fid=22", "title/")
    download_all_pages("HTTP下载", "https://cl.2718x.xyz/thread0806.php?fid=21", "title/")
    # download_all_pages("技术讨论", "https://cl.2718x.xyz/thread0806.php?fid=7", "title/")
    # download_all_pages("新时代的我们", "https://cl.2718x.xyz/thread0806.php?fid=8", "title/")
    # download_all_pages("達蓋爾的旗幟", "https://cl.2718x.xyz/thread0806.php?fid=16", "title/")
    print("读取完毕")

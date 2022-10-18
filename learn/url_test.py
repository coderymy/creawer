# 链接测试
from bs4 import BeautifulSoup

from learn.crawer_1024_jishu import getHtml





# 爬取具体的列表的内容信息
def crawer_content(name, url):
    html = getHtml(name, url)
    if (len(html) == 0):
        return ""
    soup = BeautifulSoup(html, "html.parser")  # BeautifulSoup解析html
    title_text = soup.title.text
    if (title_text == " 無法找到頁面 草榴社區 " or title_text == "403 Forbidden"):
        print("下载失败：" + name + ":404")
        return ""
    content = soup.select(".tpc_content.do_not_catch")[0].text
    # https://cl.5837x.xyz/htm_data/2210/7/5334981.html
    return content


if __name__ == '__main__':
    url = "https://cl.5837x.xyz/htm_data/2210/7/5334981.html"
    crawer_content("aaa", url)
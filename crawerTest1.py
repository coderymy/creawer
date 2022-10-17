import urllib.request
from bs4 import BeautifulSoup
if __name__ == "__main__":
    url = "http://www.baidu.com"
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': 'gzip',
    }  # 初始使用的header
    rq = urllib.request.Request(url, header)
    print(rq)
    resp = urllib.request.urlopen(rq)
    print(resp)
    html = resp.read().decode('gbk')
    print(html)
    soup = BeautifulSoup(html)
    print(soup)



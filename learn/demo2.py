import re
import time
import requests
from bs4 import BeautifulSoup

from learn.utils.IOUtil import writeContent


def getResponse(baseurl):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
        "cookie": "Hm_lvt_af43f8d0f4624bbf72abe037042ebff4=1640837022; __gads=ID=a34c31647ad9e765-22ab388e9bd6009c:T=1637739267:S=ALNI_MYCjel4B8u2HShqgmXs8VNhk1NFuw; __utmc=66375729; __utmz=66375729.1663684462.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gpi=UID=000004c822cf58b2:T=1649774466:RT=1663684463:S=ALNI_Ma3kL14WadtyLP-_lSQquhy_w85ag; __utma=66375729.1148601284.1603116839.1663684462.1663687392.2; .Cnblogs.AspNetCore.Cookies=CfDJ8NfDHj8mnYFAmPyhfXwJojexiKc4NcOPoFywr0vQbiMK4dqoay5vz8olTO_g9ZwQB7LGND5BBPtP2AT24aKeO4CP01olhQxu4EsHxzPVjGiKFlwdzRRDSWcwUr12xGxR89b_HFIQnmL9u9FgqjF6CI8canpEYxvgxZlNjSlBxDcWOzuMTVqozYVTanS-vAUSOZvdUz8T2XVahf8CQIZp6i3JzSkaaGUrXzEAEYMnyPOm5UnDjXcxAW00qwVmfLNW9XO_ITD7GVLrOg-gt7NFWHE29L9ejbNjMLECBdvHspokli6M78tCC5gmdvetlWl-ifnG5PpL7vNNFGYVofGfAZvn27iOXHTdHlEizWiD83icbe9URBCBk4pMi4OSRhDl4Sf9XASm7XKY7PnrAZTMz8pvm0ngsMVaqPfCyPZ5Djz1QvKgQX3OVFpIvUGpiH3orBfr9f6YmA7PB-T62tb45AZ3DB8ADTM4QcahO6lnjjSEyBVSUwtR21Vxl0RsguWdHJJfNq5C5YMp4QS0BfjvpL-OvdszY7Vy6o2B5VCo3Jic; .CNBlogsCookie=71474A3A63B98D6DA483CA38404D82454FB23891EE5F8CC0F5490642339788071575E9E95E785BF883C1E6A639CD61AC99F33702EF6E82F51D55D16AD9EBD615D26B40C1224701F927D6CD4F67B7375C7CC713BD; _ga_3Q0DVSGN10=GS1.1.1663687371.1.1.1663687557.1.0.0; Hm_lvt_866c9be12d4a814454792b1fd0fed295=1662692547,1663250719,1663417166,1663687558; Hm_lpvt_866c9be12d4a814454792b1fd0fed295=1663687558; _ga=GA1.2.1148601284.1603116839; _gid=GA1.2.444836177.1663687558; __utmt=1; __utmb=66375729.11.10.1663687392"}
    response = requests.get(baseurl, headers=head) # 获取网页信息
    response.encoding = 'utf-8'
    html = response.text
    return html

def crawer():
    url = "http://www.tstdoors.com/ldks/11854/4373905.html"
    html =getResponse(url)
    soup = BeautifulSoup(html, "html.parser")  # BeautifulSoup解析html
    name_html=soup.select('#content >h1')[0].string
    content_html=soup.select('.content')[0].text
    writeContent(content_html,name_html)



if __name__ == "__main__":
    crawer()

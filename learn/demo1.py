import requests
import parsel


# 爬取这个https://www.xygwh.cc/4/4446/39994695.html，并且IO写入文件中
def crawer():
    url = "http://www.tstdoors.com/ldks/11854/4373905.html"
    # 获取url的访问结果
    response = requests.get(url)
    # 访问结果中的文本信息
    responses = response.text
    # 创建选择器
    selector = parsel.selector.Selector(responses)
    # 使用css的class选择器，获取其中标签的text文本
    name= selector.css("#content > h1::text").getall()
    content_text=selector.css(".content::text").getall()
    # 加入换行
    content = '\n'.join(content_text)
    # 文本输出
    print(name[0])
    print(content)
    # 保存：



if __name__ == "__main__":
    crawer()

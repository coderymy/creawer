# 这里将每张表定义成一个类
class Content:
    id = 0
    list_num = ''
    title = ''
    content = ''
    # html = ''

    def __init__(self, list_num, title, content):
        self.list_num = list_num
        self.title = title
        self.content = content


# 这里将每张表定义成一个类
class Content_pic:
    id = 0
    content_id = 0
    content_name = ''
    pic_html = ''
    pic_url = ''
    pic_encode = ''
    pic_save_address = ''

    def __init__(self, content_id, content_name, pic_html, pic_url, pic_encode, pic_save_address):
        self.content_id = content_id
        self.content_name = content_name
        self.pic_html = pic_html
        self.pic_url = pic_url
        self.pic_encode = pic_encode
        self.pic_save_address = pic_save_address

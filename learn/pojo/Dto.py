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
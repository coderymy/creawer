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

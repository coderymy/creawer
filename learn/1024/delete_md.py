import os


def delete_md(list, directoryName):
    # 获取该文档所有信息
    # 获取以![](开头的后续结构
    # 删除图片
    # 删除文档
    for name in list:
        fileName = directoryName + name
        if (os.path.exists(fileName) and name != '.DS_Store'):
            file = open(fileName, "r", encoding="utf-8")
            for line in file.readlines():
                if (line.startswith("![](") and len(line) > 10):
                    picture_address = line[7:].split(")")[0]
                    # print(picture_address)
                    if (os.path.exists(picture_address)):
                        os.remove(picture_address)
            os.remove(fileName)
            print(f"{name}删除成功")
            # os.remove("")


# 删除文档，并删除文档中的所有图片
if __name__ == '__main__':
    # jh_remove_list = ['[原创分享]社区资深女榴友来袭~本人女，爱好男！！[13P].md']
    # jh_directory_name = "图文精华/"
    # base_js_remove_list = ['[花和尚撸自身]好想上老師的課！精選《１５部女教師謎片》，带番號！[27P].md','[流年堪忆]走向性麻木之遗失在时光里的人妻或女儿[88P].md',]
    # base_js_directory_name = "crawer_1024_js_file/"
    # dge_remove_list = ['性感小女友[11P].md',
    #                    '销魂的姿势[10P].md',
    #                    '下火的少妇[17P].md',
    #                    '我的骚逼妻子[22P].md',
    #                    '外面遇到的大洋马[10P].md',
    #                    '情趣大网骚妻[15P].md',
    #                    '前女友，后续还有，条纹衫验证。[14P].md',
    #                    '廊坊M圈里的奈儿[36P].md',
    #                    '发个骚老婆的日常[12P].md',
    #                    '不想搭理她但是老缠着我[17P].md']
    # dge_directory_name = "crawer_1024_dge_file/"
    # delete_md(jh_remove_list, jh_directory_name)
    # delete_md(base_js_remove_list, base_js_directory_name)
    # delete_md(dge_remove_list, dge_directory_name)
    for root, dirs, files in os.walk("图文精华/"):
        delete_md(files, "图文精华/")

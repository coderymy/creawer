import os


def delete_md(list, directoryName):
    # 获取该文档所有信息
    # 获取以![](开头的后续结构
    # 删除图片
    # 删除文档
    for name in list:
        fileName = directoryName + name
        if (os.path.exists(fileName)):
            file = open(fileName, "r", encoding="utf-8")
            for line in file.readlines():
                if (line.startswith("![](") and len(line) > 10):
                    picture_address = line[7:].split(")")[0]
                    # print(picture_address)
                    if (os.path.exists(picture_address)):
                        os.remove(picture_address)
            os.remove(fileName)
            # os.remove("")


# 删除文档，并删除文档中的所有图片
if __name__ == '__main__':
    jh_remove_list = ['[原创分享]社区资深女榴友来袭~本人女，爱好男！！[13P].md',
                      '[原创]新手如何赚U起步.md',
                      '[原创分享]大学生活真好，疫情在家，分享一下经常约的大学生妹子[20P].md',
                      '[原创分享]带着女神去找男技师，分享一下我睡到的女神[50P].md',
                      '[原创分享]带着我的摄影师，为榴友献出我的身体[40P].md',
                      '[原创分享]分享自己小母狗的一些片段[28P].md',
                      '[原创分享]和自己加的小女友来一次户外露出的体验[15P].md',
                      '[原创分享]社区资深女榴友，每个人都渴望的乖嫩骚宝贝送给大家[21P].md',
                      '[原创分享]说下我亲身经历的乱伦，警醒下想要乱伦的人[9P].md',
                      '[原创分享]我的妻子愿意分享自己的身体[27P].md',
                      '[原创byfreemanlee7][流年踏歌]之二，山高水远，主播有闲，打着飞的来相见[76P].md',
                      '草榴社区注册会员使用手册[2022版].md',
                      '疯狂的318续篇(发布行程约妹方法)私信暴了，结语往期福利.md',
                      '求版主删除.md',
                      '我和草榴的十年故事（5.23更新）.md',
                      '[图文故事]唐门风云淫劫录.序章——风云动荡篇——动态gif原创故事剧情无码长篇图文大剧.md',
                      '[原创]小骚骚又来咯.这次的图片顺序小骚骚都编好号啦,技术男上线[117P].md'
                      ]
    jh_directory_name = "图文精华/"

    base_js_remove_list = ['[花和尚撸自身]好想上老師的課！精選《１５部女教師謎片》，带番號！[27P].md','[流年堪忆]走向性麻木之遗失在时光里的人妻或女儿[88P].md',]
    base_js_directory_name = "crawer_1024_js_file/"

    dge_remove_list = ['性感小女友[11P].md',
                       '销魂的姿势[10P].md',
                       '下火的少妇[17P].md',
                       '我的骚逼妻子[22P].md',
                       '外面遇到的大洋马[10P].md',
                       '情趣大网骚妻[15P].md',
                       '前女友，后续还有，条纹衫验证。[14P].md',
                       '廊坊M圈里的奈儿[36P].md',
                       '发个骚老婆的日常[12P].md',
                       '不想搭理她但是老缠着我[17P].md']
    dge_directory_name = "crawer_1024_dge_file/"

    delete_md(jh_remove_list, jh_directory_name)
    delete_md(base_js_remove_list, base_js_directory_name)
    delete_md(dge_remove_list, dge_directory_name)

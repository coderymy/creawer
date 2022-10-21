import hashlib
import time


def MD5(content):
    # 输入加密内容
    MD5 = hashlib.md5()
    MD5.update(content.encode(encoding='utf-8'))
    md5_content = MD5.hexdigest()
    return md5_content


if __name__ == '__main__':
    print(MD5("最近发生的两件事：被电信套餐坑了一把，小区少妇约炮被抓奸[1P]1"))

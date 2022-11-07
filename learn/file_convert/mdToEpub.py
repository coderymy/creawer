import os

if __name__ == '__main__':
    directory = "../cl/车牌AV/"
    # 调整当前工作目录
    os.chdir(directory)
    os.mkdir("pdf/") if not os.path.exists("pdf/") else 1 + 1
    for root, dirs, files in os.walk('./'):
        for file in files:
            if (file != '.DS_Store'):
                os.system(f"pandoc -s {file} -o {'pdf/' + file.replace('md', 'epub')}")
        # 为什么break?，为了让os.walk只关注当前文件夹，而不关注子文件夹
        break

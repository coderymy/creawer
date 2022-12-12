import os

if __name__ == '__main__':
    directory = "../cl/a/"
    # 调整当前工作目录
    os.chdir(directory)
    os.mkdir("epub/") if not os.path.exists("epub/") else 1 + 1
    for root, dirs, files in os.walk('./'):
        for file in files:
            if os.path.exists(f"epub/{file.replace('md', 'epub')}"):
                continue
            if (file != '.DS_Store'):
                os.system(f"pandoc -s {file} -o {'epub/' + file.replace('md', 'epub')}")
                print(f"{file}转换成功")
        # 为什么break?，为了让os.walk只关注当前文件夹，而不关注子文件夹
        break

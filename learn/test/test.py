MAX_THREAD = ''


def getMAX_THREAD():
    global MAX_THREAD
    MAX_THREAD=MAX_THREAD+"aaa"
    print(MAX_THREAD)
    return MAX_THREAD


def aaa():
    global  MAX_THREAD
    print(MAX_THREAD)
if __name__ == '__main__':
    print(int(9 / 10))

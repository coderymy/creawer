from pymysql.err import IntegrityError

import pymysql

from learn.sql.Tables import Content

URL = "localhost"
USERNAME = "root"
PASSWORD = "Ymy123321."
DATABASE = "py_crawer"


def getDbCursor():
    global URL, USERNAME, PASSWORD, DATABASE
    conn = pymysql.connect(host=URL, port=3306, user=USERNAME, password=PASSWORD, charset='utf8', db=DATABASE)
    return conn.cursor(cursor=pymysql.cursors.DictCursor)


def insertContent(content):
    global URL, USERNAME, PASSWORD, DATABASE
    conn = pymysql.connect(host=URL, port=3306, user=USERNAME, password=PASSWORD, charset='utf8', db=DATABASE)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    try:
        sql = "insert into tb_content(list_num,title,content) value (%s,%s,%s) "
        cursor.execute(sql, [content.list_num, content.title, content.content])
        conn.commit()
        id = cursor.lastrowid
    except IntegrityError:
        selectSql = "select id from tb_content where title=%s"
        cursor.execute(selectSql, content.title)
        id = cursor.fetchone()['id']
        cursor.close()
        conn.close()
        return id
    return id


def insertContentPic(contentPic):
    global URL, USERNAME, PASSWORD, DATABASE
    conn = pymysql.connect(host=URL, port=3306, user=USERNAME, password=PASSWORD, charset='utf8', db=DATABASE)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        sql = "insert into tb_content_pic(content_id,content_name,pic_html,pic_url,pic_encode,pic_save_address) value (%s,%s,%s,%s,%s,%s) "
        cursor.execute(sql, [contentPic.content_id, contentPic.content_name, contentPic.pic_html, contentPic.pic_url,
                             contentPic.pic_encode,
                             contentPic.pic_save_address])
        conn.commit()
        cursor.close()
        conn.close()
    except IntegrityError:
        cursor.close()
        conn.close()

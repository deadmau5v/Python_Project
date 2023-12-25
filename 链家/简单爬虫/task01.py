"""
task01: 爬虫 获取URL
"""

import requests
import bs4
import pymysql

# 数据库
mysql = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456")
mysql.autocommit(True)  # 自动提交
cursor = mysql.cursor()

# 创建链接数据库 创立初始表
cursor.execute("create database if not exists lianjia")
cursor.execute("use lianjia")

cursor.execute("create table if not exists urls (url varchar(255))")

for i in range(100):
    # 设置url
    url = "https://zhuzhou.lianjia.com/ershoufang/pg" + str(i + 1)

    # 发送请求
    res = requests.get(url)

    # 使用bs4库中的 BeautifulSoup类 解析请求到的网页 保存到html变量中
    html = bs4.BeautifulSoup(res.text, "html.parser")

    # 在页面中找到ul标签 （ul标签中包含li标签，li标签就是二手房的卡片）
    ul = html.find(name="ul", attrs={"class": "sellListContent"})

    # 从ul中 找到所有li 保存到 lis变量
    lis = ul.find_all(name="li", attrs={"class": "LOGCLICKDATA"})

    # 循环li标签
    for l in lis:
        # 找到a标签 提取链接
        url = l.find(name="a")["href"]

        # 打印提取到的链接
        print(url)

        # 把链接保存到 urls 数据库
        cursor.execute("insert ignore into urls values ('%s')" % url)


# 断开数据库
cursor.close()
mysql.close()

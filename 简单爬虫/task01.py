"""
task01: 爬虫 获取URL
"""


import requests
import bs4

for i in range(71):
    # 设置url
    url = "https://cm.lianjia.com/ershoufang/pg" + str(i + 1)

    # 发送请求
    res = requests.get(url)

    # 使用bs4库中的 BeautifulSoup类 解析请求到的网页 保存到html变量中
    html = bs4.BeautifulSoup(res.text, "html.parser")

    # 在页面中找到ul标签 （ul标签中包含li标签，li标签就是二手房的卡片）
    ul = html.find(name="ul", attrs={"class": "sellListContent"})

    # 从ul中 找到所有li 保存到 lis变量
    lis = ul.find_all(name="li", attrs={"class": "LOGCLICKDATA"})

    # 循环li标签
    for i in lis:
        # 找到a标签 提取链接
        url = i.find(name="a")["href"]

        # 打印提取到的链接
        print(url)

        # 把链接保存到 urls.txt
        with open("urls.txt", "a") as f:
            # 写入链接 并换行
            f.write(url + "\n")


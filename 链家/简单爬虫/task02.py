"""
task02: 爬虫 获取详细
"""

import requests
import bs4
import pymysql

mysql = pymysql.Connect(host="127.0.0.1", port=3306, user="root", passwd="123456")
mysql.autocommit(True)

cursor = mysql.cursor()
cursor.execute("use lianjia")
cursor.execute("""
create table if not exists data (
    id int primary key auto_increment,
    金额 varchar(10),
    房屋户型 varchar(10),
    所在楼层 varchar(10),
    建筑面积 varchar(10),
    户型结构 varchar(10),
    套内面积 varchar(10),
    建筑类型 varchar(10),
    房屋朝向 varchar(10),
    建筑结构 varchar(10),
    装修情况 varchar(10),
    梯户比例 varchar(10),
    配备电梯 varchar(10),
    所在区域 varchar(10),
    别墅类型 varchar(10),
    用水类型 varchar(10)
) charset=utf8;
""")

# 表头
columns = ["金额", "房屋户型", "所在楼层", "建筑面积", "户型结构", "套内面积", "建筑类型", "房屋朝向", "建筑结构",
           "装修情况",
           "梯户比例", "配备电梯", "所在区域"]

cursor.execute("select * from lianjia.urls")
urls = cursor.fetchall()

for i in urls:

    # 删掉链接结尾的换行符
    i = i[0].replace("\n", "")

    # 发送请求
    res = requests.get(i)

    # 解析整个页面
    html = bs4.BeautifulSoup(res.text, "html.parser")

    # 储存这个页面信息的字典
    lis_attrs = {}

    # 找到总金额
    total = html.find(name="span", attrs={"class": "total"})
    if total is not None:
        total = total.text
        lis_attrs["金额"] = total

    # 所在区域
    areaName = html.find(name="div", attrs={"class": "areaName"})
    if areaName is not None:
        areaName = areaName.find(name="a").text
        lis_attrs["所在区域"] = areaName

    # 找到所有属性 添加到attrs表中
    try:
        lis = html.find(name="div", attrs={"class": "base"}).find(
            name="ul").find_all(name="li")
    except:
        continue

    for x in lis:
        lis_attrs[x.text[:4]] = x.text[4:]

    # 找到所有属性 添加到mysql表中
    sql = f"""insert into lianjia.data ({ ','.join(lis_attrs.keys()) }) values ({
        ','.join(['"' + x + '"' for x in lis_attrs.values()])
    })"""
    print(sql)
    try:
        cursor.execute(sql)
    except:
        continue

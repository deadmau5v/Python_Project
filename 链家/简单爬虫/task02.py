"""
task02: 爬虫 获取详细
"""


import requests
import bs4
import pandas

with open("./.tmp/urls.txt", "r") as f:
    # 读取爬到的url
    urls = f.readlines()

# 表头
columns = ["金额", "房屋户型", "所在楼层", "建筑面积", "户型结构", "套内面积", "建筑类型", "房屋朝向", "建筑结构", "装修情况",
           "梯户比例", "配备电梯", "所在区域"]
attrs = pandas.DataFrame(columns=columns)  # 新建空DataFrame 将li数据存入这个字典

with open("./.tmp/data.csv", "w") as f:
    pass

for i in urls:
    "判断一下i是否为空 防止请求空行"
    if i != '':
        # 删掉链接结尾的换行符
        i = i.replace("\n", "")

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
        attrs.loc[len(attrs)] = lis_attrs
        print(lis_attrs)  # 打印一下

        # 保存到 data.csv文件
        attrs.to_csv("./.tmp/data.csv", index=False)

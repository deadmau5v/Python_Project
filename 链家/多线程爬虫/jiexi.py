#import pandas
import requests
import bs4

with open("urls.txt", "r") as f:
    urls = f.readlines()
columns = ["金额(万)", "每平米价格(元/平米)", "小区名称", "房屋户型", "所在楼层", "建筑面积", "户型结构", "套内面积", "建筑类型", "房屋朝向", "建筑结构", "装修情况",
           "梯户比例", "配备电梯"]
#attrs = pandas.DataFrame(columns=columns)
for i in urls:
    if i != '':
        i = i.replace("\n", "")
        res = requests.get(i)
        html = bs4.BeautifulSoup(res.text, "html.parser")
        lis_attrs = {}
        total = html.find(name="span", attrs={"class": "total"}).text
        lis_attrs["金额(万)"] = total
        unitPriceValue = html.find(name="span", attrs={"class": "unitPriceValue"}).text
        lis_attrs["每平米价格(元/平米)"] = unitPriceValue
        communityName = html.find(name="div", attrs={"class": "communityName"}).find(name="a").text
        lis_attrs["小区名称"] = communityName
        lis = html.find(name="div", attrs={"class": "base"}).find(name="ul").find_all(name="li")
        for x in lis:
            lis_attrs[x.text[:4]] = x.text[4:]
        lis2 = html.find(name="div", attrs={"class": "transaction"}).find(name="ul").find_all(name="li")
        for y in lis2:
            y = y.replace("\n", "")
            lis_attrs[y.text[:4]] = y.text[4:]
        #attrs.loc[len(attrs)] = lis_attrs
        print(lis_attrs)
        exit()
#attrs.to_csv("data.csv")

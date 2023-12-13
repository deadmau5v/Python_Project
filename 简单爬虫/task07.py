"""
task07: 指标计算 《配备电梯情况的并图》
"""


import pandas
import pyecharts

# 读取
data = pandas.read_csv("data_cleared.csv")

# 筛选出异常值
data1 = data[["配备电梯"]].value_counts()
columns = [i[0] for i in data1.keys()]
data1 = data1.to_list()
print(columns)
print(data1)
# 配备电梯
# 无       1145
# 有        954

pie_data = [("无", data1[0]), ("有", data1[1])]
pie = pyecharts.charts.Pie()
pie.add("", pie_data)

pie.render("echarts4.html")

print("完成")


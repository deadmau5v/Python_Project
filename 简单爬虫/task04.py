"""
task04: 指标计算 《楼层分布的饼图》
"""


import pandas
import pyecharts

# 读取
data = pandas.read_csv("data_cleared.csv")

# 筛选出异常值
data1 = data[["所在楼层"]]

print(data1)
# 所在楼层
# 0      低楼层 (共3层)
# 1     高楼层 (共18层)
# 2     中楼层 (共16层)

data2 = data1.map(lambda x: x[0:3])
print(data2.value_counts())
# 所在楼层
# 低楼层     798
# 中楼层     726
# 高楼层     575
value_counts = data2.value_counts().to_list()

pie_data = [("低楼层", value_counts[0]), ("中楼层", value_counts[1]), ("高楼层", value_counts[2])]
pie = pyecharts.charts.Pie()

pie.add("", pie_data)

pie.render("echarts1.html")
print("完成")

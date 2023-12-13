"""
task06: 指标计算 《房源配备电梯装修情况分布的饼子柱状图》
"""


import pandas
import pyecharts

# 读取
data = pandas.read_csv("data_cleared.csv")

# 筛选出异常值
data1 = data[["装修情况"]].value_counts()
columns = [i[0] for i in data1.keys()]
print(columns)
print(data1)
# 装修情况
# 精装      868
# 其他      635
# 简装      328
# 毛坯      266

# 计算金额散点图
bar = pyecharts.charts.Bar()

bar.add_xaxis(columns)
bar.add_yaxis("数量", data1.to_list())

bar.set_global_opts(
    yaxis_opts=pyecharts.options.global_options.AxisOpts(name="房源数量"),
    xaxis_opts=pyecharts.options.global_options.AxisOpts(name="装修类型")
    )

# 保存
bar.render("echarts3.html")

print("完成")

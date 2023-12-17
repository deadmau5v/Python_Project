"""
task05: 指标计算 《金额与面积关系的散点图》
"""


import pandas
import pyecharts

# 读取
data = pandas.read_csv("data_cleared.csv")

# 筛选出异常值
data1 = data[["金额", "建筑面积"]]
data1 = data1[data1["金额"] < 500]
data1 = data1[data1["建筑面积"] < 500]

# 计算金额散点图
scatter = pyecharts.charts.Scatter()
scatter.add_xaxis(data1["金额"])
scatter.add_yaxis("二手房价格/面积", data1["建筑面积"])


# 关掉散点图上 显示的值 防止重叠
scatter.set_series_opts(
    label_opts=pyecharts.options.series_options.LabelOpts(is_show=False),
)

# 设置xy坐标的最大值 和 title
scatter.set_global_opts(
    yaxis_opts=pyecharts.options.AxisOpts(max_=data1["建筑面积"].max(), name="面积"),
    xaxis_opts=pyecharts.options.AxisOpts(max_=data1["金额"].max(), name="金额")
)

# 保存
scatter.render("echarts2.html")
print("完成")

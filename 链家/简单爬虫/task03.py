"""
task03: 数据清洗
"""


import numpy
import pandas

data = pandas.read_csv("./data.csv", index_col=0)

# 将无数据统一化
data = data.replace("暂无数据", numpy.nan)

# 删掉建筑面积单位 并转为float
data["建筑面积"] = [numpy.float64(str(i).replace("㎡", "")) for i in data["建筑面积"]]
data["套内面积"] = [numpy.float64(str(i).replace("㎡", "")) for i in data["套内面积"]]

# 是否有电梯转为 有/无 二值
data["配备电梯"] = ["有" if i == "有" else "无" for i in data["配备电梯"]]

data["梯户比例"] = data["梯户比例"].fillna("其他")
data["建筑结构"] = data["建筑结构"].fillna("其他")

data.to_csv("./data_cleared.csv", index=False)

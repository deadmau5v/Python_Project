from django.shortcuts import render
import pyecharts
import pandas

df = pandas.read_csv("./data_cleared.csv", encoding="utf-8")


def index(request):
    data = {
        "title": "主页",
        "page": "index.html"
    }
    return render(request, "base.html", data)


def echarts1(request):
    data1 = df[["所在楼层"]]
    data2 = data1.map(lambda x: x[0:3])
    value_counts = data2.value_counts().to_list()
    pie_data = [("低楼层", value_counts[0]), ("中楼层", value_counts[1]), ("高楼层", value_counts[2])]
    pie = pyecharts.charts.Pie()
    pie.add("", pie_data)
    pie.render("./templates/echarts1.html")

    data = {
        "title": "房源楼层分布图",
        "page": "echarts1.html"
    }
    return render(request, "base.html", data)


def echarts2(request):
    data1 = df[["金额", "建筑面积"]]
    data1 = data1[data1["金额"] < 500]
    data1 = data1[data1["建筑面积"] < 500]
    scatter = pyecharts.charts.Scatter()
    scatter.add_xaxis(data1["金额"])
    scatter.add_yaxis("二手房价格/面积", data1["建筑面积"])
    scatter.set_series_opts(
        label_opts=pyecharts.options.series_options.LabelOpts(is_show=False),
    )
    scatter.set_global_opts(
        yaxis_opts=pyecharts.options.AxisOpts(max_=data1["建筑面积"].max(), name="面积"),
        xaxis_opts=pyecharts.options.AxisOpts(max_=data1["金额"].max(), name="金额")
    )
    scatter.render("./templates/echarts2.html")
    data = {
        "title": "房产面积价格关系图",
        "page": "echarts2.html"
    }
    return render(request, "base.html", data)


def echarts3(request):
    data1 = df[["装修情况"]].value_counts()
    columns = [i[0] for i in data1.keys()]
    bar = pyecharts.charts.Bar()
    bar.add_xaxis(columns)
    bar.add_yaxis("数量", data1.to_list())
    bar.set_global_opts(
        yaxis_opts=pyecharts.options.global_options.AxisOpts(name="房源数量"),
        xaxis_opts=pyecharts.options.global_options.AxisOpts(name="装修类型")
    )
    bar.render("./templates/echarts3.html")
    data = {
        "title": "装修情况分布图",
        "page": "echarts3.html"
    }
    return render(request, "base.html", data)


def echarts4(request):
    data1 = df[["配备电梯"]].value_counts()
    data1 = data1.to_list()
    pie_data = [("无", data1[0]), ("有", data1[1])]
    pie = pyecharts.charts.Pie()
    pie.add("", pie_data)
    pie.render("./templates/echarts4.html")
    data = {
        "title": "电梯配套情况分布图",
        "page": "echarts4.html"
    }
    return render(request, "base.html", data)

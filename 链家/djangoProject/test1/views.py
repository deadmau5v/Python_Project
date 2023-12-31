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
    data1 = df["所在楼层"]
    # 截取楼层大概位置 比如 低楼层 中楼层 高楼层
    data2 = data1.map(lambda x: x[:3])

    value_counts = data2.value_counts().to_list()
    pie_data = [("低楼层", value_counts[0]), ("中楼层", value_counts[1]), ("高楼层", value_counts[2])]
    pie = pyecharts.charts.Pie()
    pie.add("楼层等级分布", pie_data)

    # 截取楼层的具体位置 比如 1楼 2楼 3楼
    data3 = data1.map(lambda x: x[3:])
    data3 = data3.map(lambda x: x
                      .replace("(", "")
                      .replace(")", "")
                      .replace(" ", "")
                      .replace("共", "")
                      .replace("层", "")
                      )
    data3 = data3.map(lambda x: int(x))

    # 将楼层分为5层一组
    def to_str(x):
        r = int(x / 5) * 5
        return f"{r}~{r + 5}层"
    data3 = data3.map(to_str)

    pie_2 = pyecharts.charts.Pie()
    pie_2.add("具体楼层分布", list(data3.value_counts().to_dict().items()))

    table = pyecharts.charts.Tab()
    table.add(pie, "楼层等级分布")
    table.add(pie_2, "具体楼层分布")

    table.render("./templates/echarts1.html")

    data = {
        "title": "房源楼层分布图",
        "page": "echarts1.html"
    }
    return render(request, "base.html", data)


def echarts2(request):
    data1 = df[["金额", "建筑面积", "所在区域"]]
    scatter = pyecharts.charts.Scatter()
    scatter.add_xaxis(data1["金额"])
    scatter.add_yaxis("二手房价格/面积", data1["建筑面积"])
    scatter.set_global_opts(
        xaxis_opts=pyecharts.options.global_options.AxisOpts(name="价格"),
        yaxis_opts=pyecharts.options.global_options.AxisOpts(name="面积")
    )
    tab = pyecharts.charts.Tab()
    tab.add(scatter, "全部")
    for i in set(data1["所在区域"].tolist()):
        scatter = pyecharts.charts.Scatter()
        data2 = data1[data1["所在区域"] == i]
        scatter.add_xaxis(data2["金额"])
        scatter.add_yaxis("二手房价格/面积", data2["建筑面积"].tolist())
        scatter.set_global_opts(
            xaxis_opts=pyecharts.options.global_options.AxisOpts(name="价格"),
            yaxis_opts=pyecharts.options.global_options.AxisOpts(name="面积")
        )
        tab.add(scatter, i)
    tab.render("./templates/echarts2.html")

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

    tab = pyecharts.charts.Tab()
    tab.add(bar, "全部")
    for i in set(df["所在区域"].tolist()):
        data2 = df[df["所在区域"] == i]
        data3 = data2[["装修情况"]].value_counts()
        columns = [i[0] for i in data3.keys()]
        bar = pyecharts.charts.Bar()
        bar.add_xaxis(columns)
        bar.add_yaxis("数量", data3.to_list())
        bar.set_global_opts(
            yaxis_opts=pyecharts.options.global_options.AxisOpts(name="房源数量"),
            xaxis_opts=pyecharts.options.global_options.AxisOpts(name="装修类型")
        )
        tab.add(bar, i)
    tab.render("./templates/echarts3.html")
    data = {
        "title": "装修情况分布图",
        "page": "echarts3.html"
    }
    return render(request, "base.html", data)


def echarts4(request):
    data1 = df[["所在区域"]].value_counts()
    address = ([i[0] for i in data1.index])
    pie = pyecharts.charts.Pie()
    pie.add("房源数量", list(zip(address, data1.to_list())))
    pie.render("./templates/echarts4.html")
    data = {
        "title": "房源数量分布图",
        "page": "echarts4.html"
    }
    return render(request, "base.html", data)

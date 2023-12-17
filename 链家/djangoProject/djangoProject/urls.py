from django.contrib import admin
from django.urls import path
from test1.views import index, echarts1, echarts2, echarts3, echarts4

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', index),
    path(r'echarts1', echarts1),
    path(r'echarts2', echarts2),
    path(r'echarts3', echarts3),
    path(r'echarts4', echarts4)
]

import json
from multiprocessing import Process

import requests as req
from redis import client
from bs4 import BeautifulSoup as Bs
from bs4 import Tag

db = client.Redis(host="172.17.0.2", port=6379)
db.keys()
print("连接数据库成功")

# 爬虫全局 Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}



def get_houses(page: int = 1) -> None:
    """
    获取 {page} 页的所有房源链接
    :param page: 页数
    :return: 导入到Redis
    """
    print(f"开始爬取 {page} 页")
    url = f"https://cm.lianjia.com/ershoufang/pg{page}/"
    res = req.get(
        url=url,
        headers=headers
    )
    html: Tag = Bs(res.text, "lxml")
    ul_tag: Tag = html.find(name="ul", attrs={"class", "sellListContent"})
    li_tags: list[Tag] = ul_tag.find_all(name="li")

    def get_url(li_tag: Tag) -> str:
        """
        解析出Tag对象中的URl
        :param li_tag: bs4的li 标签对象
        :return: URL
        """
        # 找到第一个a标签
        a_tag = li_tag.find(name="a")
        return a_tag.attrs["href"]

    for url in list(map(get_url, li_tags)):
        db.sadd("urls", url)


def get_max_page() -> int:
    """
    获取链家网所有房源页数
    :return: 最大页数
    """
    url = "https://cm.lianjia.com/ershoufang/"
    res = req.get(
        url=url,
        headers=headers,
    )
    html: Tag = Bs(res.text, "lxml")
    div_tag: Tag = html.find(name="div", attrs={"class": "house-lst-page-box"})
    page_data: str = div_tag.attrs["page-data"]
    page_data: dict = json.loads(page_data)
    return page_data["totalPage"]


if __name__ == '__main__':

    max_page = get_max_page()
    pool = []  # 线程池

    for page in range(max_page):
        page = page + 1
        t = Process(target=get_houses, args=(page,))
        pool.append(t)
        t.start()

    # 等待所有线程结束
    for t in pool:
        t.join()

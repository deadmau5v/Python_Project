import asyncio

import aiohttp
from redis import client
from bs4 import BeautifulSoup as Bs
from bs4 import Tag

db = client.Redis(host="192.168.25.134", port=6379)


class House:
    def __init__(self) -> None:  # <属性描述>                <示例>
        self.price: float = 0.0  # 价格                       ["63"]
        self.unit: str = ""  # 价格单位                     ["万"]

        self.price_of_m: float = 0.0  # 每平方价格       ["10345 元/平米"]

        self.type: str = ""  # 户型                 ["2室2厅1厨1卫"]
        self.floor: str = ""  # 楼层                 ["低楼层 (共18层)"]
        self.structure: str = ""  # 户型结构             ["平层"]
        self.build: str = ""  # 建筑构造             ["钢混结构"]
        self.toward: str = ""  # 朝向                 ["西南 东北"]
        self.renovation: str = ""  # 装修类型             ["精装修"]
        self.area: float = 0.0  # 面积 单位: m^2       ["95.78m^2"]
        self.have_lift: bool = False  # 是否有电梯           ["有"]

    def print(self) -> None:
        """
        调试日志
        :return: 无
        """
        print(
            "{"
            f"{self.price = :^6}, "
            f"{self.unit = }, "
            f"{self.price_of_m = :^7}, "
            f"{self.type = :^8}, "
            f"{self.floor = :^10}, "
            f"{self.structure = :^10}, "
            f"{self.build = :^10}, "
            f"{self.toward = :^10}, "
            f"{self.renovation = :^10}, "
            f"{self.area = :^10}, "
            f"{self.have_lift = }"
            "}"
        )


def li_to_dict(lis: list[Tag]):
    content = {}
    for tag in lis:
        content[tag.text[:4]] = tag.text[4:]
    return content


async def get_house_data(url):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url) as res:
            html = Bs(await res.text(), "lxml")
    price_tag = html.find(name="div", attrs={"class": "price"})
    house = House()
    total_tag = price_tag.find(name="span", attrs={"class": "total"})
    house.price = float(total_tag.text)
    del total_tag

    unit_tag = price_tag.find(name="span", attrs={"class": "unit"})
    house.unit = unit_tag.text
    del unit_tag

    unitPriceValue = html.find(name="span", attrs={"class": "unitPriceValue"})
    house.price_of_m = float(unitPriceValue.text.replace("元/平米", ""))
    del unitPriceValue

    lis = html.find(name="div", attrs={"class": "introContent"}).find(name="ul").find_all(name="li")
    content = li_to_dict(lis)
    house.type = content["房屋户型"]
    house.floor = content["所在楼层"]
    house.structure = content["户型结构"]
    house.build = content["建筑类型"]
    house.toward = content["房屋朝向"]
    house.renovation = content["装修情况"]
    house.area = content["建筑面积"].replace("㎡", "")
    house.print()

if __name__ == '__main__':
    urls = list(map(bytes.decode, db.smembers("urls")))
    loop = asyncio.get_event_loop()
    tasks = []
    for i in urls:
        task = loop.create_task(get_house_data(i))
        tasks.append(task)
    for i in tasks:
        loop.run_until_complete(i)

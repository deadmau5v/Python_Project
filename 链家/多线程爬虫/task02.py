import asyncio

import aiohttp
from redis import client
from bs4 import BeautifulSoup as Bs
from bs4 import Tag

db = client.Redis(host="172.17.0.2", port=6379)
db.keys()


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
    house = {}
    total_tag = price_tag.find(name="span", attrs={"class": "total"})
    house["price"] = float(total_tag.text)
    del total_tag

    unit_tag = price_tag.find(name="span", attrs={"class": "unit"})
    house["unit"] = unit_tag.text
    del unit_tag

    unitPriceValue = html.find(name="span", attrs={"class": "unitPriceValue"})
    house["price_of_m"] = float(unitPriceValue.text.replace("元/平米", ""))
    del unitPriceValue

    lis = html.find(name="div", attrs={"class": "introContent"}).find(name="ul").find_all(name="li")
    content = li_to_dict(lis)
    for i in content.keys():
        house[i] = content[i]

    print(house)

if __name__ == '__main__':
    urls = list(map(bytes.decode, db.smembers("urls")))
    loop = asyncio.get_event_loop()
    tasks = []
    for i in urls:
        task = loop.create_task(get_house_data(i))
        tasks.append(task)
    for i in tasks:
        loop.run_until_complete(i)

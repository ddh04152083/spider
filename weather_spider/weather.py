import requests
from bs4 import BeautifulSoup
from pyecharts import Bar, Line

ALL_DATA = []


def parse_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    text = response.content.decode("utf-8")
    soup = BeautifulSoup(text, "html5lib")
    conMidtab = soup.find("div", class_="conMidtab")
    tables = conMidtab.find_all("table")
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index, tr in enumerate(trs):
            tds = tr.find_all("td")
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-5]
            top_temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({"city": city, "top_temp": int(top_temp)})
            # print({"city": city, "top_temp": top_temp})

    return text


def main():
    urls = ["http://www.weather.com.cn/textFC/hb.shtml", "http://www.weather.com.cn/textFC/db.shtml",
            "http://www.weather.com.cn/textFC/hb.shtml", "http://www.weather.com.cn/textFC/hz.shtml",
            "http://www.weather.com.cn/textFC/xb.shtml", "http://www.weather.com.cn/textFC/xn.shtml"
            ]
    for url in urls:
        parse_page(url)
    ALL_DATA.sort(key=lambda data: data["top_temp"], reverse=True)
    data = ALL_DATA[1:20]

    # for city_temp in data:
    #     city = city_temp['city']
    #     cities.append(city)
    cities = list(map(lambda x: x['city'], data))
    temps = list(map(lambda x: x['top_temp'], data))
    chart = Line("中国天气最高气温排行榜")
    chart.add("", cities, temps)
    chart.render("temperature.html")

    # print(data)


if __name__ == '__main__':
    main()

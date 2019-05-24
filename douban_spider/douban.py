import json

import requests
from bs4 import BeautifulSoup


def get_page():
    url = "https://movie.douban.com/cinema/nowplaying/xian/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    # print(response.text)
    return response.text


def parse_page(text):
    soup = BeautifulSoup(text, 'lxml')
    liList = soup.find_all("li", attrs={"data-category": "nowplaying"})
    movies = []
    for li in liList:
        movie = {}
        title = li['data-title']
        score = li['data-score']
        release = li['data-release']
        duration = li['data-duration']
        region = li['data-region']
        director = li['data-director']
        actors = li['data-actors']
        img = li.find('img')
        thumbnail = img['src']
        movie['title'] = title
        movie['score'] = score
        movie['release'] = release
        movie['duration'] = duration
        movie['region'] = region
        movie['director'] = director
        movie['actors'] = actors
        movie['thumbnail'] = thumbnail
        movies.append(movie)
    for i in movies:
        print(i)
    return movies


def save_data(data):
    with open("douban.json", "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False)


if __name__ == '__main__':
    text = get_page()
    movies = parse_page(text)
    save_data(movies)

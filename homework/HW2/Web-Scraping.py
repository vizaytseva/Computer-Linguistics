import requests as rq
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = 'https://www.vedomosti.ru'
NEWS_CHAPTER_URL = 'https://www.vedomosti.ru/ecology'


def find_all_urls(soup):
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')

        if href:
            urls.append(href)
    return set(urls)


def parse_page(url):
    page = rq.get(url)
    return BeautifulSoup(page.text, features='html.parser')


def get_news(url0):
    page0 = rq.get(url0)
    soup0 = BeautifulSoup(page0.text, features="html.parser")
    time = soup0.find('time').attrs['datetime']
    date = time[:10]
    title = soup0.find_all('meta', {'property': 'og:title'})[0].attrs['content']
    text_list = soup0.find_all('p', {'class': 'box-paragraph__text'})
    text = []
    for i in text_list:
        text.append(i.text)
    final_text = ' '.join(text)
    return url0, date, title, final_text


def main():
    news_chapter_soup = parse_page(NEWS_CHAPTER_URL)

    release_urls = list(
        map(lambda url: BASE_URL + url,
            filter(lambda url: 'release' in url, find_all_urls(news_chapter_soup))))

    for link in release_urls:
        release_soup = parse_page(link)

        news_urls = list(
            map(lambda url: BASE_URL + url,
                filter(lambda url: 'articles' in url or 'columns' in url, find_all_urls(release_soup))))

        news = []
        for i in news_urls:
            new = get_news(i)
            news.append(new)

        df = pd.DataFrame(news)
        df.columns = ['link', 'date', 'headline', 'text']
        df.to_csv('EcoNews.csv', encoding='utf-8')










import re
from bs4 import BeautifulSoup
import requests
import pandas as pd


class News:
    def __init__(self, country='', city='', no_of_records=5):
        self.no_of_records = no_of_records
        self.url = 'https://news.google.com/rss/search?q=' + city + '%20' + country + '%20covid&hl=en-US&gl=US&ceid=US%3Aen'

    def get_news(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html5lib')
        item = soup.findAll('item')
        news_list = []
        for row in item:
            news_dict = {}
            news_dict['title'] = str(row.title)[7:-8]
            news_dict['date'] = str(row.pubdate)[9:-10]
            match = re.search(r'href=[\'"]?([^\'" >]+)', str(row.description))
            if match:
                news_dict['link'] = match.group(1)
            news_list.append(news_dict)
        news_df = pd.DataFrame(news_list)
        return news_df[:self.no_of_records]


if __name__ == '__main__':
    df = News(country='uk', city='london', no_of_records=5).get_news()
    print(df)

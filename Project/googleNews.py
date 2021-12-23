# -*- coding: utf-8 -*-

'''
File Name: googleNews.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

News class scrapes news from google news website, process it and then return the data.

Files importing this class: travelpalControl.py
'''

import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from dash import html


class News:
    def setLocation(self, country, city, max_no_of_records=5):
        '''
        Retrieves Google News for a 'country' and 'city'
        
        Genrates URL, retreives information and converts it to 
        Beautiful Soup object
        
        Parameters
        ----------
        country : str
            Country for which to retrieve data.
        city : str
            City for which to retrieve data.
        max_no_of_records : int
            Maximum number of data records to return.
        '''
        self.max_no_of_records = max_no_of_records
        self.country = country
        self.city = city
        self.url = 'https://news.google.com/rss/search?q=' + city + '%20' + country + '%20covid&hl=en-US&gl=US&ceid=US%3Aen'
        
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content, 'html5lib')

    def getNews(self):
        '''
        Return a list of relevent news titles, date and link
        '''
        item = self.soup.findAll('item')
        news_list = []
        for row in item:
            news_dict = {}
            news_dict['title'] = str(row.title)[7:-8]
            date = datetime.strptime(str(row.pubdate)[14:-10], '%d %b %Y %H:%M:%S %Z')
            news_dict['date'] = date.strftime("%b %d, %Y")
            match = re.search(r'href=[\'"]?([^\'" >]+)', str(row.description))
            if match:
                news_dict['link'] = match.group(1)
            news_list.append(news_dict)
        
        if len(news_list) > 0:
            return news_list[:5]
        
        return None

    def getFormattedNewsSummary(self):
        '''
        Generate HTML content for News articles
        
        Conversts list of news articles to HTML content using tags including
        reference link to that article and returns it
        '''
        content = []
        info = self.getNews()
        if info == None:
            text = "Currently no news available for " + self.city + ", " + self.country
            return html.P(children=text)
        
        for num in range(len(info)):
            text = str(num+1) + ". " + info[num]['title'] + "\n" + info[num]['date']
            content.append(
                html.Div(
                    children=[
                        html.P(children=text),
                        html.A('Get more info here', href=info[num]['link'], target="_blank"),
                        html.P(children="\n")
                    ],
                    style={'font-size':'16', 'whiteSpace': 'pre-wrap'}
                )
            )
        
        return content
            
        
if __name__ == '__main__':
    df = News()
    df.setLocation(country='uk', city='London', max_no_of_records=5)
    print(df.getNews())

# -*- coding: utf-8 -*-
## Extracts data from CDC Country Webpage and cleans

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re
import pandas as pd


def get_covid_info(country):
    url = "https://wwwnc.cdc.gov/travel/destinations/traveler/none/" + country.lower()
    html = urlopen(url)
    bsyc = BeautifulSoup(html.read(), "lxml")

    # Extracts covid_level
    header_notice_list = bsyc.find_all('h4', attrs={"class": re.compile("notice-typename notice-typename*")})
    header_notice = header_notice_list[0]
    covid_level = header_notice.contents
    covid_level = covid_level[0]

    # Extracts recommended_vaccines_df = dataframe of recommended vaccines and medicine before travel
    tbl_list = pd.read_html(url)
    recommended_vaccines_df = tbl_list[0]
    del recommended_vaccines_df['Clinical Guidance for Healthcare providers']

    return covid_level, recommended_vaccines_df  # Returns list of [str, DataFrame]

'''
    ## Download image - IN PROGRESS
    img_tags = bsyc.find_all('img')
    urls = [img['src'] for img in img_tags]
    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        if not filename:
            print("Regex didn't match with the url: {}".format(url))
            continue
        with open('map.png', 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative
                # if it is provide the base url which also happens
                # to be the site variable atm.
                url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content)
'''

if __name__ == '__main__':
    print(get_covid_info('egypt'))

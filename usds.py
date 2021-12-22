# -*- coding: utf-8 -*-
## Extracts data from United States Department of State Country Page and cleans
## Some countries have unique names and will not work. i.e. Russia -> Russian Fereration
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_visa_info(country):
    url = "https://travel.state.gov/content/travel/en/international-travel/International-Travel-Country-Information-Pages/" + country.title() + ".html"
    html = urlopen(url)
    bsyc = BeautifulSoup(html.read(), "lxml")

    # Builds two lists: quick facts titles and quick facts contents
    qf_title_list = bsyc.find_all('div', {"class": "tsg-rwd-qf-box-title"})
    qf_titles = []
    for i in qf_title_list:
        qf_titles.append(i.text)  # Need to clean further
    qf_content_list = bsyc.find_all('div', {"class": "tsg-rwd-qf-box-data"})
    qf_content = []
    for i in qf_content_list:
        qf_content.append(i.find('p').text)

    qf_titles_clean = []
    for t in qf_titles:
        qf_titles_split = t.split()
        title = ""
        for t in qf_titles_split:
            title += t + " "
        qf_titles_clean.append(title.strip().capitalize())

    # Zips dict of key=quick facts title, value= quick facts content
    visa_qf_dict = dict(zip(qf_titles_clean, qf_content))

    return visa_qf_dict # Return visa quick facts dict


if __name__ == '__main__':
    print(get_visa_info("egypt"))



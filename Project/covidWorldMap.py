# -*- coding: utf-8 -*-

'''
File Name: covidWorldMap.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

WorldMap class retrieves data from Johns Hopkins University Github page aboubt covid cases, process it and then return the map.

Files importing this class: travelpalControl
'''

import plotly.express as px
import pandas as pd

class WorldMap:
    def __init__(self):
        '''
        Generate dataFrame with past day covid cases
        '''
        self.fig = None
        iso_lookup_df = pd.read_csv(
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv',
            header=0)
        iso_lookup_df = iso_lookup_df.groupby(['Country_Region', 'iso2', 'iso3']).size().reset_index(name='counts')
        iso_lookup_df = iso_lookup_df.sort_values(by=['Country_Region', 'counts'], ascending=False)
        iso_lookup_df = iso_lookup_df.groupby(['Country_Region'])[['iso2', 'iso3', 'counts']].first().drop(
            columns='counts')

        global_confirmed_df = pd.read_csv(
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
            header=0)
        confirmed_len_idx = len(global_confirmed_df.columns) - 1
        global_confirmed_df = global_confirmed_df.iloc[:, [0, 1, confirmed_len_idx]]
        global_confirmed_df.columns = ['Province_State', 'Country_Region', '1 Day Ago']
        global_confirmed_df = global_confirmed_df.groupby(['Country_Region'])[['1 Day Ago']].agg('sum')

        covid_merge_df = iso_lookup_df.join(global_confirmed_df)
        self.covid = covid_merge_df.reset_index()
    
    def getMap(self):
        '''
        Generate and return a worldmap figure with past day covid cases
        '''
        df = self.covid
        fig = px.choropleth(df, locations="iso3",
                                color="1 Day Ago", # lifeExp is a column of gapminder
                                hover_name="Country_Region", # column to add to hover information
                                projection='natural earth',
                                color_continuous_scale=px.colors.sequential.Plasma)
        fig.update_layout(title=dict(font=dict(size=38),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))
        fig.update_geos(fitbounds="locations", visible=True,showcountries=True)
        return fig


if __name__ == '__main__':
    Map = WorldMap()
    Map.getMap().show()

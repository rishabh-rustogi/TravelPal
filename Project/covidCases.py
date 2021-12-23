# -*- coding: utf-8 -*-

'''
File Name: covidCases.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

COVIDCases class retrieves data from Johns Hopkins University Github page aboubt covid cases, process it and then return the data.
This class also create two regression model to estimate the cases

Files importing this class: travelpalControl.py
'''

import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

class COVIDCases:
    def __init__(self):
        '''
        Retrieves Covid Cases and Deaths
        
        Process the information retrieved from Johns Hopkins University,
        extract past week information and stores it for every country
        in a Dataframe
        '''
        global_deaths_df = pd.read_csv(
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
            header=0)
        death_len_idx = len(global_deaths_df.columns) - 1
        global_deaths_df = global_deaths_df.iloc[:,
                           [0, 1, death_len_idx - 6, death_len_idx - 5, death_len_idx - 4, death_len_idx - 3,
                            death_len_idx - 2, death_len_idx - 1, death_len_idx]]
        global_deaths_df.columns = ['Province_State', 'Country_Region', '7 Days Ago', '6 Days Ago', '5 Days Ago',
                                    '4 Days Ago', '3 Days Ago', '2 Days Ago', '1 Day Ago']
        global_deaths_df['Last_Week'] = global_deaths_df['1 Day Ago'] - global_deaths_df['7 Days Ago']
        global_deaths_df = global_deaths_df.groupby(['Country_Region'])[
            ['7 Days Ago', '6 Days Ago', '5 Days Ago', '4 Days Ago', '3 Days Ago', '2 Days Ago', '1 Day Ago',
             'Last_Week']].agg('sum')
        self.global_deaths_df = global_deaths_df

        global_confirmed_df = pd.read_csv(
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
            header=0)
        confirmed_len_idx = len(global_confirmed_df.columns) - 1
        global_confirmed_df = global_confirmed_df.iloc[:,
                              [0, 1, confirmed_len_idx - 6, confirmed_len_idx - 5, confirmed_len_idx - 4,
                               confirmed_len_idx - 3, confirmed_len_idx - 2, confirmed_len_idx - 1, confirmed_len_idx]]
        global_confirmed_df.columns = ['Province_State', 'Country_Region', '7 Days Ago', '6 Days Ago', '5 Days Ago',
                                       '4 Days Ago', '3 Days Ago', '2 Days Ago', '1 Day Ago']
        global_confirmed_df['Last_Week'] = global_confirmed_df['1 Day Ago'] - global_confirmed_df['7 Days Ago']
        global_confirmed_df = global_confirmed_df.groupby(['Country_Region'])[
            ['7 Days Ago', '6 Days Ago', '5 Days Ago', '4 Days Ago', '3 Days Ago', '2 Days Ago', '1 Day Ago',
             'Last_Week']].agg('sum')
        self.global_confirmed_df = global_confirmed_df

    def setCountry(self, country):
        '''
        Setter function for country
        
        Sets the country for extracting past week covid data
        
        Parameters
        ----------
        country : str
            Country for which to retrieve data.
        '''
        self.country = country

    def getCovidGraph(self):
        '''
        Returns a bar graph figure
        
        Generate Dataframe for producing plotly graph.
        '''
        country = self.country
        df1 = self.global_confirmed_df.query("Country_Region=='{}'".format(country)).T.iloc[[0, 1, 2, 3, 4, 5, 6],
                :].reset_index()
        df1['Type'] = 'Cases'
        df1 = df1.rename(columns={"index": "Timeline", country: "Frequency"})
        df1.Frequency = df1.Frequency - df1.iloc[0, 1]
        df2 = self.global_deaths_df.query("Country_Region=='{}'".format(country)).T.iloc[[0, 1, 2, 3, 4, 5, 6],
                :].reset_index()
        df2['Type'] = 'Deaths'
        df2 = df2.rename(columns={"index": "Timeline", country: "Frequency"})
        df2.Frequency = df2.Frequency - df2.iloc[0, 1]
        df3 = df1.append(df2).query("Timeline!='7 Days Ago'")
        
        return self.createLineBarChart(df3)
    
    def createLineBarChart(self, df):
        '''
        Returns a bar graph figure
        
        Creates a plotly bar chart containing both cases and deaths 
        for a 'country' and return it
        '''
        maskCases = (df['Type'] == 'Cases')
        maskDeaths = (df['Type'] == 'Deaths')
        colors = {'Cases':'steelblue',
                'Deaths':'firebrick'}
        
        regCases = LinearRegression().fit(np.asarray(list(range(6))).reshape((-1,1)), np.asarray(df[maskCases]['Frequency']).reshape((-1,1)))
        trace4  = go.Scatter(
                mode='lines+markers',
                x = df[maskCases]['Timeline'],
                y = regCases.predict(np.asarray(list(range(6))).reshape((-1,1))).flatten(),
                name="Fitted Value for Cases",
                line=dict(width=4),
                marker=dict(size=10)
            )
        
        trace3 = go.Bar(
                x = df[maskCases]['Timeline'],
                y = df[maskCases]['Frequency'],
                marker_line_width=1.5,
                marker_line_color='rgb(8,48,107)',
                marker_color=colors['Cases'],
                opacity=0.5,
                name="Cases",
            )
        
        regDeaths = LinearRegression().fit(np.asarray(list(range(6))).reshape((-1,1)), np.asarray(df[maskDeaths]['Frequency']).reshape((-1,1)))
        trace2  = go.Scatter(
                mode='lines+markers',
                x = df[maskDeaths]['Timeline'],
                y = regDeaths.predict(np.asarray(list(range(6))).reshape((-1,1))).flatten(),
                name="Fitted Value for Deaths",
                line=dict(color='firebrick', width=4),
                marker=dict(size=10)
            )

        trace1 = go.Bar(
                x = df[maskDeaths]['Timeline'],
                y = df[maskDeaths]['Frequency'],
                marker_line_width=1.5,
                marker_line_color='rgb(8,48,107)',
                marker_color=colors['Deaths'],
                opacity=0.5,
                name="Deaths",
            )

        layout = go.Layout(
            title_text='Last Week - COVID-19 Cases and Deaths in {}'.format(self.country),
            yaxis_title_text='Frequency',
            xaxis_title_text='Timeline',
            legend_title_text='Type'
        )
        fig = go.Figure(data=[trace1, trace2, trace3, trace4], layout=layout)
        fig.update_yaxes(type="log")
        return fig


if __name__ == '__main__':
    Cases = COVIDCases()
    Cases.setCountry("India")
    Cases.getCovidGraph().show()

# -*- coding: utf-8 -*-

'''
File Name: travelpalAppLayout.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

This file contains methods to construct app layput and handle data transfer from and to the app

Files imported by this file: travelpalApp.py, travelpalControl.py

Files importing this file: travelpal.py
'''

from travelpalApp import app
import dash 
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from travelpalControl import TravelpalController
import dash

# Define an object of type TravelPalController for the application functionalities
controller = TravelpalController()

def constructApp():
    '''
    Returns the application basic structure
    
    HTML tags with CSS formatting formaing the blueprint
    of the TravelPal Application
    '''
    return dcc.Loading(
        children=[
            html.Div(
                id='travelpal',
                children=[
                    dbc.Row(
                        dbc.Col(html.Br())
                    ),
                    dbc.Row(
                        dbc.Col(
                            [
                                dbc.Row(
                                    dbc.Col(
                                        html.P(
                                            children="TravelPal", 
                                        ),
                                        style={'color':'red', 'textAlign': 'center', 'font-size':'48px', 'font-weight':'bold'}
                                    ),
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        html.P(
                                            children="One Stop Solution for all your travel Information",
                                        ),
                                        style={'color':'#CFCFCF','textAlign': 'center', 'font-size':'20px'}
                                    )
                                ),
                            ],
                            className='header',
                            style={'background-color': '#222222', 'top':'0px','overflow':'hidden'}
                        ),
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    children=[
                                        html.Div(children="Country", className="menu-title", style={'textAlign': 'center', 'font-size':'16px'}),
                                        dcc.Dropdown(
                                            id="country-dropdown",
                                            options=[{"label": country, "value": country} for country in controller.getCountries()],
                                            placeholder="Select Country",
                                            className="dropdown",
                                        ),
                                    ]
                                ),
                                width=4
                            ),
                            dbc.Col(
                                html.Div(
                                    children=[
                                        html.Div(children="Region", className="menu-title", style={'textAlign': 'center'}),
                                        dcc.Dropdown(
                                            id="region-dropdown",
                                            placeholder="Select Region",
                                            clearable=False,
                                            className="dropdown",
                                        ),
                                    ],
                                ),
                                width=4
                            )
                        ],
                        justify="center",
                        className="menu",
                        style={'background-color': 'white', 'position':'float','border': '15px solid', 'border-color':'#222222', 'padding':'20px'}
                    ),
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                children=dcc.Graph(
                                    id="world-covid-graph", config={"displayModeBar": False},
                                ),
                                className="card",
                            ), 
                            style= {'display': 'block'}     
                        )
                    ),
                    dbc.Row(
                        html.Div(
                            children=[
                                
                                dbc.Row(
                                    id="covid-summary-row",
                                    children=html.Div([
                                        dbc.Row([
                                            dbc.Col(
                                                children=[
                                                    html.Div(
                                                        id="covid-level",
                                                        children=[
                                                            html.P(children="Covid Level Severity"),
                                                            dbc.Progress(id="covid-severity-level" ,label="Covid Level Low", value=80, color="success", bar=True, animated=False),
                                                        ],
                                                        style={'width':'80%', 'height':'80px','padding-left':'20px'}
                                                    ),
                                                    html.Div(
                                                        children=html.Div(
                                                                id="key-facts",
                                                                children=[
                                                                    html.Div(
                                                                        id="summary-info",
                                                                        children=html.P(children="Summary"),
                                                                        style={'font-size':'18px', 'font-weight':'bold'}
                                                                    ),
                                                                    html.Div(
                                                                        children=html.P(id="covid-short-summary"),
                                                                        style={'font-size':'16'}
                                                                    ),
                                                                    html.Div(
                                                                        children=html.P(children="Hotspots:"),
                                                                        style={'font-size':'18px', 'font-weight':'bold'}
                                                                    ),
                                                                    html.Div(
                                                                        children=html.P(id="covid-hotspots"),
                                                                        style={'font-size':'16'}
                                                                    ),
                                                                ],
                                                                style={'color':'#CFCFCF', 'padding':'30px', 'width':'100%', 'border': '5px solid', 'border-color':'#222222','border-radius':'25px', 'background':'#4E4E4E'}
                                                            ),
                                                    ),
                                                ],
                                                style={'padding-right':'20px'},
                                                width=8
                                            ),
                                            dbc.Col(
                                                children=html.Div(
                                                    id="image-row",
                                                    children=[
                                                        html.Img(alt="Unable to fetch country map",
                                                                style={'width':'100%', 'height':'100%','border-radius':'25px', 'background-color': '#000000'}
                                                            )
                                                    ],
                                                    style={'color':'#CFCFCF', 'padding':'3px', 'width':'100%', 'border': '2px solid', 'border-color':'#222222','border-radius':'25px', 'background':'#222222'}
                                                ),
                                                style={'padding-left':'20px'},
                                                width=4
                                            ),
                                        ])   
                                    ],
                                    style={'padding':'40px'}
                                    )
                                ),
                                dbc.Row(
                                    html.Div(
                                        children=html.Div(
                                                id="covid-graph",
                                                children=[
                                                    html.Div(
                                                        children=html.P(children="Past week covid chart:"),
                                                        style={'font-size':'18px', 'font-weight':'bold'}
                                                    ),
                                                    html.Div(
                                                        children=dcc.Graph(
                                                            figure={},
                                                            id="covid-line-graph",
                                                        ),
                                                        className="card",
                                                    ),
                                                ],
                                                style={'color':'#CFCFCF', 'padding':'30px', 'width':'100%', 'border': '5px solid', 'border-color':'#222222','border-radius':'25px', 'background':'#4E4E4E'}
                                            ),
                                        style={'padding':'40px'}
                                    )
                                ),
                                dbc.Row(
                                    id="info-row",
                                    children=html.Div([
                                        dbc.Row([
                                            dbc.Col(
                                                children=html.Div(
                                                    id="vaccine-info-row",
                                                    children=[
                                                        html.Div(
                                                            children=html.P(children="Vaccines related information:"),
                                                            style={'font-size':'18px', 'font-weight':'bold'}
                                                        ),
                                                        html.Div(
                                                            id="vaccince-info",
                                                            children=html.P(children="Sample Covid info"),
                                                            style={'font-size':'16', 'whiteSpace': 'pre-wrap'}
                                                        ),
                                                    ],
                                                    style={'color':'#CFCFCF', 'padding':'30px', 'width':'100%', 'border': '5px solid', 'border-color':'#222222','border-radius':'25px', 'background':'#4E4E4E'}
                                                ),
                                                style={'padding-right':'20px'}
                                            ),
                                            dbc.Col(
                                                children=html.Div(
                                                    id="visa-info-row",
                                                    children=[
                                                        html.Div(
                                                            children=html.P(children="Visa related information:"),
                                                            style={'font-size':'18px', 'font-weight':'bold'}
                                                        ),
                                                        html.Div(
                                                            id="visa-info",
                                                            children=html.P(children="Sample Visa Info"),
                                                            style={'font-size':'16', 'whiteSpace': 'pre-wrap'}
                                                        ),
                                                    ],
                                                    style={'color':'#CFCFCF', 'padding':'30px', 'width':'100%', 'border': '5px solid', 'border-color':'#222222','border-radius':'25px', 'background':'#4E4E4E'}
                                                ),
                                                style={'padding-left':'20px'}
                                            ),
                                        ])   
                                    ],
                                    style={'padding':'40px'}
                                    )
                                ),
                                dbc.Row(
                                    html.Div(
                                        children=html.Div(
                                                id="covid-related-info",
                                                children=[
                                                    html.Div(
                                                        children=html.P(children="Covid related info:"),
                                                        style={'font-size':'18px', 'font-weight':'bold'}
                                                    ),
                                                    html.Div(
                                                        id="covid-realted-all-info",
                                                        children=html.P(children="Sample Covid News"),
                                                        style={'font-size':'16'}
                                                    ),
                                                ],
                                                style={'color':'#CFCFCF', 'padding':'30px', 'width':'100%', 'border': '5px solid', 'border-color':'#222222','border-radius':'25px', 'background':'#4E4E4E'}
                                            ),
                                        style={'padding':'40px'}
                                    )
                                ),
                                dbc.Row(
                                    html.Div(
                                        children=html.Div(
                                                id="covid-news",
                                                children=[
                                                    html.Div(
                                                        children=html.P(children="Covid related news:"),
                                                        style={'font-size':'18px', 'font-weight':'bold'}
                                                    ),
                                                    html.Div(
                                                        id="covid-news-info",
                                                        children=html.P(children="Sample Covid News"),
                                                        style={'font-size':'16'}
                                                    ),
                                                ],
                                                style={'color':'#CFCFCF', 'padding':'30px', 'width':'100%', 'border': '5px solid', 'border-color':'#222222','border-radius':'25px', 'background':'#4E4E4E'}
                                            ),
                                        style={'padding':'40px'}
                                    )
                                ),
                                dbc.Row(
                                    html.Div(
                                        children=html.Div(
                                                id="weather-info",
                                                children=[
                                                    html.Div(
                                                        children=html.P(children="7 days weather forcast:"),
                                                        style={'font-size':'18px', 'font-weight':'bold'}
                                                    ),
                                                    html.Div(
                                                        children=dcc.Graph(
                                                            id="weather-line-graph",
                                                        ),
                                                        className="card",
                                                    ),
                                                ],
                                                style={'color':'#CFCFCF', 'padding':'30px', 'width':'100%', 'border': '5px solid', 'border-color':'#222222','border-radius':'25px', 'background':'#4E4E4E'}
                                            ),
                                        style={'padding':'40px'}
                                    )
                                ),
                                dbc.Row(
                                    html.Div(
                                        children=html.Div(
                                                id="POI-info",
                                                children=[
                                                    html.Div(
                                                        children=html.P(children="Points of Interest:"),
                                                        style={'font-size':'18px', 'font-weight':'bold'}
                                                    ),
                                                    html.Div(
                                                        id="poi-places-info",
                                                        children=html.P(children="POI Info will come here"),
                                                        style={'font-size':'16'}
                                                    ),
                                                ],
                                                style={'color':'#CFCFCF', 'padding':'30px', 'width':'100%', 'border': '5px solid', 'border-color':'#222222','border-radius':'25px', 'background':'#4E4E4E'}
                                            ),
                                        style={'padding':'40px'}
                                    )
                                ),
                            ],
                            id="location-content",
                            style={'display': 'none'}
                        )
                    ),
                ],
                style={'background':'#CCCCCC'}
            ),
        ],
        color="#119DFF",
        type="dot",
        fullscreen=True,
    )

@app.callback(
    dash.dependencies.Output('region-dropdown', 'options'),
    dash.dependencies.Output('region-dropdown', 'value'),
    [dash.dependencies.Input('country-dropdown', 'value')]
)
def updateRegionDropdown(country):
    '''
    Returns region for a country
    
    Callback function sets the regions dropdown option with correct values
    
    Parameters
    ----------
    country : str
        Country for which to retrieve Regions.
    '''
    return [{'label': region, 'value': region} for region in controller.getRegions(country)], None

@app.callback(
    dash.dependencies.Output('world-covid-graph', 'figure'),
    dash.dependencies.Output('world-covid-graph', component_property='style'),
    dash.dependencies.Output('location-content', component_property='style'),
    dash.dependencies.Output('covid-severity-level', 'value'),
    dash.dependencies.Output('covid-severity-level', 'label'),
    dash.dependencies.Output('summary-info', 'children'),
    dash.dependencies.Output('covid-short-summary', 'children'),
    dash.dependencies.Output('covid-hotspots', 'children'),
    dash.dependencies.Output('image-row', 'children'),
    dash.dependencies.Output('vaccince-info', 'children'),
    dash.dependencies.Output('visa-info', 'children'),
    dash.dependencies.Output('covid-related-info', 'children'),
    dash.dependencies.Output('covid-news-info', 'children'),
    dash.dependencies.Output('weather-line-graph', 'figure'),
    dash.dependencies.Output('poi-places-info', 'children'),
    dash.dependencies.Output('covid-line-graph', 'figure'),
    [
        dash.dependencies.Input('region-dropdown', 'value'),
        dash.dependencies.Input('country-dropdown', 'value'),
    ]
)
def doStuff(region, country):
    '''
    Returns the application data
    
    Callback function fills the basic layout with all the information
    
    Parameters
    ----------
    region : str
        Region name to search for information.
    country : str
        Country name to search for information.
    '''
    return controller.getReturnInformation(region, country)
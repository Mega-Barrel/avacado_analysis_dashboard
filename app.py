from distutils.command.config import config
from pydoc import classname
import dash
import pandas as pd
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output

# Reading dataset file
avacado_data = pd.read_csv('./avocado.csv')
avacado_data = avacado_data.query("type == 'conventional' and region == 'Albany'")
avacado_data['Date'] = pd.to_datetime(avacado_data['Date'], format="%Y-%m-%d")
avacado_data.sort_values("Date", inplace=True)

# adding external stylesheet
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

# Initializing a dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Title of app
app.title = 'Avocado Analytics: Understand your avocados!'

# Layout of the app
app.layout = html.Div(
    [
        html.Div(
            [
                html.P(
                    "🥑", 
                    className="header-emoji"
                ),
                html.H1(
                    'Avocado Analytics',
                    className = 'header-title'
                ),
                html.P(
                    "Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className = 'header-description'
                ),
            ],
            className = 'header'    
        ),
        # Plotly chart
        html.Div(
            [
                # graph 1
                html.Div(
                    dcc.Graph(
                        id = 'price-chart',
                        config = {
                            'displayModeBar': False,
                        },
                        figure = {
                            'data': [
                                {
                                    'x': avacado_data['Date'],
                                    'y': avacado_data['AveragePrice'],
                                    'type': "lines",
                                    'hovertemplate': "$%{y:.2f}"
                                                                "<extra></extra>"
                                },
                            ],
                            'layout': {
                                'title': {
                                    'text': 'Average Price of Avocados',
                                    'x': 0.05,
                                    'xanchor': 'left'
                                },
                                'xaxis': {
                                    'fixedrange': True
                                },
                                'yaxis': {
                                    'tickprefix': '$',
                                    'fixedrange': True
                                },
                                'colorway': [
                                    '#17B897'
                                ],
                                'hovermode': 'x',
                            },
                        },
                    ),
                    className = 'card'
                ),
                
                # graph 2
                html.Div(
                    dcc.Graph(
                        id = 'volume-chart',
                        config = {
                            'displayModeBar': False,
                        },
                        figure = {
                            'data': [
                                {
                                    'x': avacado_data['Date'],
                                    'y': avacado_data['Total Volume'],
                                    'type': 'lines',
                                },
                            ],
                            'layout': {
                                'title': {
                                    'x': avacado_data['Date'],
                                    'y': avacado_data['Total Volume'],
                                    'type': 'lines',
                                },
                                'xaxis': {
                                    'fixedrange': True
                                },
                                'yaxis': {
                                    'fixedrange': True
                                },
                                'colorway': [
                                    '#E12D39'
                                ],
                                'hovermode': 'x',
                            },
                        },
                    ),
                    className = 'card',
                ),
            ],
            className = 'wrapper'
        ),    
    ]
)

if __name__ == '__main__':
    app.run_server(
        debug = True
    )
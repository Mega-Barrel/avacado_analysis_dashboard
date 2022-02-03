# from distutils.command.config import config
# from pydoc import classname
import dash
import numpy as np
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output

# Reading dataset file
avocado_data = pd.read_csv('./avocado.csv')
avocado_data['Date'] = pd.to_datetime(avocado_data['Date'], format='%Y-%m-%d')
avocado_data.sort_values('Date', inplace=True)

# adding external stylesheet
external_stylesheets = [
    {
        'href': 'https://fonts.googleapis.com/css2?'
        'family=Lato:wght@400;700&display=swap',
        'rel': 'stylesheet',
    },
]

# Initializing a dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Title of app
app.title = 'Avocado Analytics: Understand your Avocados!'

# Layout of the app
app.layout = html.Div(
    [   
        # header div
        html.Div(
            [
                html.P(
                    '🥑', 
                    className='header-emoji'
                ),
                html.H1(
                    'Avocado Analytics',
                    className = 'header-title'
                ),
                html.P(
                    'Analyze the behavior of avocado prices'
                    ' and the number of avocados sold in the US'
                    ' between 2015 and 2018',
                    className = 'header-description'
                ),
            ],
            className = 'header'    
        ),
        
        # Plotly chart wrapper card
        html.Div(
            [
                # region Name filter
                html.Div(
                    [
                        html.Div(
                            'Region', 
                            className = 'menu-title'
                        ),
                        dcc.Dropdown(
                            id = 'region-filter',
                            options = [
                                {
                                    'label': region, 
                                    'value': region
                                } for region in np.sort(avocado_data.region.unique())
                            ],
                            value = 'Albany',
                            clearable = False,
                            className ='dropdown',
                        ),
                    ]
                ),
                
                # avocado_type filter
                html.Div(
                    [
                        html.Div(
                            'Type', 
                            className = 'menu-title'
                        ),
                        dcc.Dropdown(
                            id = 'type-filter',
                            options = [
                                {
                                    'label': avocado_type, 
                                    'value': avocado_type
                                } for avocado_type in avocado_data.type.unique()
                            ],
                            value = 'organic',
                            clearable = False,
                            searchable = False,
                            className = 'dropdown',
                        ),
                    ],
                ),
                
                # daterange filter
                html.Div(
                    [
                        html.Div(
                            'Date Range',
                            className = 'menu-title'
                            ),
                        dcc.DatePickerRange(
                            id = 'date-range',
                            min_date_allowed = avocado_data.Date.min().date(),
                            max_date_allowed = avocado_data.Date.max().date(),
                            start_date = avocado_data.Date.min().date(),
                            end_date = avocado_data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className = 'menu',
        ),
        
        # Plots
        html.Div(
            [
                html.Div(
                    children = dcc.Graph(
                        id = 'price-chart', 
                        config = {
                            'displayModeBar': False
                        },
                    ),
                    className = 'card',
                ),
                html.Div(
                    dcc.Graph(
                        id = 'volume-chart', 
                        config = {
                            'displayModeBar': False
                        },
                    ),
                    className = 'card',
                ),
            ],
            className = 'wrapper',
        ),  
    ]
)

@app.callback(
    [
        Output('price-chart', 'figure'), 
        Output('volume-chart', 'figure')
    ],
    [
        Input('region-filter', 'value'),
        Input('type-filter', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'),
    ],
)
def update_charts(region, avocado_type, start_date, end_date):
    mask = (
        (avocado_data.region == region)
        & (avocado_data.type == avocado_type)
        & (avocado_data.Date >= start_date)
        & (avocado_data.Date <= end_date)
    )
    filtered_data = avocado_data.loc[mask, :]
    price_chart_figure = {
        'data': [
            {
                'x': filtered_data['Date'],
                'y': filtered_data['AveragePrice'],
                'type': 'lines',
                'hovertemplate': '$%{y:.2f}<extra></extra>',
            },
        ],
        'layout': {
            'title': {
                'text': f'Average Price of Avocados in {region}',
                'x': 0.05,
                'xanchor': 'left',
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
    }

    volume_chart_figure = {
        'data': [
            {
                'x': filtered_data['Date'],
                'y': filtered_data['Total Volume'],
                'type': 'lines',
            },
        ],
        'layout': {
            'title': {
                'text': f'Avocados Sold in {region}', 
                'x': 0.05, 
                'xanchor': 'left'
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
            'hovermode': 'x'
        },
    }
    return price_chart_figure, volume_chart_figure
    

if __name__ == '__main__':
    app.run_server(
        debug = True
    )
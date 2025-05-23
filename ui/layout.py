# Author: Davis Thomas Daniel
# Project: droic
# Module: ui.layout

from dash import dcc, html

def create_layout():
    layout = html.Div([
        # logo
        html.Div([
            html.Img(src='/assets/droic_logo.svg', style={'height': '180px'}),
        ], style={'textAlign': 'center', 'marginBottom': '30px', 'marginTop': '10px'}),
        # notifications
        html.Div([
            html.Div(id='general-notification',
                     className='notification-hidden'),
            dcc.Interval(id='notification-clear-interval',
                         interval=1500, n_intervals=0, disabled=True),
        ]),
        html.Br(),
        html.Div([
            # shows devices available and connection types
            html.Div([
                html.Div(id='connection-status',
                         className='device-status-box'),
            ]),
            # device info box, when connected shows info in pill shaped elements
            html.Div(id='device-info', style={'marginBottom': '20px'}),

            # device-selection-container
            html.Div([
                html.Div([
                    html.Label("Device:", style={'marginRight': '10px'}),
                    # dropdown for device selection, auto-selects first available device.
                    dcc.Dropdown(
                        id='device-dropdown',
                        options=[], 
                        style={'width': '500px', 'marginRight': '20px',
                               'alignItems': 'center'},
                        clearable=False
                    ),
                    # refresh-button
                    html.Button('Refresh Devices', id='refresh-button', n_clicks=0,
                                style={'marginLeft': '10px', 'marginRight': '10px'}),
                    # connect to adb via wi-fi
                    html.Button('Wi-Fi Connect', id='wifi-connect-button', n_clicks=0,
                                style={'marginLeft': '10px'})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '15px'})
            ], id='device-selection-container'),

            # monitoring controls
            html.Div([
                html.Label("Monitor", style={'marginRight': '2px'}),
                html.Label("every", style={'marginRight': '2px'}),
                dcc.Input(
                    id='interval-input',
                    type='number',
                    min=1,
                    max=60,
                    value=5,
                    style={'width': '50px', 'marginRight': '5px'}
                ),
                html.Label("seconds.", style={'marginRight': '5px'}),
                # save to local database
                dcc.Dropdown(
                    id='save-to-db-dropdown',
                    options=[
                        {'label': 'Save', 'value': 'save'},
                        {'label': "Don't save", 'value': 'dont_save'}
                    ],
                    value='save',
                    clearable=False,
                    searchable=False,
                    style={'width': '128px', 'marginRight': '5px'}
                ),
                html.Label("to database.", style={'marginRight': '5px'}),
                # start, stop and clear buttons.
                html.Button('Start', id='start-button', n_clicks=0,
                            style={'marginRight': '10px'}),
                html.Button('Stop', id='stop-button', n_clicks=0,
                            disabled=True, style={'marginRight': '10px'}),
                html.Button('Clear', id='clear-button', n_clicks=0,
                            style={'marginRight': '10px'})
            ],
                style={
                'display': 'flex',
                'alignItems': 'center',
                'flexWrap': 'wrap',
                'gap': '5px',
                'marginBottom': '20px'
            },
                id='monitoring-controls'),
                
            html.Div([
                html.Label("For", style={'marginRight': '10px'}),
                # dropdown for metric-selector
                dcc.Dropdown(
                    id='metric-selector-dropdown',
                    options=[
                        {'label': 'CPU', 'value': 'cpu'},
                        {'label': "Mem", 'value': 'mem'},
                        {'label': "Tasks", 'value': 'tasks'}
                    ],
                    value='cpu',
                    clearable=False,
                    searchable=False,
                    style={'width': '70px', 'marginRight': '2px'}
                ),
                html.Label("show", style={'marginRight': '10px'}),
                dcc.Dropdown(
                    id='specific-metrics-dropdown',
                    options=[],
                    value=[],
                    multi=True,
                    placeholder="All metrics (select to filter)",
                    style={'width': '500px'}
                ),
                html.Label("on plot.", style={'marginRight': '10px'}),
            ], 
            style={
                'display': 'flex',
                'alignItems': 'center',
                'flexWrap': 'wrap',
                'gap': '5px',
                'marginBottom': '20px'
            },
            id='specific-metrics-container'),
            # main chart
            dcc.Graph(id='droic-plot', style={'height': '500px'}),
            dcc.Interval(
                id='interval-component',
                interval=1000,
                n_intervals=0
            ),
            # separate interval component for device connection check
            dcc.Interval(
                id='device-check-interval',
                interval=2000,  # check every 2 seconds.
                n_intervals=0
            ),
            html.Div(id='auto-stopped-state', style={'display': 'none'}),
            dcc.Store(id='available-metrics-store')
        ], style={'padding': '20px'})
    ], className='dash-container')

    return layout
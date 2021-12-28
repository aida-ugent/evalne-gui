import os
import dash
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from dash import dcc, State, html
from dash.html.Label import Label


dashboard_layout = html.Div([

    html.H3(children='Global and Edge Sampling Parameters'),
    html.Hr(),

    # TASK (dropdown)
        # if LP:
            # LP_NUM_EDGE_SPLITS (text check integer)
            # EDGE_EMBEDDING_METHODS (dropdown)
        # if NR (TODO)
            # NR_EDGE_SAMP_FRAC (text check integer)
            # EDGE_EMBEDDING_METHODS (dropdown)
        # if NC (TODO)
            # NC_NUM_NODE_SPLITS (text check integer)
            # NC_NODE_FRACS (text check frac)
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label(['Evaluation Task:']),
                    dcc.Dropdown(
                        id='task-dropdown',
                        options=[{'label': 'Link prediction', 'value': 'LP'},
                                 {'label': 'Sign prediction', 'value': 'SP'},
                                 {'label': 'Network reconstruction', 'value': 'NR'},
                                 {'label': 'Node classification', 'value': 'NC'}],
                        value='LP',
                    ),
                ],
                style={'width': '30%', 'padding-right': '5%'}
            ),
            html.Div(
                children=[
                    html.Label(['Num Edge Splits:']),
                    dcc.Input(id="input-box-1", className='input-box', type="number", value=5),
                ],
                style={'width': '30%', 'padding-right': '5%'}
            ),
            html.Div(
                children=[
                    html.Label(['Edge Embedding Method:']),
                    dcc.Dropdown(
                        id='ee-dropdown',
                        options=[{'label': 'Average', 'value': 'Avg'},
                                 {'label': 'Hadamard', 'value': 'Had'},
                                 {'label': 'Weighted L1', 'value': 'WL1'},
                                 {'label': 'Weighted L2', 'value': 'WL2'}],
                        value='Avg',
                    ),
                ],
                style={'width': '30%'}
            ),
        ],
        style={'display': 'flex'}
    ),
    html.Br(),

    # LP_MODEL (dropdown + custom input)
    # EMBED_DIM (text check integer)
    # TIMEOUT (text check integer)
    # SEED (text check integer)
    # VERBOSE (checkbox)
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label(['LP model:']),
                    dcc.Dropdown(
                        id='lpmodel-dropdown',
                        options=[{'label': 'LogisticRegression', 'value': 'lr'},
                                 {'label': 'LogisticRegressionCV', 'value': 'lrcv'}],
                        value='lrcv',
                    ),
                ],
                style={'width': '22%', 'padding-right': '4%'}
            ),
            html.Div(
                children=[
                    html.Label(['Embedding dimensionality:']),
                    dcc.Input(id="input-box-2", className='input-box', type="number", value=128),
                ],
                style={'width': '22%', 'padding-right': '4%'}
            ),
            html.Div(
                children=[
                    html.Label(['Evaluation timeout:']),
                    dcc.Input(id="input-box-3", className='input-box', type="number", value=0),
                ],
                style={'width': '22%', 'padding-right': '4%'}
            ),
            html.Div(
                children=[
                    html.Label(['Seed:']),
                    dcc.Input(id="input-box-4", className='input-box', type="number", value=42),
                ],
                style={'width': '22%'}
            ),
        ],
        style={'display': 'flex'}
    ),
    html.Br(),

    # TRAINTEST_FRAC (text check frac)
    # TRAINVALID_FRAC (text check frac)
    # SPLIT_ALG (dropdown)
    # OWA (dropdown)
    # FE_RATIO (text check integer)
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label(['Train-test fraction:']),
                    dcc.Input(id="input-box-5", type="range", value=0.8, min=0, max=1, step=0.1),
                    html.Br(),
                    html.Label(['Train-valid fraction:']),
                    dcc.Input(id="input-box-6", type="range", value=0.9, min=0, max=1, step=0.1),
                ],
                style={'width': '22%', 'padding-right': '4%'}
            ),
            html.Div(
                children=[
                    html.Label(['Split algorithm:']),
                    dcc.Dropdown(
                        id='splitalg-dropdown',
                        options=[{'label': 'Spanning tree', 'value': 'st'},
                                 {'label': 'Random', 'value': 'rand'},
                                 {'label': 'Naive', 'value': 'naive'},
                                 {'label': 'Fast', 'value': 'fast'},
                                 {'label': 'Timestamp', 'value': 'timestamp'}],
                        value='st',
                    ),
                ],
                style={'width': '22%', 'padding-right': '4%'}
            ),
            html.Div(
                children=[
                    html.Label(['Negative sampling:']),
                    dcc.Dropdown(
                        id='negsamp-dropdown',
                        options=[{'label': 'Open world', 'value': 'ow'},
                                 {'label': 'Closed world', 'value': 'cw'}],
                        value='ow',
                    ),
                ],
                style={'width': '22%', 'padding-right': '4%'}
            ),
            html.Div(
                children=[
                    html.Label(['Negative edge ratio:']),
                    dcc.Input(id="input-box-7", className='input-box', type="text", value='1:1'),
                ],
                style={'width': '22%'}
            ),
        ],
        style={'display': 'flex'}
    ),
    html.Br(),

    html.H3(children='Networks and Preprocessing'),
    html.Hr(),

    # NAMES (text)
    # INPATHS (text)
    # LABELPATH (text)
    # DIRECTED (checkbox)
    # SEPARATORS (dropdown + custom input)
    # COMMENTS (dropdown + custom input)
    html.Div(
        children=[
            html.Label(['Network names:']),
            dcc.Input(id="input-box-8", className='input-box', type="text",
                      placeholder="Insert network names separated with blanks..."),
        ],
    ),
    html.Br(),
    html.Div([
        html.Label(['Network edgelist paths:']),
        dcc.Upload(
            id='upload-networks',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Edgelist Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-data-upload'),
    ]),
    html.Br(),
    html.Div([
        html.Label(['Network node label paths:']),
        dcc.Upload(
            id='upload-nodelabels',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Node Label Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-data-upload'),
    ]),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label(['Network type:']),
                    dcc.Checklist(
                        options=[
                            {'label': 'Directed', 'value': 'dir'},
                        ],
                    ),
                ],
                style={'width': '30%', 'padding-right': '5%'}
            ),
            html.Div(
                children=[
                    html.Label(['Separator per edgelist file:']),
                    dcc.Input(id="input-box-10", className='input-box', type="text",
                              placeholder="Insert separators with banks..."),
                ],
                style={'width': '30%', 'padding-right': '5%'}
            ),
            html.Div(
                children=[
                    html.Label(['Comment char per edgelist file:']),
                    dcc.Input(id="input-box-11", className='input-box', type="text",
                              placeholder="Insert comment chars with banks..."),
                ],
                style={'width': '30%'}
            ),
        ],
        style={'display': 'flex'}
    ),
    html.Br(),

    # RELABEL (checkbox)
    # DEL_SELFLOOPS (checkbox)
    # SAVE_PREP_NW (checkbox)
    # WRITE_STATS (checkbox)
    # DELIMITER (dropdown + custom input)
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label(['Network preprocessing:']),
                    dcc.Checklist(
                        options=[
                            {'label': 'Relabel nodes (0..N)', 'value': 'rel'},
                            {'label': 'Remove selfloops', 'value': 'selfloops'},
                        ],
                        value=['rel', 'selfloops'],
                        style={'display': 'grid'}
                    ),
                ],
                style={'width': '30%', 'padding-right': '5%'}
            ),
            html.Div(
                children=[
                    dcc.Checklist(
                        options=[
                            {'label': 'Save network', 'value': 'save'},
                            {'label': 'Write stats', 'value': 'stats'},
                        ],
                        style={'display': 'grid'}
                    ),
                ],
                style={'width': '30%', 'padding-right': '5%', 'padding-top': '20px'}
            ),
            html.Div(
                children=[
                    html.Label(['Preprocessed edgelist delimiter:']),
                    dcc.Dropdown(
                        id='prepdelim-dropdown',
                        options=[{'label': 'Blank', 'value': 'space'},
                                 {'label': 'Comma', 'value': 'comma'},
                                 {'label': 'Tab', 'value': 'tab'}],
                        value='comma',
                    ),
                ],
                style={'width': '30%'}
            ),
        ],
        style={'display': 'flex'}
    ),

    html.H3(children='Baselines and NE methods'),
    html.Hr(),
    html.Br(),

    html.H3(children='Metrics and Plots'),
    html.Hr(),
    # MAXIMIZE (dropdown)
    # SCORES (dropdown)
    # CURVES (dropdown)
    # PRECATK_VALS (text??)
    html.Div(
        children=[
            html.Div(
                children=[
                    # TODO: if NC the options in the dropdown should be different
                    html.Label(['Metric to maximize:']),
                    dcc.Dropdown(
                        id='maximize-dropdown',
                        options=[
                            {'label': 'AUC', 'value': 'auc'},
                            {'label': 'F-score', 'value': 'fscore'},
                            {'label': 'Precision', 'value': 'prec'},
                            {'label': 'Recall', 'value': 'rec'},
                            {'label': 'Accuracy', 'value': 'acc'},
                            {'label': 'Fallout', 'value': 'fall'},
                            {'label': 'Miss', 'value': 'miss'}
                        ],
                        value='auc',
                    ),
                ],
                style={'width': '22%', 'padding-right': '4%'}
            ),
            html.Div(
                children=[
                    html.Label(['Scores to report:']),
                    dcc.Dropdown(
                        id='scores-dropdown',
                        options=[
                            {'label': 'All', 'value': 'all'},
                            {'label': 'AUC', 'value': 'auc'},
                            {'label': 'F-score', 'value': 'fscore'},
                            {'label': 'Precision', 'value': 'prec'},
                            {'label': 'Recall', 'value': 'rec'},
                            {'label': 'Accuracy', 'value': 'acc'},
                            {'label': 'Fallout', 'value': 'fall'},
                            {'label': 'Miss', 'value': 'miss'}
                        ],
                        value='all',
                    ),
                ],
                style={'width': '22%', 'padding-right': '4%'}
            ),
            html.Div(
                children=[
                    html.Label(['Curves to compute:']),
                    dcc.Dropdown(
                        id='curves-dropdown',
                        options=[
                            {'label': 'None', 'value': 'none'},
                            {'label': 'ROC', 'value': 'roc'},
                            {'label': 'PR', 'value': 'pr'},
                            {'label': 'All', 'value': 'all'}],
                        value='roc',
                    ),
                ],
                style={'width': '22%', 'padding-right': '4%'}
            ),
            html.Div(
                children=[
                    html.Label(['Precision@k values:']),
                    dcc.Input(id="input-box-12", className='input-box', type="text",
                              placeholder='K values for Prec@k (e.g. 1 10 100 1000)'),
                ],
                style={'width': '22%'}
            ),
        ],
        style={'display': 'flex'}
    ),
    html.Br(),
    html.Br(),
    html.Div([
        html.Button('Run Evaluation', id='run-eval', n_clicks=0),
    ]),
    html.Br(),
    html.Br(),
])





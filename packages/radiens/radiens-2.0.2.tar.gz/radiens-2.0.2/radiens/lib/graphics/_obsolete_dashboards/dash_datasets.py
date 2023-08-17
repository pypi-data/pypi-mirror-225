import sys
import threading
import queue
import argparse
import queue
import time
import json
from pathlib import Path
import numpy as np
import tempfile

from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from dash.exceptions import PreventUpdate
import dash_daq as daq

import lib
import lib_backend as backend

layout = html.Div(
    [
        html.Div(
            [
                html.H3(
                    'RADIENS:DataViz -- Linked Datasets',
                    disable_n_clicks=True,
                    style={"width": "100%", "text-align":
                           "left", "font-weight":
                           "bold", 'fontSize': 20},
                ),
                html.Div(
                    html.A('NeuroNexus Knowledge Center',
                           href='https://neuronexus.com',
                           target='_blank'),
                    disable_n_clicks=True,
                    style={"width": "100%",
                           "text-align": "right",
                           "font-weight": "bold",
                           'fontSize': 14},
                ),
            ],
        ),
        html.Div(
            [
                dash_table.DataTable(
                    backend.get_linked_dsource_list(True).to_dict('records'),
                    [{"name": i, "id": i} for i in backend.get_linked_dsource_list(True).columns],
                    id='linked-dset',
                    editable=False,
                    sort_action='native',
                    sort_mode='multi',
                    row_selectable='single',
                    cell_selectable=False,
                    column_selectable=False,
                    page_action="native",
                    page_current=0,
                    page_size=10,
                    selected_rows=[],
                    persistence=True,
                    style_header={
                        # 'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'black',
                        'textAlign': 'left',
                        'border': '2px solid blue',
                        'font-family': 'sans-serif',
                        'fontSize': 12,
                    },
                    style_data={
                        # 'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'black',
                        'textAlign': 'left',
                        'border': '1px solid blue',
                        'font-family': 'sans-serif',
                        'fontSize': 12,
                    },
                    style_as_list_view=True,
                ),

            ],
        )
    ],
)


@ callback(
    Output('cmd-line', 'data'),
    Input('cmd-line', 'modified_timestamp'))
def parse_cmd_line(timestamp):
    print('FIRED parse_cmd_line: timestamp=', timestamp)
    # if timestamp is None:  # no-op start up call
    #     raise PreventUpdate()
    args = lib.parser.parse_args()
    return {'dash_uid': args.dash_uid, 'dsrc_id': None}


@ callback(
    Output('linked-dset', 'data'),
    Input('ticker_datasets', 'n_intervals'),
)
def dset_table_init(intervals):
    '''  '''
    df = backend.videre.get_dataset_ids()
    df.columns = ['Dataset ID', 'Base Name']
    df['id'] = df.reset_index(drop=True).index.map(str)
    return df.to_dict('records')


@ callback(
    Output('dsrc-id', 'data'),
    Input('cmd-line', 'data'),
)
def dsrc_id_init(args):
    '''always fired at launch '''
    if 'dsrc_id' not in args:
        return {'dsrc_id': None, 'row_idx': -1, 'col_idx': -1}
    return {'dsrc_id': args['dsrc_id'], 'row_idx': -1, 'col_idx': -1}


@ callback(
    Output('dsrc-id', 'data', allow_duplicate=True),
    Input('linked-dset', 'selected_row_ids'),
    State('linked-dset', 'data'),
    prevent_initial_call=True,
)
def sel_dset_on_selected_rows(sel_row_ids, tbl):
    ''' '''
    df = pd.DataFrame.from_dict(tbl)
    if sel_row_ids is None or len(df) == 0:
        raise PreventUpdate()
    dsrc_id = df.loc[df['id'] == str(sel_row_ids[0])]
    if len(dsrc_id) != 1:
        raise PreventUpdate()
    return {'dsrc_id': dsrc_id['Dataset ID'].tolist()[0], 'row_idx': -1, 'col_idx': -1}


@ callback(
    Output('linked-dset', 'selected_rows_ids'),
    Input('dsrc-id', 'data'),
    State('linked-dset', 'data'),
    State('linked-dset', 'selected_row_ids'),
)
def sel_dset_on_dsrc_id(dsrc_id, tbl, in_sel_row_ids):
    ''' '''
    df = pd.DataFrame.from_dict(tbl)
    if len(df) == 0 or dsrc_id is None:
        raise PreventUpdate()
    new_row_id = df.loc[df['Dataset ID'] == dsrc_id]
    if len(new_row_id) != 1:
        raise PreventUpdate()
    new_row_id = new_row_id['id'][0]
    if len(in_sel_row_ids) == 1 and new_row_id == in_sel_row_ids[0]:
        raise PreventUpdate()
    return [new_row_id]


@ callback(
    Output('dsrc_metadata', 'data'),
    Input('dsrc-id', 'data'),
)
def update_dsrc_meta_settings(data):
    ''' '''
    if data is None or not 'dsrc_id' in data or data['dsrc_id'] is None:
        raise PreventUpdate()
    try:
        meta = backend.videre.get_data_file_metadata(dataset_id=data['dsrc_id'], fail_hard=True)
    except Exception as ex:
        print('failed to get meta data from {}'.format(data['dsrc_id']), file=os.strerror, flush=True)
        raise PreventUpdate()
    meta_json = meta.as_json()
    return meta_json


@ callback(
    Output('dsrc_TR', 'data'),
    Input('dsrc_metadata', 'data'),
)
def update_dsrc_TR(meta_json):
    ''' '''
    print('\n\n\nFIRE get TR: ', meta_json)
    if meta_json is None:
        raise PreventUpdate()
    meta = json.loads(meta_json)
    return meta['TR']

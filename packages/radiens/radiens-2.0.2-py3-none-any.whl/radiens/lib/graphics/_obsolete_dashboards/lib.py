import os
import sys
import yaml
import shutil
import argparse
import numpy as np
import pandas as pd
from pathlib import Path
import json

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
from radiens.utils.constants import (SIGNALS, TIME_RANGE, TRS_MODE, SignalType)
from radiens.lib.sig_metrics import (SignalMetrics)
from radiens.lib.signals_snapshot import (PSD)
from radiens import VidereClient


# =============================
# backend
# =============================

# def dash_start_path() -> str:
#     return str(Path(os.path.realpath(__file__)).resolve().parent)


def get_linked_dsource_list(init: bool) -> pd.DataFrame:
    if init:
        df = pd.DataFrame({'Dataset ID': [], 'Base Name': []})
    else:  # mocks getting from back end
        df = pd.DataFrame({'Dataset ID': ['dset_1', 'dset_2'], 'Base Name': ['blah', 'blah 2x']})
    df['id'] = df.reset_index(drop=True).index
    return df


videre = VidereClient()


# https://css-tricks.com/snippets/css/a-guide-to-flexbox/


parser = argparse.ArgumentParser(prog='radiens-py dashboard', description='dashboard command line')
parser.add_argument('-cmd', choices=['DASH_CMD_OPEN', 'DASH_CMD_CLOSE',
                                     'DASH_CMD_INIT', 'DASH_CMD_UPDATE', 'DASH_CMD_EXIT'], type=str, help='dashboard command')
parser.add_argument('-port', dest='port',  type=int, help='dash server port')
parser.add_argument('-uid', dest='dash_uid',  type=str, help='dashboard UID')
parser.add_argument('-dsrcID', dest='dsrc_id', type=str, help='datasource ID')
parser.add_argument('-mode', dest='metric_mode', type=int, help='signal metric mode (enum value)')
parser.add_argument('-metric', dest='metric', type=int, help='signal metric (enum value)')

# =============================
# DASH LAYOUTS
# =============================

# df_dataset_table_init = pd.DataFrame({'Dataset ID': [], 'Base Name': [], 'id': []})
# df_dataset_table_cols = ['Dataset ID', 'Base Name', 'id'
# global for all dashboards
STYLE_SHEETS = {'lux': dbc.themes.LUX, 'darkly': dbc.themes.DARKLY}
TICKER_PERIOD_MS = {'ticker_1': 1000}

# load_figure_template(STYLE_SHEETS['darkly'])
# app = Dash(__name__,
#            # suppress_callback_exceptions=True,
#            external_stylesheets=[STYLE_SHEETS['darkly']],
#            meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],)

# layout_style = {
#     # 'border': 'solid 1px #A2B1C6',
#     # 'border-radius': '5px',
#     # 'padding': '20px',
#     # 'margin-top': '15px'
# }

# c_stores_1 = html.Div(
#     [
#         dcc.Store(id='cmd-line', storage_type='memory'),
#         dcc.Store(id='dsrc-id', storage_type='memory'),  # KEY for getting dsource meta {'dsrc_id', 'row_idx', 'col_idx'}
#         dcc.Store(id='dsrc_metadata', storage_type='memory'),
#         dcc.Store(id='dsrc_TR', storage_type='memory'),
#         dcc.Store(id='sel_TR', storage_type='memory'),
#     ], hidden=True
# )

# c_interval_1 = dcc.Interval(
#     id='ticker_1',
#     interval=1*TICKER_PERIOD_MS['ticker_1'],  # in milliseconds
#     n_intervals=0,
# )


# def c_title(name):
#     return html.H1('RADIENS:DataViz -- {}'.format(name),
#                    disable_n_clicks=True,
#                    style={"width": "100%", "text-align":
#                           "left", "font-weight":
#                           "bold", 'fontSize': 20},)


# c_knowledge_ctr = html.Div(html.A('NeuroNexus Knowledge Center',
#                            href='https://neuronexus.com',
#                            target='_blank'),
#                            disable_n_clicks=True,
#                            style={"width": "100%",
#                            "text-align": "right",
#                                   "font-weight": "bold",
#                                   'fontSize': 14})


# c_dataset_modal = html.Div(
#     [
#         dbc.Button("Linked Datasets", id="dset_list_open", n_clicks=0),
#         dbc.Modal(
#             [
#                 dbc.ModalHeader(dbc.ModalTitle("Linked Datasets on Radiens Hub")),
#                 # dbc.ModalBody('This is modal body'),
#                 dash_table.DataTable(
#                     get_linked_dsource_list(True).to_dict('records'),
#                     [{"name": i, "id": i} for i in get_linked_dsource_list(True).columns],
#                     id='linked-dset',
#                     editable=False,
#                     sort_action='native',
#                     sort_mode='multi',
#                     row_selectable='single',
#                     cell_selectable=False,
#                     column_selectable=False,
#                     page_action="native",
#                     page_current=0,
#                     page_size=10,
#                     selected_rows=[],
#                     persistence=True,
#                     style_header={
#                         # 'backgroundColor': 'rgb(30, 30, 30)',
#                         'color': 'black',
#                         'textAlign': 'left',
#                         'border': '2px solid blue',
#                         'font-family': 'sans-serif',
#                         'fontSize': 12,
#                     },
#                     style_data={
#                         # 'backgroundColor': 'rgb(50, 50, 50)',
#                         'color': 'black',
#                         'textAlign': 'left',
#                         'border': '1px solid blue',
#                         'font-family': 'sans-serif',
#                         'fontSize': 12,
#                     },
#                     style_as_list_view=True,
#                 ),
#                 dbc.ModalFooter(
#                     dbc.Button(
#                         "Close", id="dset_list_close", className="ms-auto", n_clicks=0
#                     )
#                 ),
#             ],
#             id="dset_list_modal",
#             is_open=False,
#             size="lg",
#         ),
#     ]
# )

# c_signals_modal = html.Div(
#     [
#         dbc.Button("Linked Datasets", id="dset_list_open", n_clicks=0),
#         dbc.Modal(
#             [
#                 dbc.ModalHeader(dbc.ModalTitle("Linked Datasets on Radiens Hub")),
#                 # dbc.ModalBody('This is modal body'),
#                 dash_table.DataTable(
#                     get_linked_dsource_list(True).to_dict('records'),
#                     [{"name": i, "id": i} for i in get_linked_dsource_list(True).columns],
#                     id='linked-dset',
#                     editable=False,
#                     sort_action='native',
#                     sort_mode='multi',
#                     row_selectable='single',
#                     cell_selectable=False,
#                     column_selectable=False,
#                     page_action="native",
#                     page_current=0,
#                     page_size=10,
#                     selected_rows=[],
#                 ),
#                 dbc.ModalFooter(
#                     dbc.Button(
#                         "Close", id="dset_list_close", className="ms-auto", n_clicks=0
#                     )
#                 ),
#             ],
#             id="dset_list_modal",
#             is_open=False,
#             size="lg",
#         ),
#     ]
# )


# =============================
# DASH CALLBACKS
# =============================

# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open


# @ callback(
#     Output("dset_list_modal", "is_open"),
#     [Input("dset_list_open", "n_clicks"), Input("dset_list_close", "n_clicks")],
#     [State("dset_list_modal", "is_open")],
# )(toggle_modal)
#
#
# command line callbacks
# @ callback(
#     Output('cmd-line', 'data'),
#     Input('cmd-line', 'modified_timestamp'))
# def parse_cmd_line(timestamp):
#     print('FIRED parse_cmd_line: timestamp=', timestamp)
#     # if timestamp is None:  # no-op start up call
#     #     raise PreventUpdate()
#     args = parser.parse_args()
#     print('args =', args)
#     return {'dash_uid': args.dash_uid, 'dsrc_id': None}

# # ========
# # dataset table callbacks


# @ callback(
#     Output('linked-dset', 'data'),
#     Input('ticker_1', 'n_intervals'),
# )
# def dset_table_init(intervals):
#     '''  '''
#     df = videre.get_dataset_ids()
#     df.columns = ['Dataset ID', 'Base Name']
#     df['id'] = df.reset_index(drop=True).index.map(str)
#     return df.to_dict('records')


# @ callback(
#     Output('dsrc-id', 'data'),
#     Input('cmd-line', 'data'))
# def dsrc_id_init(args):
#     '''always fired at launch '''
#     print('FIRED dsrc_id_init: args=', args)
#     if 'dsrc_id' not in args:
#         return {'dsrc_id': None, 'row_idx': -1, 'col_idx': -1}
#     return {'dsrc_id': args['dsrc_id'], 'row_idx': -1, 'col_idx': -1}


# @ callback(
#     Output('dsrc-id', 'data', allow_duplicate=True),
#     Input('linked-dset', 'selected_row_ids'),
#     State('linked-dset', 'data'),
#     prevent_initial_call=True,
# )
# def sel_dset_on_selected_rows(sel_row_ids, tbl):
#     ''' '''
#     df = pd.DataFrame.from_dict(tbl)
#     if sel_row_ids is None or len(df) == 0:
#         raise PreventUpdate()
#     dsrc_id = df.loc[df['id'] == str(sel_row_ids[0])]
#     if len(dsrc_id) != 1:
#         raise PreventUpdate()
#     return {'dsrc_id': dsrc_id['Dataset ID'].tolist()[0], 'row_idx': -1, 'col_idx': -1}


# @ callback(
#     Output('linked-dset', 'selected_rows'),
#     Input('dsrc-id', 'data'),
#     State('linked-dset', 'data'),
#     State('linked-dset', 'selected_row_ids'),
# )
# def sel_dset_on_dsrc_id(dsrc_id, tbl, in_sel_row_ids):
#     ''' '''
#     df = pd.DataFrame.from_dict(tbl)
#     if len(df) == 0 or dsrc_id is None:
#         raise PreventUpdate()
#     new_row_id = df.loc[df['Dataset ID'] == dsrc_id]
#     if len(new_row_id) != 1:
#         raise PreventUpdate()
#     new_row_id = new_row_id['id'][0]
#     if len(in_sel_row_ids) == 1 and new_row_id == in_sel_row_ids[0]:
#         raise PreventUpdate()
#     return [new_row_id]


# @ callback(
#     Output('dsrc_metadata', 'data'),
#     Input('dsrc-id', 'data'),
# )
# def update_dsrc_meta_settings(data):
#     ''' '''
#     if data is None or not 'dsrc_id' in data or data['dsrc_id'] is None:
#         raise PreventUpdate()
#     try:
#         meta = videre.get_data_file_metadata(dataset_id=data['dsrc_id'], fail_hard=True)
#     except Exception:
#         print('failed to get meta data from {}'.format(data['dsrc_id']), file=os.strerror, flush=True)
#         raise PreventUpdate()
#     meta_json = meta.as_json()
#     return meta_json


# @ callback(
#     Output('dsrc_TR', 'data'),
#     Input('dsrc_metadata', 'data'),
# )
# def update_dsrc_TR(meta_json):
#     ''' '''
#     print('\n\n\nFIRE get TR: ', meta_json)
#     if meta_json is None:
#         raise PreventUpdate()
#     meta = json.loads(meta_json)
#     return meta['TR']

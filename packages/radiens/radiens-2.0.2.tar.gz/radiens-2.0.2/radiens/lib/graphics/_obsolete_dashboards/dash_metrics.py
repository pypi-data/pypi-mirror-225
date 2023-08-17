import sys
import threading
import queue
import argparse
import queue
import time
from pathlib import Path
import numpy as np
import tempfile

from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from dash.exceptions import PreventUpdate
import dash_daq as daq


from radiens.exceptions.grpc_error import handle_grpc_error
import radiens.grpc_radiens.pyradiens_pb2_grpc as pyradiens_pb2_grpc
from radiens.api.api_utils.util import scan_for_open_port
from radiens.grpc_radiens import (
    common_pb2, pyradiens_pb2)
import radiens.lib.graphics.dashboards.lib_plotly as dl
from radiens.utils.util import make_time_range
from radiens.lib.sig_metrics import (SignalMetrics, SignalMetricsStatus, METRIC_ID, METRIC_MODE, METRIC)

import lib as dl
from lib import c_stores_1

app = dl.app
app.title = "Signal Metrics"
app.layout = html.Div(
    [
        c_stores_1,
        dl.c_interval_1,
        dl.c_title('Signal Metrics Dashboard'),
        html.Div([dl.c_knowledge_ctr],),
        html.Div(
            [
                dl.c_dataset_modal,
                dl.c_signals_modal,
                html.Div(
                    [
                        html.Label(['Metric mode'],
                                   key='metric_mode_key',
                                   style={'font-weight': 'bold', "text-align": "left"},
                                   title='Signal metric modes (see https://neuronexus.com)'),
                        dcc.Dropdown(
                            id='metric_mode',
                            options=[
                                {'label': 'packet', 'value': 'packet', 'title': 'metrics by packet from start of stream'},
                                {'label': 'cumul packet', 'value': 'cumul_packet', 'title': 'cumulative packet metrics from start of stream'},
                                {'label': 'stream', 'value': 'stream', 'title': 'cumulative from start of stream'},
                            ],
                            value='select metric mode 2...',
                            clearable=False,
                            searchable=False,
                            persistence=True,
                            placeholder='select mode...',
                            style={
                                'color': 'black',
                            }
                        ),
                    ],
                    style=dict(width='20%')
                ),
                html.Div(
                    [
                        html.Label(['Metric'],
                                   key='metric_mode_key',
                                   style={'font-weight': 'bold', "text-align": "left"},
                                   title='Signal metric (see https://neuronexus.com)'),
                        dcc.Dropdown(
                            id='metric',
                            options=[
                                {'label': 'abs max', 'value': 'abs_max'},
                                {'label': 'abs p2p', 'value': 'abs_p2p'},
                                {'label': 'std dev', 'value': 'sd'},
                                {'label': 'rms', 'value': 'rms'},
                                {'label': 'SNR', 'value': 'snr'},
                                {'label': 'event rate', 'value': 'evt_rate'},
                                {'label': 'event abs max', 'value': 'evt_abs_max'},
                                {'label': 'event abs p2p', 'value': 'evt_abs_p2p'},
                                {'label': 'event mean abs max', 'value': 'evt_mean_abs_max'},
                                {'label': 'event mean abs p2p', 'value': 'evt_mean_abs_p2p'},
                            ],
                            value='select metric...',
                            clearable=False,
                            searchable=False,
                            persistence=True,
                            style={
                                'color': 'black',
                            }
                        ),
                    ],
                    style=dict(width='20%')
                ),
                html.Div(
                    [
                        html.Label(['Metric time bin (sec)'],
                                   key='metric_time_bin',
                                   style={'font-weight': 'bold', "text-align": "left"},
                                   title='Signal metric time bin (see https://neuronexus.com)'),
                        daq.NumericInput(
                            id='metric_pkt_width',
                            value=0.5,
                            min=0.1,
                            max=10.0,
                            persistence=True,
                            style={
                                'color': 'black',
                            }

                        ),
                    ],
                    style=dict(width='20%')
                ),
                html.Div(
                    [
                        html.Label(['Synchronize'],
                                   key='sync_dashboards',
                                   style={'font-weight': 'bold', "text-align": "left"},
                                   title='Synchronize settings across active dashboards'),
                        dcc.Checklist(
                            id='sync_checkbox',
                            options=[
                                {'label': 'sync', 'value': 'sync', 'title': 'synchronize settings'},
                            ],
                            value=[],
                            inline=True,
                            persistence=True,
                        ),
                    ],
                    style=dict(width='20%')
                )
            ],
            style={
                'display': 'flex'
            }
        ),
        html.Div(
            [
                dcc.Graph(id='live-update-graph',
                          figure=dict(
                              layout=go.Layout(
                                  plot_bgcolor='rgba(0,0,0,0)',  # app_color["graph_bg"],
                                  paper_bgcolor='rgba(0,0,0,0)',  # app_color["graph_bg"],
                              )
                          ),
                          ),
            ]
        ),
        html.Br(),
        html.Div(
            [
                html.Label(['Dataset Time Range [sec]'],
                           key='t_range_sel_key',
                           style={'font-weight': 'bold', "text-align": "left"},
                           title='select the dataset sub-range by moving the sliders'),
                dcc.RangeSlider(id='time-range-slider', min=0, max=20, step=None, value=[0, 10],
                                tooltip={"placement": "bottom", "always_visible": True},
                                allowCross=False,
                                included=False,
                                updatemode='mouseup',
                                persistence=True),
            ],
            style={'width': '75%', 'padding': '25px', 'margin-left': '40px'},
        ),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        html.Div("(radiens) dash % "),
                        dcc.Input(id='mock_stdin', value='initial value', type='text'),
                        html.Div(id='live-update-text'),
                    ]
                ),
            ],
        ),
    ],
    style=dl.layout_style,
)


@ callback()(
    Output('mock_stdin', 'value'),
    Input('ticker_1', 'n_intervals'))
def update_mock_stdin(interval):
    if interval % 5 == 0:
        cmd_line = '-tstart {} -tend {}'.format(interval, interval+10)
    else:
        raise PreventUpdate('no update {}'.format(interval))
    return f'{cmd_line}'


@ callback()(
    Output('live-update-text', 'children'),
    Input('mock_stdin', 'value')
)
def update_status_text(input_value):
    return f'status: {input_value}'


@ callback(
    Output('time-range-slider', 'min'),
    Input('ticker_1', 'n_intervals'),
    State('dsrc_TR', 'data'),
)
def update_t_range_slider_min(intervals, tr):
    ''' '''
    if tr is None:
        raise PreventUpdate()
    print(' HEY updated slide min  ',  intervals,  tr['sec'][0])
    return tr['sec'][0]


@ callback(
    Output('time-range-slider', 'max'),
    Input('ticker_1', 'n_intervals'),
    State('dsrc_TR', 'data'),
)
def update_t_range_slider_max(intervals, tr):
    ''' '''
    if tr is None:
        raise PreventUpdate()
    print(' YO YO updated slide max  ', intervals, tr['sec'][1])
    return tr['sec'][1]


# @ dl.app.callback()(Output('live-update-graph', 'figure'),
#                     Input('ticker_1', 'n_intervals'),
#                     Input('time-range-slider', 'value'),
#                     #    [Input('time-sync_checkbox-slider', 'value')],
#                     )
# def update_graph_live(interval, tr_value):
#     print('live-graph: tick interval=, value= state=', interval, tr_value, state.has_data)

#     if not state.has_data or state.is_equal_sel_time_range(tr_value[0], tr_value[1]):
#         raise PreventUpdate()
#     state.d['TR'] = make_time_range(time_range=tr_value, fs=state.d['TR'].fs)

#     try:
#         state.d['metrics'] = state.videre.signal_metrics().get_metrics(state.d['TR'].sec,
#                                                                        metrics=[state.d['sel_metric_id']],
#                                                                        tail=False, dataset_metadata=state.d['dsrc_meta'])
#     except Exception as ex:
#         print(' !!!! EXCEPTION')
#         raise PreventUpdate()

#     if state.d['metrics'].settings['num_packets'] == 0 or state.d['metrics'].settings['num_sigs'] == 0:
#         print(' !!!! zeros!!')
#         raise PreventUpdate()

#     yaxis = np.arange(state.d['metrics'].time_range.sec[0], state.d['metrics'].time_range.sec[1],
#                       state.d['metrics'].settings['packet_dur_sec'])
#     k = 0
#     print('req TR=   metric TR=   packet_dur=', state.d['TR'], state.d['metrics'].time_range, state.d['metrics'].settings['packet_dur_sec'])
#     print('yaxis shape={}, xaxis={} metrics ={}'.format(yaxis.shape,
#           state.d['metrics'].settings['num_sigs'], state.d['metrics'].val[:, :, k].T.shape))
#     if yaxis.shape[0] != state.d['metrics'].val[:, :, k].T.shape[1]:
#         yaxis = yaxis[:state.d['metrics'].val[:, :, k].T.shape[1]]
#     print('yaxis = ', yaxis)
#     trace = dict(
#         type="surface",
#         y=yaxis,
#         x=np.arange(0, state.d['metrics'].settings['num_sigs']),
#         z=state.d['metrics'].val[:, :, k],
#         hoverinfo="skip",
#         colorscale='Jet',
#         showscale=True,
#         render_mode='webgl',
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',  # app_color["graph_bg"],
#     )

#     layout = dict(
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         font={"color": "#fff"},
#         height=DEFAULTS['fig_size'][0],
#         width=DEFAULTS['fig_size'][1],
#         scene=dict(aspectmode='auto',
#                    aspectratio=dict(x=1, y=5, z=1.0),
#                    xaxis=dict(range=[0, state.d['metrics'].settings['num_sigs']]),
#                    yaxis=dict(range=state.d['metrics'].time_range),
#                    zaxis=dict(range=[0, state.d['metrics'].val[:, :, k].T.max()]),
#                    yaxis_title='Time Elapsed (sec)', xaxis_title='Signal', zaxis_title='Metric val',
#                    ),
#     )
#     state.fig = dict(data=[trace], layout=layout)
#     return state.fig


def grfx_main() -> bool:
    while True:
        time.sleep(0.75)
        try:
            args = stdin_queue.get(block=False)
        except queue.Empty:
            continue


def stdin_main(mock_stdin: Path = None):
    while True:
        if mock_stdin.exists() and mock_stdin.stat().st_size > 0:
            with open(mock_stdin, mode='r') as f:
                f.seek(0)
                line = f.readlines()
            open(mock_stdin, mode='w').close()
            args = dl.parser.parse_args(line[0].split())  # blocks until <enter>
            stdin_queue.put(args)
            if args.cmd in ['DASH_CMD_EXIT']:
                return
        time.sleep(1.0)


def main(args):
    args = dl.parser.parse_args()
    mock_stdin = Path('./', args.dash_uid+'.i')
    mock_stdout = Path('./', args.dash_uid+'.o')
    stdin_thread = threading.Thread(target=stdin_main, kwargs={'mock_stdin': mock_stdin}, daemon=True)
    stdin_thread.start()
    port = 8050 if args.port is None else args.port
    dl.app.run_server(port=port, debug=False)  # block until exit
    print('!#USER_SYS_EXIT', flush=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

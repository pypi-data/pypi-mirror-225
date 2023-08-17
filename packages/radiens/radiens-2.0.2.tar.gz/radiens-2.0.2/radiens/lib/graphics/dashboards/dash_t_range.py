import sys
import os
import threading
import queue
import argparse
import queue
import time
import numpy as np
from concurrent import futures
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
from matplotlib.gridspec import GridSpec
from matplotlib import cm
from matplotlib.widgets import TextBox

import grpc
from radiens import VidereClient
from radiens.exceptions.grpc_error import handle_grpc_error
import radiens.grpc_radiens.pyradiens_pb2_grpc as pyradiens_pb2_grpc
from radiens.api.api_utils.util import scan_for_open_port
from radiens.grpc_radiens import (
    common_pb2, pyradiens_pb2)
import radiens.lib.graphics.dashboards.lib as dl
from radiens.utils.util import make_time_range
from radiens.lib.graphics.dashboards.lib import (DashBoard)
from radiens.lib.sig_metrics import (SignalMetrics, SignalMetricsStatus, METRIC_ID, METRIC_MODE, METRIC)


stdin_queue = queue.Queue()

mpl.use('Qt5Agg')

# specific to this dashboard
DEFAULTS = {'sup_title': 'Time selection',
            'fig_size': (12, 6),
            'grfx_main_loop_sleep_sec': 0.027,
            'stdin_main_loop_sleep_sec': 0.033}  # width, height


class TimeSelectionDashBoard(DashBoard):
    def __init__(self, sup_title: str, fig_size: tuple) -> None:
        super().__init__(sup_title, fig_size)
        self._videre = VidereClient()
        self._d = {'full': {}, 'sub': {}}
        self._fobj = {'full': {}, 'sub': {}}
        self._ax = {'full': None, 'sub': None}

    def open(self, args: argparse.Namespace) -> None:
        super().open(args)
        if args.dsrc_id is None:
            raise ValueError('missing dsrc_id arg')
        self._dsrc_id = args.dsrc_id
        if args.metric_mode is None or args.metric is None:
            raise ValueError('missing metric mode and/or name')

        # update data
        self._d['sel_metric_id'] = METRIC_ID(mode=METRIC_MODE(args.metric_mode), name=METRIC(args.metric))
        self._d['dsrc_meta'] = self._videre.get_data_file_metadata(dataset_id=self._dsrc_id, fail_hard=True)
        self._d['full']['TR'] = self._d['dsrc_meta'].time_range
        self._d['full']['metrics'] = self._videre.signal_metrics().get_metrics(self._d['full']['TR'].sec,
                                                                               metrics=[self._d['sel_metric_id']],
                                                                               tail=False, dataset_metadata=self._d['dsrc_meta'])
        self._d['sub']['TR'] = self._d['dsrc_meta'].time_range
        self._d['sub']['metrics'] = self._videre.signal_metrics().get_metrics(self._d['sub']['TR'].sec,
                                                                              metrics=[self._d['sel_metric_id']],
                                                                              tail=False, dataset_metadata=self._d['dsrc_meta'])

        # update graphics
        gs = GridSpec(2, 1, figure=self._fig, height_ratios=[2, 1])
        self._ax['sub'] = self._fig.add_subplot(gs[0, 0])  # subset time range
        self._ax['full'] = self._fig.add_subplot(gs[1, 0])  # full time range
        self._fobj['full']['title'] = self._ax['full'].set_title('{}\n{}:{}'.format(str(Path(self._d['dsrc_meta'].path, self._d['dsrc_meta'].base_name)),
                                                                                    self._d['sel_metric_id'].mode.name, self._d['sel_metric_id'].name.name),
                                                                 fontdict=dl.TXT_STYLE['title'], loc='left')
        self._fobj['sub']['title'] = self._ax['sub'].set_title('Subset region', fontdict=dl.TXT_STYLE['title'], loc='left')
        self._compose_data_axes()

        self._fobj['full']['span'] = SpanSelector(
            self._ax['full'],
            self._widget_on_select,
            "horizontal",
            useblit=True,
            props=dict(alpha=0.5, facecolor="tab:blue"),
            interactive=True,
            drag_from_anywhere=True)

        plt.show(block=False)
        print('!#OPEN_OK', flush=True)

    def close(self) -> None:
        super().close()

    def init(self) -> None:
        super().init()

    def command(self, args: argparse.Namespace) -> None:
        args.is_frac_time = bool(args.is_frac_time)
        super().command(args)
        if args.command in ['DASH_CMD_OPEN']:
            self.open(args)
        elif args.command in ['DASH_CMD_UPDATE']:
            self.update(args)

    def update(self, args: argparse.Namespace) -> None:
        print('nothing to update')
        print('!#UPDATE_OK', flush=True)

    def _compose_data_axes(self):
        k = 0
        _interpolation = 'antialiased'
        for sptype in ['full', 'sub']:
            self._ax[sptype].set_ylabel('signal', fontdict=dl.TXT_STYLE['label_1'])
            self._ax[sptype].set_xlabel('time (seconds)', fontdict=dl.TXT_STYLE['label_1'])
            self._ax[sptype].tick_params(axis='both', which='major', labelsize=dl.TXT_STYLE['label_1']['fontsize'])
            self._ax[sptype].tick_params(axis='both', which='minor', labelsize=dl.TXT_STYLE['label_2']['fontsize'])
            self._fobj[sptype]['taxis'] = np.arange(self._d[sptype]['TR'].sec[0], self._d[sptype]
                                                    ['TR'].sec[1], 1/self._d[sptype]['TR'].fs)
            self._fobj[sptype]['pkt_taxis'] = np.arange(self._d[sptype]['TR'].sec[0], self._d[sptype]['TR'].sec[1],
                                                        self._d[sptype]['metrics'].settings['packet_dur_sec'])

            self._ax[sptype].set_xlim(self._d[sptype]['metrics'].time_range.sec)
            self._fobj[sptype]['img'] = self._ax[sptype].imshow(self._d[sptype]['metrics'].val[:, :, k].T, cmap=dl.COLOR_MAP['default'],
                                                                aspect='auto',
                                                                interpolation=_interpolation,
                                                                animated=True,
                                                                extent=(self._d[sptype]['metrics'].time_range.sec[0], self._d[sptype]['metrics'].time_range.sec[1],
                                                                        0, self._d[sptype]['metrics'].settings['num_sigs']), origin='lower')
            self._fobj[sptype]['cbar'] = self._fig.colorbar(
                self._fobj[sptype]['img'], ax=self._ax[sptype], location='bottom', shrink=4.0, aspect=20)
            self._fobj[sptype]['cbar'].set_label('metric', rotation=0, size='small')
            self._fobj[sptype]['cbar'].ax.tick_params(labelsize=dl.TXT_STYLE['label_2']['fontsize'])
        return

    def _widget_on_select(self, xmin_s, xmax_s):
        indmin, indmax = np.searchsorted(self._fobj['full']['taxis'], (xmin_s, xmax_s))
        indmax = min(len(self._fobj['full']['taxis']) - 1, indmax)
        region_x = self._fobj['full']['taxis'][indmin:indmax]

        k = 0
        if len(region_x) >= 2:
            # update data
            self._d['sub']['TR'] = make_time_range(time_range=[xmin_s, xmax_s], fs=self._d['sub']['TR'].fs)
            self._d['sub']['metrics'] = self._videre.signal_metrics().get_metrics(self._d['sub']['TR'].sec,
                                                                                  metrics=[self._d['sel_metric_id']],
                                                                                  tail=False, dataset_metadata=self._d['dsrc_meta'])

            # update graphics
            self._fobj['sub']['img'].set_data(self._d['sub']['metrics'].val[:, :, k].T,)
            self._ax['sub'].set_xlim(self._d['sub']['metrics'].time_range.sec)
            self._fobj['sub']['cbar'].update_normal(self._fobj['sub']['img'])
            self._handle_interactive_graphics_events()

            # pipe updated state to std out
            print('!#TIME_SEL:=:DASH_CMD_UPDATE -tstart {} -tend {} -ft 0'.format(xmin_s, xmax_s), flush=True)


def grfx_main() -> bool:
    dash = TimeSelectionDashBoard(DEFAULTS['sup_title'], DEFAULTS['fig_size'])
    while True:
        time.sleep(DEFAULTS['grfx_main_loop_sleep_sec'])
        if not dash.is_open:
            return 0
        try:
            args = stdin_queue.get(block=False)
        except queue.Empty:
            dash._handle_interactive_graphics_events()
            continue

        if args.command in ['DASH_CMD_EXIT']:
            return 0
        try:
            dash.command(args)
        except Exception as ex:
            print(ex, file=sys.stderr, flush=True)
            return 1

        dash._handle_interactive_graphics_events()


def stdin_main():
    parser = argparse.ArgumentParser(prog='radiens-py dashboard', description='dashboard command line')
    parser.add_argument('command', choices=['DASH_CMD_OPEN', 'DASH_CMD_CLOSE',
                        'DASH_CMD_INIT', 'DASH_CMD_UPDATE', 'DASH_CMD_EXIT'], type=str, help='dashboard command')
    parser.add_argument('-uid', dest='dash_uid',  type=str, help='dashboard UID')
    parser.add_argument('-dsrcID', dest='dsrc_id', type=str, help='datasource ID')
    parser.add_argument('-mode', dest='metric_mode', type=int, help='signal metric mode (enum value)')
    parser.add_argument('-metric', dest='metric', type=int, help='signal metric (enum value)')
    parser.add_argument('-tstart', dest='time_start', type=float, help='time start (sec or fraction)')
    parser.add_argument('-tend', dest='time_end', type=float, help='time end (sec or fraction)')
    parser.add_argument('-ft', dest='is_frac_time', type=int, help='fractional time flag')
    stdin_queue.put(parser.parse_args(sys.argv[1:]))
    while True:
        args = parser.parse_args(input().split())  # blocks until <enter>
        stdin_queue.put(args)
        if args.command in ['DASH_CMD_EXIT']:
            return
        time.sleep(DEFAULTS['stdin_main_loop_sleep_sec'])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ['DASH_CMD_OPEN']:
        print('usage: dash_sig_metrics.py DASH_CMD_OPEN -uid <dash UID> -didx <dataset index>\n`dataset index` must be linked to DEFAULT radiens hub')
    stdin_thread = threading.Thread(target=stdin_main, daemon=True)
    stdin_thread.start()
    grfx_main()
    print('!#USER_SYS_EXIT', flush=True)


if __name__ == '__main__':
    sys.exit(main())

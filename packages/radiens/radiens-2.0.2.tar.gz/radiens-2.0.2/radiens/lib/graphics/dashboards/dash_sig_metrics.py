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

mpl.use('Qt5Agg')  # MacOSX, QtAgg, TkAgg, Qt5Agg  (TkAgg has internal bug)

# specific to this dashboard
DEFAULTS = {'sup_title': 'Signal Metrics',
            'fig_size': (8, 8),
            'grfx_main_loop_sleep_sec': 0.027,
            'stdin_main_loop_sleep_sec': 0.033}  # width, height


class SigMetricsDashBoard(DashBoard):
    def __init__(self, sup_title: str, fig_size: tuple) -> None:
        super().__init__(sup_title, fig_size)
        self._videre = VidereClient()
        self._dataset_meta = None
        self._ax = {}
        self._metrics = None
        self._sel_metric = None
        self._sel_TR = None
        self._cbar = None
        self._surf = None

    def open(self, args: argparse.Namespace) -> None:
        super().open(args)
        if args.dsrc_id is None:
            raise ValueError('missing dsrc_id arg')
        self._dsrc_id = args.dsrc_id
        if args.metric_mode is None or args.metric is None:
            raise ValueError('missing metric mode and/or name')

        # update data
        self._sel_metric = METRIC_ID(mode=METRIC_MODE(args.metric_mode), name=METRIC(args.metric))
        self._dataset_meta = self._videre.get_data_file_metadata(dataset_id=self._dsrc_id, fail_hard=True)

        self._sel_TR = self._dataset_meta.time_range
        self._metrics = self._videre.signal_metrics().get_metrics(self._sel_TR.sec,
                                                                  metrics=[self._sel_metric],
                                                                  tail=False, dataset_metadata=self._dataset_meta)

        # update graphics
        self._ax[0] = self._fig.add_subplot(111, projection='3d')  # subset time range
        self._title = self._ax[0].set_title('{}\n{}:{}'.format(str(Path(self._dataset_meta.path, self._dataset_meta.base_name)),
                                                               self._sel_metric.mode.name, self._sel_metric.name.name),
                                            fontdict=dl.TXT_STYLE['title'], loc='left')
        self._compose_data_axis()
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

        # update data
        is_changed = False
        if args.metric_mode is not None and args.metric is not None:
            self._sel_metric = METRIC_ID(mode=METRIC_MODE(args.metric_mode), name=METRIC(args.metric))
            is_changed = True
        if args.time_start is not None and args.time_end is not None:
            if args.is_frac_time:
                self._sel_TR = make_time_range(time_range=[self._dataset_meta.time_range.sec[0]+args.time_start*self._dataset_meta.time_range.dur_sec,
                                                           self._dataset_meta.time_range.sec[0]+args.time_end*self._dataset_meta.time_range.dur_sec],
                                               fs=self._dataset_meta.time_range.fs)
            else:
                self._sel_TR = make_time_range(time_range=[args.time_start, args.time_end],
                                               fs=self._dataset_meta.time_range.fs)
            is_changed = True

        if is_changed:
            self._metrics = self._videre.signal_metrics().get_metrics(self._sel_TR.sec,
                                                                      metrics=[self._sel_metric],
                                                                      tail=False, dataset_metadata=self._dataset_meta)

        # update graphics
        self._ax[0].clear()
        self._title = self._ax[0].set_title('{}\n{}:{}'.format(str(Path(self._dataset_meta.path, self._dataset_meta.base_name)),
                                                               self._sel_metric.mode.name, self._sel_metric.name.name),
                                            fontdict=dl.TXT_STYLE['title'], loc='left')
        self._compose_data_axis()
        plt.show(block=False)
        print('!#UPDATE_OK', flush=True)

    def _compose_data_axis(self):
        self._ax[0].set_ylabel('signal', fontdict=dl.TXT_STYLE['label_1'])
        self._ax[0].set_xlabel('time (seconds)', fontdict=dl.TXT_STYLE['label_1'])
        self._ax[0].zaxis.set_label('metric')
        self._ax[0].zaxis.set_major_formatter('{x:.1f}')
        k = 0

        pkt_taxis = np.arange(self._metrics.time_range.sec[0], self._metrics.time_range.sec[1],
                              self._metrics.settings['packet_dur_sec'])
        x0, y0 = np.meshgrid(pkt_taxis, np.linspace(
            0, self._metrics.settings['num_sigs'], self._metrics.settings['num_sigs']), indexing='ij')

        pkt_idx_min, pkt_idx_max = np.searchsorted(pkt_taxis, (self._metrics.time_range.sec[0], self._metrics.time_range.sec[1]))
        region = np.s_[pkt_idx_min:pkt_idx_max, 0:self._metrics.settings['num_sigs']]
        x, y, z = x0[region], y0[region], self._metrics.val[:, :, k][region]

        self._surf = self._ax[0].plot_surface(x, y, z, edgecolor='royalblue', lw=0.0,
                                              rcount=min(self._metrics.settings['num_packets'], dl.MAX_3D_SURFACE_RC_COUNT),
                                              ccount=min(self._metrics.settings['num_sigs'], dl.MAX_3D_SURFACE_RC_COUNT),
                                              cmap=dl.COLOR_MAP['default'],
                                              alpha=0.3, antialiased=False)
        if self._cbar is None:
            self._cbar = self._fig.colorbar(self._surf, shrink=0.75, aspect=15)  # shrink=0.5, aspect=5,
            self._cbar.minorticks_on()
            self._cbar.set_label('metric dim')
        else:
            self._cbar.update_normal(self._surf)

        xlim = (self._metrics.time_range.sec[0], self._metrics.time_range.sec[1]+0.10*self._metrics.time_range.dur_sec)
        self._ax[0].set_xlim(xlim)
        self._ax[0].contour(x, y, z, zdir='x', offset=xlim[1], stride=1, cmap=dl.COLOR_MAP['default'])

        ylim = (0-self._metrics.settings['num_sigs']*0.1, self._metrics.settings['num_sigs'])
        self._ax[0].set_ylim(ylim)
        self._ax[0].contour(x, y, z, zdir='y', offset=ylim[0], stride=self._metrics.settings['num_sigs']*0.1, cmap=dl.COLOR_MAP['default'])

        minz = np.min(z)
        maxz = np.max(z)
        zlim = (minz, maxz+(maxz-minz)*0.1)
        self._ax[0].set_zlim(zlim)
        self._ax[0].contour(x, y, z, zdir='z', offset=zlim[1], stride=(maxz-minz)/5.0, cmap=dl.COLOR_MAP['default'])

        for d in ['x', 'y', 'z']:
            self._ax[0].tick_params(axis=d, which='major', labelsize=dl.TXT_STYLE['label_1']['fontsize'])
            self._ax[0].tick_params(axis=d, which='minor', labelsize=dl.TXT_STYLE['label_2']['fontsize'])

        return


def grfx_main() -> bool:
    dash = SigMetricsDashBoard(DEFAULTS['sup_title'], DEFAULTS['fig_size'])
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
        time.sleep(0.027)


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

import os
import sys
import threading
import queue
import time
import numpy as np
from concurrent import futures
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
from matplotlib.gridspec import GridSpec

import grpc
from radiens import VidereClient
from radiens.exceptions.grpc_error import handle_grpc_error
import radiens.grpc_radiens.pyradiens_pb2_grpc as pyradiens_pb2_grpc
from radiens.api.api_utils.util import scan_for_open_port
from radiens.grpc_radiens import (
    common_pb2, pyradiens_pb2)
import radiens.lib.graphics.dashboards.lib as dl
from radiens.lib.sig_metrics import (SignalMetrics, METRIC_ID, METRIC_MODE, METRIC)

mpl.use('Qt5Agg')  # MacOSX, QtAgg, TkAgg, Qt5Agg

# specific to this fig
DEFAULTS = {'fig_size': (8, 8),
            'tr_metric': METRIC_ID(mode=METRIC_MODE.BASE, name=METRIC.MAX_MIN_DIFF_ABS),
            'focus_metric': METRIC_ID(mode=METRIC_MODE.BASE, name=METRIC.NOISE_UV)}


def compose_ax_focus_metrics(metrics, k, ax, fig):
    cmap = 'RdBu_r'
    _interpolation = 'antialiased'
    ax.set_title('Signal Metric {}:{}'.format(metrics.metric_ids[k].mode.name, metrics.metric_ids[k].name.name),
                 fontdict=dl.TXT_STYLE['title'], loc='left')
    ax.set_ylabel('native index', fontdict=dl.TXT_STYLE['label_1'])
    ax.set_xlabel('time (seconds)', fontdict=dl.TXT_STYLE['label_1'])
    ax.set_xlim(metrics.time_range.sec)
    ax.tick_params(axis='both', which='major', labelsize=dl.TXT_STYLE['label_1']['fontsize'])
    ax.tick_params(axis='both', which='minor', labelsize=dl.TXT_STYLE['label_2']['fontsize'])

    img = ax.imshow(metrics.val[:, :, k].T, cmap=cmap,
                    aspect='auto',
                    interpolation=_interpolation,
                    animated=True,
                    extent=(metrics.time_range.sec[0], metrics.time_range.sec[1],
                            0, metrics.settings['num_sigs']), origin='lower')
    cbar = fig.colorbar(img, ax=ax)
    cbar.set_label('metric', rotation=90, size='small')
    cbar.ax.tick_params(labelsize=dl.TXT_STYLE['label_2']['fontsize'])
    return img


def main():
    k_tr_sel_metric = 0
    k_data_metric = 1

    if len(sys.argv) != 4:
        dl.echo_err('sig_metrics', 'usage: dash_sig_metrics base_file_path dashboard_id style')
        sys.exit(1)

    try:
        plt.style.use(dl.get_style(sys.argv[3]))
    except ValueError as ex:
        dl.echo_err('sig_metrics', 'invalid style arg '+ex.args)
        sys.exit(1)

    # get signal metrics for time-range selection
    try:
        videre = VidereClient()
        dsource = videre.link_data_file(Path(sys.argv[1]).expanduser().absolute())
        metrics = videre.signal_metrics().get_metrics(dsource.time_range.sec, tail=False, dataset_metadata=dsource)
    except Exception as ex:
        dl.echo_err('sig_metrics', '{}'.format(ex.args))
        sys.exit(1)

    plt.ion()
    fig = plt.figure(layout="tight", figsize=DEFAULTS['fig_size'])
    gs = GridSpec(4, 2, figure=fig, width_ratios=[1, 5], height_ratios=[2, 20, 5, 1])
    ax = {'hdr': fig.add_subplot(gs[0, :]),
          'sel': fig.add_subplot(gs[1, 0]),
          'data': fig.add_subplot(gs[1, 1]),
          'tr_sel': fig.add_subplot(gs[2, :]),
          'ftr': fig.add_subplot(gs[3, :]),
          }

    dl.compose_ax_sel(ax['sel'], fig)
    dl.compose_ax_hdr(ax['hdr'], fig)
    dl.compose_ax_ftr(ax['ftr'], fig)
    dl.set_ax_hdr({'title': 'Signal Metrics', 'sub-title_1': 'blah', 'sub-title_2': 'yo'}, ax['hdr'], fig)
    dl.set_ax_ftr({'ftr_1': 'Dataset UID'}, ax['ftr'], fig)

    img = {'tr_sel': dl.compose_ax_tr_sel(metrics, k_tr_sel_metric, ax['tr_sel'], fig),
           'data': compose_ax_focus_metrics(metrics, k_data_metric, ax['data'], fig)}
    taxis = np.arange(metrics.time_range.sec[0], metrics.time_range.sec[1], 1/metrics.time_range.fs)
    pkt_taxis = np.arange(metrics.time_range.sec[0], metrics.time_range.sec[1], metrics.settings['packet_dur_sec'])

    # call back function(s). must be nested to access state: taxis, pkt_taxis, img, ax, k_data_metric, & fig
    def onselect(xmin_s, xmax_s):
        indmin, indmax = np.searchsorted(taxis, (xmin_s, xmax_s))
        indmax = min(len(taxis) - 1, indmax)

        pkt_indmin, pkt_indmax = np.searchsorted(pkt_taxis, (xmin_s, xmax_s))
        pkt_indmax = min(len(pkt_taxis) - 1, pkt_indmax)
        region_x = taxis[indmin:indmax]

        if len(region_x) >= 2:
            img['data'].set_data(metrics.val[pkt_indmin:pkt_indmax, :, k_data_metric])
            img['data'].autoscale()
            img['data'].set(extent=(region_x[0], region_x[-1],
                                    0, metrics.settings['num_sigs']))
            ax['data'].set_xlim(region_x[0], region_x[-1])
            fig.canvas.draw_idle()

    # define widgets
    # time-range selector
    span = SpanSelector(
        ax['tr_sel'],
        onselect,
        "horizontal",
        useblit=True,
        props=dict(alpha=0.5, facecolor="tab:blue"),
        interactive=True,
        drag_from_anywhere=True
    )
    plt.show(block=True)  # blocks until fig is closed


if __name__ == '__main__':
    sys.exit(main())

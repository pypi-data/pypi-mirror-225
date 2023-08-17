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
from radiens.lib.sig_metrics import (SignalMetrics, METRIC_ID, METRIC_MODE, METRIC)

mpl.use('TkAgg')  # MacOSX, QtAgg, TkAgg, Qt5Agg

# specific to this fig
DEFAULTS = {'fig_size': (8, 8),
            'tr_metric': METRIC_ID(mode=METRIC_MODE.BASE, name=METRIC.MAX_MIN_DIFF_ABS),
            'focus_metric': METRIC_ID(mode=METRIC_MODE.BASE, name=METRIC.NOISE_UV)}


def compose_ax_focus_metrics(metrics, k, ax, fig):
    ax.set_title('Signal Metric {}:{}'.format(metrics.metric_ids[k].mode.name, metrics.metric_ids[k].name.name),
                 fontdict=dl.TXT_STYLE['title'], loc='left')
    ax.set_ylabel('signal', fontdict=dl.TXT_STYLE['label_1'])
    ax.set_xlabel('time (seconds)', fontdict=dl.TXT_STYLE['label_1'])
    ax.set_zlabel('metric')
    ax.zaxis.set_major_formatter('{x:.1f}')

    pkt_taxis = np.arange(metrics.time_range.sec[0],
                          metrics.time_range.sec[1],
                          metrics.settings['packet_dur_sec'])
    x0, y0 = np.meshgrid(pkt_taxis, np.linspace(0, metrics.settings['num_sigs'], metrics.settings['num_sigs']), indexing='ij')

    pkt_idx_min, pkt_idx_max = np.searchsorted(pkt_taxis, (metrics.time_range.sec[0], metrics.time_range.sec[1]))
    region = np.s_[pkt_idx_min:pkt_idx_max, 0:metrics.settings['num_sigs']]
    x, y, z = x0[region], y0[region], metrics.val[:, :, k][region]

    surf = ax.plot_surface(x, y, z, edgecolor='royalblue', lw=0.0,
                           rcount=min(metrics.settings['num_packets'], dl.MAX_3D_SURFACE_RC_COUNT),
                           ccount=min(metrics.settings['num_sigs'], dl.MAX_3D_SURFACE_RC_COUNT),
                           cmap=dl.COLOR_MAP['default'],
                           alpha=0.3, antialiased=False)
    cbar = fig.colorbar(surf, shrink=0.5, aspect=5)

    xlim = (metrics.time_range.sec[0], metrics.time_range.sec[1]+0.10*metrics.time_range.dur_sec)
    ax.set_xlim(xlim)
    ax.contour(x, y, z, zdir='x', offset=xlim[1], stride=1, cmap=dl.COLOR_MAP['default'])

    ylim = (0-metrics.settings['num_sigs']*0.1, metrics.settings['num_sigs'])
    ax.set_ylim(ylim)
    ax.contour(x, y, z, zdir='y', offset=ylim[0], stride=metrics.settings['num_sigs']*0.1, cmap=dl.COLOR_MAP['default'])

    minz = np.min(z)
    maxz = np.max(z)
    zlim = (minz, maxz+(maxz-minz)*0.1)
    ax.set_zlim(zlim)
    ax.contour(x, y, z, zdir='z', offset=zlim[1], stride=(maxz-minz)/5.0, cmap=dl.COLOR_MAP['default'])

    for d in ['x', 'y', 'z']:
        ax.tick_params(axis=d, which='major', labelsize=dl.TXT_STYLE['label_1']['fontsize'])
        ax.tick_params(axis=d, which='minor', labelsize=dl.TXT_STYLE['label_2']['fontsize'])

    return {'cbar': cbar, 'surf': surf, 'X': x0, 'Y': y0}


def main():
    k_tr_sel_metric = 0
    k_data_metric = 1

    if len(sys.argv) != 4:
        dl.echo_err('sig_metrics', 'usage: % python -m ./dash_sig_metrics base_file_path dashboard_id style')
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
    fig = plt.figure(figsize=DEFAULTS['fig_size'], layout='constrained')  # layout="tight",
    plt.get_current_fig_manager().set_window_title('radiens:'+sys.argv[2])
    gs = GridSpec(2, 1, figure=fig, height_ratios=[9, 1])
    ax = {'data': fig.add_subplot(gs[0, 0], projection='3d'),
          'tr_sel': fig.add_subplot(gs[1, 0]),
          }

    # dl.compose_ax_hdr(ax['hdr'], fig)
    # dl.set_ax_hdr({'title': 'Signal Metrics', 'sub-title_1': 'blah', 'sub-title_2': 'yo'}, ax['hdr'], fig)

    img = {'tr_sel': dl.compose_ax_tr_sel(metrics, k_tr_sel_metric, ax['tr_sel'], fig),
           'data': compose_ax_focus_metrics(metrics, k_data_metric, ax['data'], fig)}
    taxis = np.arange(metrics.time_range.sec[0], metrics.time_range.sec[1], 1/metrics.time_range.fs)
    pkt_taxis = np.arange(metrics.time_range.sec[0], metrics.time_range.sec[1], metrics.settings['packet_dur_sec'])

    # sel_pos_h = 0.93
    # sel_pos_v = 0.95
    # sel_pos_dv = 0.03
    # sel_box_h = 0.025

    # def get_sig_sel(arg):
    #     print('get_sig_sel:  arg=', arg)

    # axbox = fig.add_axes([sel_pos_h, sel_pos_v, 0.03, sel_box_h])  # left, bottom, width, height (fractions of fig width & height)
    # axbox.text(-0.15, 0.5, 'signal idx', transform=axbox.transAxes, fontsize=8,
    #            verticalalignment='center', horizontalalignment='right')
    # text_box = TextBox(axbox, "", textalignment="left")
    # text_box.text_disp.set_fontsize(8)
    # text_box.on_submit(get_sig_sel)

    # def get_dataset_sel(arg):
    #     print('get_sig_sel:  arg=', arg)
    # # left, bottom, width, height (fractions of fig width & height)
    # axbox2 = fig.add_axes([sel_pos_h, sel_pos_v-sel_pos_dv, 0.03, sel_box_h])
    # # props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    # axbox2.text(-0.15, 0.5, 'dataset idx', transform=axbox2.transAxes, fontsize=8,
    #             verticalalignment='center', horizontalalignment='right')
    # text_box2 = TextBox(axbox2, "", textalignment="left")
    # text_box2.text_disp.set_fontsize(8)
    # text_box2.on_submit(get_dataset_sel)
    # # text_box.set_val('')  # Trigger `submit` with the initial string.
    # # call back function(s). must be nested to access state: taxis, pkt_taxis, img, ax, k_data_metric, & fig

    def onselect(xmin_s, xmax_s):
        indmin, indmax = np.searchsorted(taxis, (xmin_s, xmax_s))
        indmax = min(len(taxis) - 1, indmax)
        region_x = taxis[indmin:indmax]

        pkt_indmin, pkt_indmax = np.searchsorted(pkt_taxis, (xmin_s, xmax_s))
        pkt_indmax = min(len(pkt_taxis) - 1, pkt_indmax)

        if len(region_x) >= 2:
            ax['data'].clear()
            # img['data']['cbar'].remove()
            ax['data'].set_title('Signal Metric {}:{}'.format(metrics.metric_ids[k_data_metric].mode.name, metrics.metric_ids[k_data_metric].name.name),
                                 fontdict=dl.TXT_STYLE['title'], loc='left')
            ax['data'].set_ylabel('signal', fontdict=dl.TXT_STYLE['label_1'])
            ax['data'].set_xlabel('time (seconds)', fontdict=dl.TXT_STYLE['label_1'])
            ax['data'].set_zlabel('metric')
            for d in ['x', 'y', 'z']:
                ax['data'].tick_params(axis=d, which='major', labelsize=dl.TXT_STYLE['label_1']['fontsize'])
                ax['data'].tick_params(axis=d, which='minor', labelsize=dl.TXT_STYLE['label_2']['fontsize'])

            num_pkts = pkt_indmax-pkt_indmin
            pkt_taxis2 = np.arange(pkt_indmin*metrics.settings['packet_dur_sec'], pkt_indmax *
                                   metrics.settings['packet_dur_sec'], metrics.settings['packet_dur_sec'])+pkt_taxis[0]
            region2 = np.s_[pkt_indmin:pkt_indmax, 0:metrics.settings['num_sigs']]
            x, y, z = img['data']['X'][region2], img['data']['Y'][region2], metrics.val[:, :, k_data_metric][region2]

            surf = ax['data'].plot_surface(x, y, z, edgecolor='royalblue', lw=0.0,
                                           rcount=min(num_pkts, dl.MAX_3D_SURFACE_RC_COUNT),
                                           ccount=min(metrics.settings['num_sigs'], dl.MAX_3D_SURFACE_RC_COUNT),
                                           cmap=dl.COLOR_MAP['default'],
                                           alpha=0.3, antialiased=False)
            # img['data']['cbar'] = fig.colorbar(surf, ax=ax['data'], shrink=0.5, aspect=5)

            xlim = (pkt_taxis2[0], pkt_taxis2[-1]+0.10*(pkt_taxis2[-1]-pkt_taxis2[0]))
            ax['data'].set_xlim(xlim)
            ax['data'].contour(x, y, z, zdir='x', offset=xlim[1], stride=1, cmap=dl.COLOR_MAP['default'])

            ylim = (0-metrics.settings['num_sigs']*0.1, metrics.settings['num_sigs'])
            ax['data'].set_ylim(ylim)
            ax['data'].contour(x, y, z, zdir='y', offset=ylim[0], stride=metrics.settings['num_sigs']*0.1, cmap=dl.COLOR_MAP['default'])

            minz = np.min(z)
            maxz = np.max(z)
            zlim = (minz, maxz+(maxz-minz)*0.1)
            ax['data'].set_zlim(zlim)
            ax['data'].contour(x, y, z, zdir='z', offset=zlim[1], stride=(maxz-minz)/5.0, cmap=dl.COLOR_MAP['default'])

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

import os
import sys
import yaml
import shutil
import argparse
import numpy as np
import pandas as pd
from pathlib import Path

import matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.image as mpimg
import matplotlib.animation as animation
from matplotlib import cm
from radiens.utils.constants import (SIGNALS, TIME_RANGE, TRS_MODE, SignalType)
from radiens.lib.sig_metrics import (SignalMetrics)
from radiens.lib.signals_snapshot import (PSD)


# global for all figs
FIG_STYLES = {'dark': 'dark_background', '538': 'fivethirtyeight', 'fast': 'fast',
              'seaborn-v0_8': 'seaborn-v0_8'}
FONT_DICT_0 = {'fontsize': 12, 'weight': 'bold', 'horizontalalignment': 'center'}
FONT_DICT_1 = {'fontsize': 11, 'weight': 'bold', 'horizontalalignment': 'left'}
FONT_DICT_2 = {'fontsize': 10, 'weight': 'normal', 'horizontalalignment': 'left'}
FONT_DICT_3 = {'fontsize': 8, 'weight': 'normal', 'horizontalalignment': 'left'}
TXT_STYLE = {'title': FONT_DICT_1, 'sub_title_1': FONT_DICT_2,
             'sub_title_2': FONT_DICT_2, 'ftr': FONT_DICT_3,
             'label_1': FONT_DICT_3, 'label_2': FONT_DICT_3}
MAX_3D_SURFACE_RC_COUNT = 200
COLOR_MAP = {'default': cm.jet}  # cm.viridis  https://matplotlib.org/stable/gallery/color/colormap_reference.html


def dash_start_path() -> str:
    return str(Path(os.path.realpath(__file__)).resolve().parent)


def get_style(req):
    if req not in FIG_STYLES.keys():
        raise ValueError('invalid style arg {}'.format(req))
    return FIG_STYLES[req]


class DashBoard():
    def __init__(self, sup_title: str, fig_size: tuple) -> None:
        self._videre = None
        self._dsrc_id = None
        self._dash_uid = None
        self._fig_size = fig_size
        self._sup_title = sup_title
        self._fig = None
        self._is_open = True
        plt.ion()
        plt.style.use(FIG_STYLES['dark'])

    @property
    def is_open(self) -> bool:
        return self._is_open

    def open(self, args: argparse.Namespace) -> None:
        if args.dash_uid is None:
            raise ValueError('missing dashboard UID argument')
        self._dash_uid = args.dash_uid
        self._fig = plt.figure(figsize=self._fig_size, layout='constrained')  # layout="tight",
        self._fig.canvas.mpl_connect('close_event', self._on_fig_close)
        self._fig.suptitle(self._sup_title, fontsize=FONT_DICT_0['fontsize'],
                           fontweight=FONT_DICT_0['weight'])
        plt.get_current_fig_manager().set_window_title('radiens:'+self._dash_uid)

    def close(self) -> None:
        pass

    def init(self) -> None:
        pass

    def command(self, args: argparse.Namespace) -> None:
        pass

    def _handle_interactive_graphics_events(self):
        if isinstance(self._fig, plt.Figure) and plt.fignum_exists(self._fig.number):
            self._fig.canvas.flush_events()
            self._fig.canvas.draw_idle()

    def _on_fig_close(self, event):
        self._fig.canvas.flush_events()
        self._fig.canvas.draw_idle()
        print('!#USER_FIG_CLOSED')  # for detection in stdOut pipe
        self._is_open = False


def compose_ax_tr_sel(metrics: SignalMetrics, k, ax, fig):
    cmap = 'RdBu_r'
    _interpolation = 'antialiased'
    ax.set_title('Time range selector: signal metric {}:{}'.format(metrics.metric_ids[k].mode.name, metrics.metric_ids[k].name.name),
                 fontdict=TXT_STYLE['title'], loc='left')
    ax.set_ylabel('signal', fontdict=TXT_STYLE['label_1'])
    ax.set_xlabel('time (seconds)', fontdict=TXT_STYLE['label_1'], loc='left')
    ax.set_xlim(metrics.time_range.sec)
    ax.tick_params(axis='both', which='major', labelsize=TXT_STYLE['label_1']['fontsize'])
    ax.tick_params(axis='both', which='minor', labelsize=TXT_STYLE['label_2']['fontsize'])
    img = ax.imshow(metrics.val[:, :, k].T, cmap=cmap,
                    aspect='auto',
                    interpolation=_interpolation,
                    animated=True,
                    extent=(metrics.time_range.sec[0], metrics.time_range.sec[1],
                            0, metrics.settings['num_sigs']), origin='lower')
    cbar = fig.colorbar(img, ax=ax, location='bottom')
    cbar.set_label('metric', rotation=0, size='small')
    cbar.ax.tick_params(labelsize=TXT_STYLE['label_2']['fontsize'])
    return img


def compose_ax_sel(ax, fig):
    ax.axis('off')


def compose_ax_hdr(ax, fig):
    ax.axis('off')


def compose_ax_ftr(ax, fig):
    ax.axis('off')


def set_ax_hdr(arg, ax, fig):
    fig.text(0.05, 0.98, arg['title'], fontdict=TXT_STYLE['title'])
    fig.text(0.05, 0.94, arg['sub-title_1'], fontdict=TXT_STYLE['sub_title_1'])
    fig.text(0.05, 0.91, arg['sub-title_2'], fontdict=TXT_STYLE['sub_title_2'])


def set_ax_ftr(arg, ax, fig):
    fig.text(0.05, 0.02, arg['ftr_1'], fontdict=TXT_STYLE['ftr'])

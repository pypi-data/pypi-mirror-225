import logging
from bokeh.plotting import figure, show, output_file
from bokeh.transform import linear_cmap
from bokeh.util.hex import hexbin
from bokeh.io import curdoc
from bokeh.models import Title
from radiens.utils.constants import (SignalType)

_logger = logging.getLogger(__name__)


def plot_psd_heatmap(psd, fig_size=(1000, 500)):
    curdoc().theme = 'night_sky'  # 'dark_minimal'
    title = 'Power spectral density'
    title += '\ntime range : {} sec ({:.3f} sec duration),  sample freq={} Hz'.format(
        psd.time_range.sec, psd.time_range.dur_sec, psd.time_range.fs)
    sub_title_2 = 'freq bin width: {:.2f} Hz,  scaling: {}, FFT window: {}'.format(
        psd.attributes['freq_bin_width'],
        psd.attributes['scaling'].name, psd.attributes['wdw_type'].name)

    p = figure(title=title,
               width=fig_size[0], height=fig_size[1],
               title_location='above',
               x_range=(psd.freq_range[0], psd.freq_range[1]),
               y_range=(0, psd.channel_metadata.num_sigs(SignalType.AMP)),
               toolbar_location="right")
    p.grid.visible = False
    p.add_layout(Title(text=sub_title_2, align="left"), "below")
    p.xaxis.axis_label = 'Frequency [Hz]'
    p.yaxis.axis_label = 'Signal [native idx]'

    p.image(image=[psd.psd], x=psd.freq_range[0], y=0,
            dw=psd.freq_range[1],
            dh=psd.channel_metadata.num_sigs(SignalType.AMP),
            palette='Spectral11')

    show(p)
    return p

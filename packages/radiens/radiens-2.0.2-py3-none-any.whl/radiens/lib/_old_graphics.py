# radix.nb_graphics.py

import os
import sys
import yaml
import shutil
import numpy as np
import pandas as pd
from scipy.interpolate import griddata

import matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.image as mpimg
import matplotlib.animation as animation


class SignalsDashboard():
    '''
    This object uses matplotlib, which is preferred for movies
    '''

    def __init__(self, sp_map_obj, scope_sig_idx, t_hmap=None, zlim=[-8500, 8500], user_label='', fig_size=(8, 8)):
        '''
        '''

        self._zlim = zlim
        self._fig_size = fig_size
        self._dim_units = sp_map_obj.dim_units
        self.base_title = user_label
        self.title = self.base_title

        plt.ioff()
        self.fig = plt.figure(figsize=self._fig_size, dpi=100)
        self.axis = dict()
        self.data_update = dict()
        _axes_keys = ['meta', 'scope', 't_hmap', 'sp_hmap']
        gs = gridspec.GridSpec(4, 1, height_ratios=[1, 2, 4, 20])
        for m, g in enumerate(gs):
            self.axis[_axes_keys[m]] = self.fig.add_subplot(g)

        # self.fig.suptitle(self.title)
        self.fig.tight_layout()
        _cmap = plt.get_cmap("RdBu")

        # self.ax.cla()
        # === meta-data
        self.axis['meta'].axis('off')
        self.axis['meta'].set_xlim([0, 1])
        self.axis['meta'].set_ylim([0, 1])
        self.axis['meta'].text(0.005, 0.9, 'NNx Sapiens Analytics: Signals Dashboard',
                               fontsize=8, color="black", ha='left', va='top', weight='bold')
        self.axis['meta'].text(0.025, 0.20, 'Signals: ' + self.title, fontsize=8, color="blue", ha='left', va='top')
        self.axis['meta'].text(0.3, 0.20, 'Num signals: {}'.format(len(sp_map_obj.sgrp.sys_chan_idx)),
                               fontsize=8, color="black", ha='left', va='top')
        self.axis['meta'].text(0.3, -0.4, 'Time range : ({}, {}) sec'.format(0.0, 0.0), fontsize=8, color="black", ha='left', va='top')

        # === scope
        self.axis['scope'].set_title('Scope: signal index {}'.format(scope_sig_idx), color='black', fontsize=8, loc='left', weight='bold')
        self.axis['scope'].set_xlim([sp_map_obj.t_smpl[0], sp_map_obj.t_smpl[-1]])
        self.axis['scope'].set_ylim(self._zlim)
        self.axis['scope'].spines['right'].set_color('none')
        self.axis['scope'].spines['left'].set_color('none')
        self.axis['scope'].spines['top'].set_color('none')
        self.axis['scope'].spines['bottom'].set_position(('data', 0))
        self.axis['scope'].set_xticklabels([])
        for label in self.axis['scope'].get_yticklabels():
            label.set_fontsize(8)
        self.axis['scope'].set_xticklabels([])
        self.axis['scope'].grid(color='gray', alpha=0.5, linestyle='dashed', linewidth=0.5)
        self.axis['scope'].plot(sp_map_obj.t_smpl, sp_map_obj.df_sig[scope_sig_idx].values,
                                color='black', lw=1)

        _x = [sp_map_obj.t_smpl[0], sp_map_obj.t_smpl[0]]
        _y = [self._zlim[0], self._zlim[1]]
        self.data_update['scope_t_marker'], = self.axis['scope'].plot(_x, _y, color='blue', lw=1, alpha=0.5)

        # === time heatmap
        self.axis['t_hmap'].set_title('Temporal heatmap', color='black', fontsize=8, loc='left', weight='bold')
        self.axis['t_hmap'].set_xlim(sp_map_obj.t_smpl[0], sp_map_obj.t_smpl[-1])
        self.axis['t_hmap'].set_ylim([0, len(sp_map_obj.sgrp.sys_chan_idx)])
        self.axis['t_hmap'].spines['right'].set_color('none')
        self.axis['t_hmap'].spines['left'].set_color('none')
        self.axis['t_hmap'].spines['top'].set_color('none')
        # self.axis['t_hmap'].spines['bottom'].set_position(('data',0))
        # self.axis['t_hmap'].set_xticklabels([])
        self.axis['t_hmap'].grid(False)
        self.axis['t_hmap'].set_xlabel("time [sec]", fontsize=8)
        self.axis['t_hmap'].set_ylabel("sig index", fontsize=8)
        for label in self.axis['t_hmap'].get_xticklabels():
            label.set_fontsize(8)
        for label in self.axis['t_hmap'].get_yticklabels():
            label.set_fontsize(8)

        _extent = [sp_map_obj.t_smpl[0], sp_map_obj.t_smpl[-1], 0, len(sp_map_obj.sgrp.sys_chan_idx)]
        self.axis['t_hmap'].imshow(sp_map_obj.df_sig.values.T,
                                   extent=_extent, aspect='auto',
                                   origin='lower', interpolation='none', cmap=_cmap,
                                   vmin=self._zlim[0], vmax=self._zlim[1], animated=True)
        _x = [sp_map_obj.t_smpl[0], sp_map_obj.t_smpl[0]]
        _y = self.axis['t_hmap'].get_ylim()
        self.data_update['t_hmap_t_marker'], = self.axis['t_hmap'].plot(_x, _y, color='blue', lw=1, alpha=0.5)

        # === spatial heatmap
        self.axis['sp_hmap'].set_title('Spatio-temporal heatmap', color='black',
                                       fontsize=8, loc='left', weight='bold')
        for label in self.axis['sp_hmap'].get_xticklabels():
            label.set_fontsize(8)
        for label in self.axis['sp_hmap'].get_yticklabels():
            label.set_fontsize(8)
        self.axis['sp_hmap'].set_xlim(sp_map_obj.span['x'])
        self.axis['sp_hmap'].set_ylim(sp_map_obj.span['y'])
        self.data_update['sp_hmap'] = self.axis['sp_hmap'].imshow(sp_map_obj.map_values.T,
                                                                  extent=(sp_map_obj.span['x'][0], sp_map_obj.span['x'][1],
                                                                          sp_map_obj.span['y'][1], sp_map_obj.span['y'][0]),
                                                                  origin='lower', interpolation='bicubic', cmap=_cmap, aspect='auto',
                                                                  vmin=self._zlim[0], vmax=self._zlim[1], animated=True)

        cbar = self.fig.colorbar(self.data_update['sp_hmap'])
        cbar.set_label('adc', rotation=0, size='x-small')
        cbar.ax.tick_params(labelsize=6)

        self.axis['sp_hmap'].set_xlabel(self._dim_units, fontsize=8)
        self.axis['sp_hmap'].set_ylabel(self._dim_units, fontsize=8)

        self.data_update['sp_hmap_t_label'] = self.axis['sp_hmap'].text(0.007, 0.98, '{:.3f} sec'.format(0.0), fontsize=8, color="white", ha='left', va='top',
                                                                        backgroundcolor='k', transform=self.axis['sp_hmap'].transAxes)

        _xpos_sites = sp_map_obj.df_site_pos['site_ctr_x_tissue'].values
        _ypos_sites = sp_map_obj.df_site_pos['site_ctr_y_tissue'].values
        self.axis['sp_hmap'].scatter(_xpos_sites, _ypos_sites, s=25, color="black")

        self.fig.tight_layout()


#     def init_plot(self, spat_hmap_zgrid, t, plot_dim=(900, 500)):
#         '''
#         '''
#         if self.fig_spat_hmap is None:

#             self.fig_scope = figure(plot_width=600, plot_height=200,
#                      x_range=[0,len(xpts)], y_range=[-8000, 8000], x_axis_location="above")
#             self.fig_scope.line(x=xpts, y=ypts)
#             self.fig_scope.line(x=[600,600], y=[-5000, 5000], line_color='gray', line_width=5, line_alpha=0.5)


#             self.fig_spat_hmap = figure(plot_width=900, plot_height=500, title=self.title,
#                 x_axis_label='mediolateral, mm', y_axis_label='rostrocaudal, mm',
#                 x_range=sp_map_obj.span['x'], y_range=sp_map_obj.span['y'],
#                 tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])

#             self.t_label = Label(x=10, y=400, x_units='screen', y_units='screen',
#                  text='{:.3f} sec '.format(0.0), render_mode='css', text_color='white', text_font_size='8pt',
#                  border_line_color=None, border_line_alpha=1.0,
#                  background_fill_color='black', background_fill_alpha=1.0)

#             self.fig_spat_hmap.add_layout(self.t_label)
#             self.fig_spat_hmap.add_layout(self._color_bar, 'right')

#         self.spat_hmap = self.fig_spat_hmap.image(image=[spat_hmap_zgrid.T], x=sp_map_obj.span['x'][0], y=sp_map_obj.span['y'][0], dw=self._dw, dh=self._dh, palette="Viridis256")

#         grid = gridplot([[self.p_scope_chan], [self.fig_spat_hmap]])
#         self.grid = gridplot([[p_scope_chan], [p]])

# x_range = 0, mdata.shape[0]
# y_range = 0, mdata.shape[1]

# # scope channel
# p_scope_chan = figure(plot_width=600, plot_height=200,
#                      x_range=[0,len(xpts)], y_range=[-8000, 8000], x_axis_location="above")
# p_scope_chan.line(x=xpts, y=ypts)
# p_scope_chan.line(x=[600,600], y=[-5000, 5000], line_color='gray', line_width=5, line_alpha=0.5)

# # heatmap
# p = figure(plot_width=600, plot_height=100,
#            x_range=x_range, y_range=y_range,
#            tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
# p.xaxis.visible = False

# p.image(image=[mdata.T], x=0, y=0, dw=x_range[1], dh=y_range[1], palette="Spectral11")
# p.line(x=[600,600], y=[0, 64], line_color='gray', line_width=5, line_alpha=0.5)
# # color_bar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(),
# #                      label_standoff=12, border_line_color=None, location=(0,0))

# t_label = Label(x=10, y=430, x_units='screen', y_units='screen',
#                  text=' t = {:.3f} sec '.format(50.41), render_mode='css', text_color='white', text_font_size='8pt',
#                  border_line_color=None, border_line_alpha=1.0,
#                  background_fill_color='black', background_fill_alpha=1.0)


# #p.add_layout(color_bar, 'right')
# p.add_layout(t_label)
# # export_png(p, filename="tmp_plot.png")
# #show(column(p, p))

# # make a grid
# grid = gridplot([[p_scope_chan], [p]])
# show(grid)

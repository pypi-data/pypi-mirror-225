import time
import uuid
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, List, Union

import numpy as np
import pandas as pd
import radiens.api.api_allego as api_allego
import radiens.api.api_curate as api
import radiens.api.api_videre as api_videre
import radiens.utils.config as cfg
from radiens.api.api_utils.protocols import (ProtocolAPI, TransformEdge,
                                             TransformNode)
from radiens.api.api_utils.util import (BaseClient, to_file_ext,
                                        to_radiens_file_type)
from radiens.grpc_radiens import common_pb2, datasource_pb2
from radiens.lib.channel_metadata import ChannelMetadata
from radiens.lib.dataset_metadata import DatasetMetadata
from radiens.lib.sig_metrics import (METRIC, METRIC_ID, METRIC_MODE,
                                     SignalMetrics, SignalMetricsStatus)
from radiens.utils.constants import (CORE_SERVICE, DEFAULT_HUB, KPI_ADDR,
                                     NEURONS1_ADDR,
                                     PRIMARY_CACHE_STREAM_GROUP_ID, SignalType)

# the following lines are to avoid circular imports and are only used for typing hints
# (TYPE_CHECKING always evaluates to false at runtime)
if TYPE_CHECKING:
    from radiens.curate_client import CurateClient
    from radiens.videre_client import VidereClient


class MetricsClient():
    """
    Metrics client object for CurateClient, VidereClient
    """

    def __init__(self, parent_client):
        """
        """
        self.__parent: Union[CurateClient, VidereClient] = parent_client

    def clear(self, dataset_metadata=None, hub_name=DEFAULT_HUB) -> None:
        """
        Clears KPI data.  This is only available for :py:class:`.CurateClient` and :py:class:`.VidereClient`

        Parameters:
            dataset_metadata (~radiens.lib.dataset_metadata.DatasetMetadata): dataset metadata object
        Returns:
            None

        Example:
            >>> client.signal_metrics().clear()
            None

        See Also:
            :py:meth:`~radiens.VidereClient.get_data_file_metadata`
            :py:meth:`~radiens.VidereClient.link_data_file`

        """
        if self.__parent.type in ['allego']:
            raise RuntimeError('metrics clear is not available for allego')
        else:
            if not isinstance(dataset_metadata, DatasetMetadata):
                raise ValueError(
                    'videre: dataset_metadata must be a DatasetMetadata')
            api_videre.set_kpi_clear(self.__parent._server_address(
                hub_name, CORE_SERVICE), dataset_metadata.attributes['dsource_id'])

    def calculate(self,
                  dataset_metadata=None,
                  hub_name=DEFAULT_HUB) -> None:
        """
        Calculates KPI data.  This is only available for CurateClient and VidereClient

        Parameters:
            dataset_metadata (~radiens.lib.dataset_metadata.DatasetMetadata): dataset metadata object         

        Returns:
            None

        Example:
            >>> client.signal_metrics().calculate()
            None

        See Also:
            :py:meth:`~radiens.VidereClient.get_data_file_metadata`
            :py:meth:`~radiens.VidereClient.link_data_file`

        """
        if self.__parent.type in ['allego']:
            raise RuntimeError('metrics calculate is not available for allego')
        else:
            if not isinstance(dataset_metadata, DatasetMetadata):
                raise ValueError(
                    'videre: dataset_metadata must be a DatasetMetadata')
            api_videre.set_kpi_calculate(self.__parent._server_address(
                hub_name, CORE_SERVICE), dataset_metadata.attributes['dsource_id'])

    def set_event_threshold_level(self, neg_thr=None, pos_thr=None, scale='uV', ntv_idxs=None, weak_thr=False, dataset_metadata=None, hub_name=DEFAULT_HUB, channel_metadata=None) -> str:
        """
        Sets spike detection threshold.  This function does not effect the threshold state.

        Parameters:
            neg_thr (str): ``on`` | ``off``
            pos_thr (str): ``on`` | ``off``
            scale (str):  ``uV`` | ``sd``
            ntv_idxs (list): channel native indices (default None=all channels)
            weak_thr (bool): use True to set the weak threshold (default=False)
            dataset_metadata (~radiens.lib.dataset_metadata.DatasetMetadata): dataset metadata object
            channel_metadata (~radiens.lib.channel_metadata.ChannelMetadata): Allego connected channels

        Returns:
            msg (str): summary description of threshold levels

        Example:
            >>> client.signal_metrics().set_threshold_level(neg_thr=85)
            '[32 channels] detect: neg thr=85.00 uV, pos thr=n/a uV'

        See Also:
             :py:meth:`set_threshold`
             :py:meth:`get_channel_metadata`

        """
        if self.__parent.type not in ['allego'] and not isinstance(dataset_metadata, DatasetMetadata):
            raise ValueError('videre: dataset_metadata must be provided')
        if neg_thr in [None] and pos_thr in [None]:
            return 'no new threshold levels were requested so none were changed'
        if channel_metadata in [None]:
            channel_metadata = self.__parent.get_channel_metadata() if self.__parent.type in [
                'allego'] else dataset_metadata.channel_metadata
        if not isinstance(channel_metadata, ChannelMetadata):
            raise ValueError(
                'channel metadata must be of type ChannelMetadata')
        if isinstance(ntv_idxs, (list, np.ndarray)):
            pass
        elif isinstance(ntv_idxs, (int, float)):
            ntv_idxs = [ntv_idxs]
        elif ntv_idxs in [None]:
            ntv_idxs = channel_metadata.index(SignalType.AMP).ntv
        else:
            raise ValueError('ntv_idxs must be scalar or list or None')
        reg_float = [0, 0]
        reg_bool = [False, False]
        if neg_thr not in [None]:
            reg_float[0] = neg_thr
            reg_bool[0] = True
        if pos_thr not in [None]:
            reg_float[1] = pos_thr
            reg_bool[1] = True
        if scale in ['sd'] and weak_thr in [False]:
            arg = common_pb2.SORTER_THR_LEVEL_SD
        elif scale in ['uV'] and weak_thr in [False]:
            arg = common_pb2.SORTER_THR_LEVEL
        elif scale in ['sd'] and weak_thr in [True]:
            arg = common_pb2.SORTER_WEAK_THR_LEVEL_SD
        elif scale in ['uV'] and weak_thr in [True]:
            arg = common_pb2.SORTER_WEAK_THR_LEVEL
        else:
            raise ValueError(
                'scale must be `uV` | `sd` and/or weak_thr must be True | False')
        req = [common_pb2.SpikeSorterSetParamRequest(spikeSorterID='not_used',
                                                     cmd=arg,
                                                     regFloat64=reg_float,
                                                     regBool=reg_bool,
                                                     ntvChanIdx=ntv_idxs)]

        if self.__parent.type in ['allego']:
            req.spikeSorterID = PRIMARY_CACHE_STREAM_GROUP_ID
            api_allego.sorter_set_params(
                NEURONS1_ADDR, common_pb2.SpikeSorterSetParamsRequest(params=req))
        else:
            if not isinstance(dataset_metadata, DatasetMetadata):
                raise ValueError(
                    'videre: dataset_metadata must be a DatasetMetadata')
            req[0].spikeSorterID = dataset_metadata.attributes['dsource_id']
            api_videre.set_kpi_params(self.__parent._server_address(hub_name, CORE_SERVICE),
                                      common_pb2.SpikeSorterSetParamsRequest(params=req))

        return '[{} channels] {}: neg thr={} {}, pos_thr={} {}' .format(len(ntv_idxs),
                                                                        'detect' if arg in [common_pb2.SORTER_THR_LEVEL,
                                                                                            common_pb2.SORTER_THR_LEVEL_SD] else 'weak',
                                                                        '{:.2f}'.format(reg_float[0]) if reg_bool[0] in [
            True] else 'n/a',
            scale,
            '{:.2f}'.format(reg_float[1]) if reg_bool[1] in [
            True] else 'n/a',
            scale)

    def set_event_threshold(self, neg_thr=None, pos_thr=None, ntv_idxs=None, weak_thr=False, dataset_metadata=None, hub_name=DEFAULT_HUB, channel_metadata=None) -> str:
        """
        Sets signal metrics event detect threshold 'on' or 'off'

        Parameters:
            neg_thr (str): ``on`` | ``off``
            pos_thr (str): ``on`` | ``off``
            ntv_idxs (list): channel native indices (default None=all channels)
            weak_thr (bool): use True to set the weak threshold (default=False)
            dataset_metadata (~radiens.lib.dataset_metadata.DatasetMetadata): dataset metadata object
            channel_metadata (~radiens.lib.channel_metadata.ChannelMetadata): Allego connected channels

        Returns:
            msg (str): summary description of threshold levels

        Example:
            >>> client.signal_metrics().set_event_threshold(neg_thr='on')
            '[32 channels] detect: neg thr='on', pos thr=n/a'

        See Also:
             :py:meth:`set_threshold_level`
             :py:meth:`get_channel_metadata`

        """
        if self.__parent.type not in ['allego'] and not isinstance(dataset_metadata, DatasetMetadata):
            raise ValueError('videre: dataset_metadata must be provided')
        if neg_thr in [None] and pos_thr in [None]:
            return 'no new threshold states were requested so none were changed'
        if channel_metadata in [None]:
            channel_metadata = self.__parent.get_channel_metadata() if self.__parent.type in [
                'allego'] else dataset_metadata.channel_metadata
        if not isinstance(channel_metadata, ChannelMetadata):
            raise ValueError(
                'channel metadata must be of type ChannelMetadata')
        if isinstance(ntv_idxs, (list, np.ndarray)):
            pass
        elif isinstance(ntv_idxs, (int, float)):
            ntv_idxs = [ntv_idxs]
        elif ntv_idxs in [None]:
            ntv_idxs = channel_metadata.index(SignalType.AMP).ntv
        else:
            raise ValueError('ntv_idxs must be scalar or list or None')
        reg_float = [0, 0]
        reg_bool = [False, False]
        if neg_thr not in [None]:
            if neg_thr not in ['on', 'off']:
                raise ValueError('neg_thr must be ``on`` or ``off``')
            reg_float[0] = 1.0 if neg_thr in ['on'] else 0.0
            reg_bool[0] = True
        if pos_thr not in [None]:
            if pos_thr not in ['on', 'off']:
                raise ValueError('pos_thr must be ``on`` or ``off``')
            reg_float[1] = 1.0 if pos_thr in ['on'] else 0.0
            reg_bool[1] = True
        if weak_thr in [False]:
            arg = common_pb2.SORTER_THR_ACTIVATE
        elif weak_thr in [True]:
            arg = common_pb2.SORTER_WEAK_THR_ACTIVATE
        else:
            raise ValueError('weak_thr must be True | False')
        req = [common_pb2.SpikeSorterSetParamRequest(cmd=arg,
                                                     regFloat64=reg_float,
                                                     regBool=reg_bool,
                                                     ntvChanIdx=ntv_idxs)]
        if self.__parent.type in ['allego']:
            req.spikeSorterID = PRIMARY_CACHE_STREAM_GROUP_ID
            api_allego.set_kpi_params(
                NEURONS1_ADDR, common_pb2.SpikeSorterSetParamsRequest(params=req))
        else:
            req[0].spikeSorterID = dataset_metadata.attributes['dsource_id']
            api_videre.set_kpi_params(self.__parent._server_address(hub_name, CORE_SERVICE),
                                      common_pb2.SpikeSorterSetParamsRequest(params=req))
        return '[{} channels] {}: neg thr={}, pos_thr={}' .format(len(ntv_idxs),
                                                                  'detect' if arg in [common_pb2.SORTER_THR_LEVEL,
                                                                                      common_pb2.SORTER_THR_LEVEL_SD] else 'weak',
                                                                  '{}'.format(neg_thr) if reg_bool[0] in [
            True] else 'n/a',
            '{}'.format(pos_thr) if reg_bool[1] in [True] else 'n/a')

    def set_event_window(self, pre_ms: float, post_ms: float, dataset_metadata=None, hub_name=DEFAULT_HUB, channel_metadata=None) -> str:
        """
        Sets signal metrics event event window

        Parameters:
            pre_ms (float): ms before event
            post_ms (float): ms after event
            dataset_metadata (~radiens.lib.dataset_metadata.DatasetMetadata): dataset metadata object
            channel_metadata (~radiens.lib.channel_metadata.ChannelMetadata): Allego connected channels

        Returns:
            msg (str): summary description of event window

        Example:
            >>> client.signal_metrics().set_event_window(2, 2)
            '[32 channels] event window: pre-threshold=2 ms, post-threshold=2 ms

        See Also:
             :py:meth:`set_threshold_level`
             :py:meth:`get_channel_metadata`

        """
        if self.__parent.type not in ['allego'] and not isinstance(dataset_metadata, DatasetMetadata):
            raise ValueError('videre: dataset_metadata must be provided')
        if not isinstance(pre_ms, (int, float)) or not isinstance(post_ms, (int, float)):
            return 'pre_ms and post_ms are required scalars'
        if channel_metadata in [None]:
            channel_metadata = self.__parent.get_channel_metadata() if self.__parent.type in [
                'allego'] else dataset_metadata.channel_metadata
        if not isinstance(channel_metadata, ChannelMetadata):
            raise ValueError(
                'channel metadata must be of type ChannelMetadata')
        reg_float = [pre_ms, post_ms]
        reg_bool = [True, True]
        req = [common_pb2.SpikeSorterSetParamRequest(cmd=common_pb2.SORTER_THR_WDW,
                                                     regFloat64=reg_float,
                                                     regBool=reg_bool,
                                                     ntvChanIdx=channel_metadata.index(SignalType.AMP).ntv)]
        if self.__parent.type in ['allego']:
            req.spikeSorterID = PRIMARY_CACHE_STREAM_GROUP_ID
            api_allego.set_kpi_params(
                NEURONS1_ADDR, common_pb2.SpikeSorterSetParamsRequest(params=req))
        else:
            req[0].spikeSorterID = dataset_metadata.attributes['dsource_id']
            api_videre.set_kpi_params(self.__parent._server_address(hub_name, CORE_SERVICE),
                                      common_pb2.SpikeSorterSetParamsRequest(params=req))
        return '[{} channels] event window: pre-threshold={} ms, post-threshold={} ms' .format(len(channel_metadata.index(SignalType.AMP).ntv),
                                                                                               '{}'.format(
                                                                                                   pre_ms),
                                                                                               '{}'.format(post_ms))

    def set_event_shadow(self, shadow_ms: float, dataset_metadata=None, channel_metadata=None, hub_name=DEFAULT_HUB) -> str:
        """
        Sets signal metrics event shadow

        Parameters:
            shadow_ms (float): duration of shadow in milliseconds
            dataset_metadata (~radiens.lib.dataset_metadata.DatasetMetadata): dataset metadata object
            channel_metadata (~radiens.lib.channel_metadata.ChannelMetadata): Allego connected channels

        Returns:
            msg (str): summary description of threshold levels

        Example:
            >>> client.signal_metrics().set_event_shadow(1)
            '[32 channels] event shadow 1 ms'

        See Also:
             :py:meth:`set_threshold_level`
             :py:meth:`get_channel_metadata`

        """
        if self.__parent.type not in ['allego'] and not isinstance(dataset_metadata, DatasetMetadata):
            raise ValueError('videre: dataset_metadata must be provided')
        if not isinstance(shadow_ms, (int, float)):
            return 'shadow_ms is a required scalar'
        if channel_metadata in [None]:
            channel_metadata = self.__parent.get_channel_metadata() if self.__parent.type in [
                'allego'] else dataset_metadata.channel_metadata
        if not isinstance(channel_metadata, ChannelMetadata):
            raise ValueError(
                'channel metadata must be of type ChannelMetadata')
        reg_float = [shadow_ms, np.NaN]
        reg_bool = [True, False]
        req = [common_pb2.SpikeSorterSetParamRequest(cmd=common_pb2.SORTER_SHADOW,
                                                     regFloat64=reg_float,
                                                     regBool=reg_bool,
                                                     ntvChanIdx=channel_metadata.index(SignalType.AMP).ntv)]
        if self.__parent.type in ['allego']:
            req.spikeSorterID = PRIMARY_CACHE_STREAM_GROUP_ID
            api_allego.set_kpi_params(
                NEURONS1_ADDR, common_pb2.SpikeSorterSetParamsRequest(params=req))
        else:
            req[0].spikeSorterID = dataset_metadata.attributes['dsource_id']
            api_videre.set_kpi_params(self.__parent._server_address(hub_name, CORE_SERVICE),
                                      common_pb2.SpikeSorterSetParamsRequest(params=req))
        return '[{} channels] event shadow {} ms,' .format(len(channel_metadata.index(SignalType.AMP).ntv),
                                                           '{}'.format(shadow_ms))

    def set_packet_duration(self, packet_dur_sec: float, dataset_metadata=None, hub_name=DEFAULT_HUB) -> None:
        """
        Sets signal metrics packet duration in seconds

        Parameters:
            packet_dur_sec (float): duration in seconds of signals used to calculate signal metrics packet
            dataset_metadata (~radiens.lib.dataset_metadata.DatasetMetadata): dataset metadata object

        Returns:
            msg (str): summary description of threshold levels

        Example:
            >>> client.signal_metrics().set_packet_duration(neg_thr='on')
            None

        See Also:
             :py:meth:`set_threshold_level`
             :py:meth:`get_channel_metadata`

        """
        if self.__parent.type not in ['allego'] and not isinstance(dataset_metadata, DatasetMetadata):
            raise ValueError('videre: dataset_metadata must be provided')
        if not isinstance(packet_dur_sec, (int, float)):
            return 'packet_dur_sec is a required scalar'
        req = common_pb2.SetKpiParamRequest(param=packet_dur_sec)
        if self.__parent.type in ['allego']:
            req.streamGroupId = PRIMARY_CACHE_STREAM_GROUP_ID
            api_allego.set_kpi_packet_dur(NEURONS1_ADDR, req)
        else:
            req.streamGroupId = dataset_metadata.attributes['dsource_id']
            api_videre.set_kpi_packet_dur(
                self.__parent._server_address(hub_name, CORE_SERVICE), req)

    def get_params(self, dataset_metadata=None, hub_name=DEFAULT_HUB) -> pd.DataFrame:
        """
        Returns KPI parameters

        Parameters:
            dataset_metadata (~radiens.lib.dataset_metadata.DatasetMetadata): dataset metadata object

        Returns:
            pandas.DataFrame
        """
        if self.__parent.type in ['allego']:
            api_allego.get_kpi_params(NEURONS1_ADDR)
        else:
            if not isinstance(dataset_metadata, DatasetMetadata):
                raise ValueError(
                    'videre: dataset_metadata must be a DatasetMetadata')
            return api_videre.get_kpi_params(self.__parent._server_address(hub_name, CORE_SERVICE), dataset_metadata.attributes['dsource_id'])

    def get_metrics_status(self, dataset_metadata=None, hub_name=DEFAULT_HUB) -> SignalMetricsStatus:
        """
        Returns the status of the stream metrics service

        Parameters:
            dataset_metadata (~radiens.lib.dataset_metadata.DatasetMetadata): dataset metadata object

        Returns:
            status (dict): dict of status parameters, with keys='time_range','packet_dur_sec', 'beta', 'is_tracking_cache', 'wall_time_start', 'persistence_sec'
        """
        if self.__parent.type in ['allego']:
            return api_allego.get_kpi_status(KPI_ADDR)
        else:
            if not isinstance(dataset_metadata, DatasetMetadata):
                raise ValueError(
                    'videre: dataset_metadata must be a DatasetMetadata')
            return api_videre.get_kpi_status(self.__parent._server_address(hub_name, CORE_SERVICE), dataset_metadata.attributes['dsource_id'])

    def get_metrics(self,
                    time_range: Union[int, float, list, np.ndarray] = None,
                    metrics: list[METRIC_ID] = None,
                    ntv_idxs=None,
                    tail=True,
                    plot: bool = True,
                    file: str = None,
                    data: bool = True,
                    dataset_metadata=None,
                    hub_name=DEFAULT_HUB,
                    channel_metadata=None) -> SignalMetrics:
        """
        Gets the requested signal metrics from a data source.

        Parameters:
            time_range (int, float, list, ndarray): if parent client is :py:class:`.AllegoClient`, then this parameter can be `float` or `int`; otherwise, it must be `list` or `~numpy.ndarray`
            metrics (list): a list of :py:class:`~radiens.lib.sig_metrics.METRIC_ID`. It specified a default list is used.
            dataset_metadata (~radiens.lib.dataset_metadata.DatasetMetadata): dataset metadata object
            channel_metadata (~radiens.lib.channel_metadata.ChannelMetadata): Allego connected channels


        Returns:
            SignalMetrics (~radiens.lib.sig_metrics.SignalMetrics): Requested metrics

        """
        if self.__parent.type in ['allego']:
            if not isinstance(time_range, (float, int)) and time_range not in [None]:
                raise ValueError(
                    'allego: time_range must be None or scalar lag time (sec) from head of primary cache')
            if not isinstance(channel_metadata, (ChannelMetadata)) and channel_metadata not in [None]:
                raise ValueError(
                    'allego: channel metadata must be None or a ChannelMetadata')
            _tr = [5, np.NAN] if time_range in [None] else [time_range, np.NAN]
            channel_metadata = self.__parent.get_channel_metadata() if channel_metadata in [
                None] else channel_metadata
        else:
            if not isinstance(time_range, (list, np.ndarray)) and time_range is not None:
                raise ValueError(
                    'videre: time_range must be None or [start, end] (sec) with respect to datasource time range')
            if not isinstance(dataset_metadata, DatasetMetadata):
                raise ValueError(
                    'videre: dataset metadata must be a DatasetMetadata')
            channel_metadata = dataset_metadata.channel_metadata
            _tr = dataset_metadata.time_range.sec if time_range is None else np.array(
                time_range, dtype=np.float64)
        ntv_idxs = channel_metadata.index(SignalType.AMP).ntv
        status = self.get_metrics_status(dataset_metadata=dataset_metadata)

        if metrics in [None]:
            metrics = [METRIC_ID(mode=METRIC_MODE.BASE, name=METRIC.RMS),
                       METRIC_ID(mode=METRIC_MODE.BASE, name=METRIC.NOISE_UV),
                       METRIC_ID(mode=METRIC_MODE.BASE,
                                 name=METRIC.MAX_MIN_DIFF_ABS),
                       METRIC_ID(mode=METRIC_MODE.BASE, name=METRIC.SNR),
                       METRIC_ID(mode=METRIC_MODE.BASE,
                                 name=METRIC.EVENT_RATE),
                       METRIC_ID(mode=METRIC_MODE.BASE,
                                 name=METRIC.EVENT_MEAN_MAX_MIN_DIFF_ABS),
                       ]
        _metrics = []
        for m in metrics:
            _metrics.append(common_pb2.KpiMetricID(
                mode=m.mode.value, name=m.name.value))
        arg = common_pb2.BundleReq(ntvIdxs=ntv_idxs, tR=common_pb2.TimeRange(
            timeRangeSec=list(_tr), fs=status.time_range.fs), metrics=_metrics, isTail=tail)
        req = common_pb2.KpiMetricsReq(stype=common_pb2.PRI,
                                       arg=arg,
                                       isPlot=plot,
                                       path=file,
                                       isReturnData=data)
        if self.__parent.type in ['allego']:
            req.streamGroupId = PRIMARY_CACHE_STREAM_GROUP_ID
            return api_allego.get_kpi_metrics(KPI_ADDR, req)
        else:
            if not isinstance(dataset_metadata, DatasetMetadata):
                raise ValueError(
                    'videre: dataset_metadata must be a DatasetMetadata')
            req.streamGroupId = dataset_metadata.attributes['dsource_id']
            return api_videre.get_kpi_metrics(self.__parent._server_address(hub_name, CORE_SERVICE), dataset_metadata.attributes['dsource_id'], req)

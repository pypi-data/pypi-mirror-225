import os
import sys
from pathlib import Path

import grpc
import numpy as np
import pandas as pd
from radiens.api.api_utils.util import server_start_script
from radiens.exceptions.grpc_error import handle_grpc_error
from radiens.grpc_radiens import (biointerface_pb2, biointerface_pb2_grpc,
                                  common_pb2, datasource_pb2,
                                  radiensserver_pb2_grpc, spikesorter_pb2)
from radiens.grpc_radiens.common_pb2 import RadixFileTypes
from radiens.lib.dataset_metadata import DatasetMetadata
from radiens.lib.selector_tables import SelectorTables
from radiens.lib.sig_metrics import SignalMetrics, SignalMetricsStatus
from radiens.lib.signals_snapshot import PSD, Signals
from radiens.utils.config import new_server_channel

# from radiens.lib.graphics.dashboards.lib import dash_start_path

CLIENT_NAME = 'Videre'


def set_datasource(addr, req: datasource_pb2.DataSourceSetSaveRequest):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            res = stub.SetDataSourceFromFile(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        return DatasetMetadata(res)


def unlink_datasource(addr, datasetIDs: list):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            res = stub.ClearDataSource(
                datasource_pb2.DataSourceRequest(dsourceID=datasetIDs))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        return list(res.sortedID)


def list_datasource_ids(addr):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            res = stub.ListDataSourceIDs(datasource_pb2.DataSourceRequest())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        return list(res.sortedID)


def convert_kilosort_output(addr, req: common_pb2.WrangleRequest):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensSpikeSorter1Stub(chan)
        try:
            stub.SpikeSorterWrangleData(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        return


def get_selector_tables(addr, req):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.GetSelectorTables(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        return SelectorTables(resp)


def get_signals(addr, req):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            raw = stub.GetHDSnapshotPy(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        return Signals(raw)


def get_psd(addr, req):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.GetPSD(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        if req.isReturnPSD:
            return PSD(resp)


def get_spike_waveforms(addr, dsource_id: str, time_range: list, ntv_chan_idxs: list):
    if len(time_range) != 2:
        raise ValueError("time range must be a list of length 2")
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            req = biointerface_pb2.SpikesGetSpikesRequest(
                ntvChanIdx=ntv_chan_idxs, spikeLabels=[])
            req.dsourceID = dsource_id
            req.mode = biointerface_pb2.NeuronsSignalMode.SpikeWaveforms
            req.timeStart = time_range[0]
            req.timeStop = time_range[1]
            req.maxSpikesPerChannel = 1000  # arbitrary for now (TODO)

            raw = stub.SpikesGetSpikesDense(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)

        _waveforms = np.reshape(np.frombuffer(
            raw.data, dtype=np.float32), (raw.totalNSpikes, raw.waveformNPoints))

        return _waveforms


def get_spikes_timestamps(addr, dsource_id: str, time_range: list, ntv_chan_idxs: list):
    if len(time_range) != 2:
        raise ValueError("time range must be a list of length 2")
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            req = spikesorter_pb2.SpikeSorterGetRasterDataRequest(
                ntvChanIdx=ntv_chan_idxs,
                timeRange=time_range,
                spikeSorterID=dsource_id,
                timeWindow=1,  # make timeWindow == plotWidthPoints for no downsampling
                plotWidthPoints=1,
                componentID="",
            )

            raw = stub.SpikesGetRasterData(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)

        resp = []
        # for idx in range(len(raw.spikeTimestampsByChannel)):
        for msg in raw.spikeTimestampsByChannel:
            # msg = raw.spikeTimestampsByChannel[idx]
            resp.append({'ntv_idx': msg.ntvChanIdx,
                         'timestamps': msg.spikeTimestamps,
                         'labels': msg.labels})
        return resp


# ==========================
# ====== KPIs ==============
# ==========================

def set_kpi_calculate(addr, dsource_id) -> None:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            stub.KpiCalculate(
                common_pb2.KpiStandardRequest(dsourceID=[dsource_id]))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)


def set_kpi_clear(addr, dsource_id) -> None:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            stub.KpiClear(common_pb2.KpiStandardRequest(
                dsourceID=[dsource_id]))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)


def set_kpi_params(addr, req):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            stub.SetKpiParam(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)


def set_kpi_packet_dur(addr, req):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            stub.SetKpiPacketDur(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)


def get_kpi_metrics(addr, dsource_id, req) -> SignalMetrics:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.KpiGetMetrics(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        return SignalMetrics(dsource_id, resp)


def get_kpi_status(addr, dsource_id) -> SignalMetricsStatus:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.GetKpiStatus(
                common_pb2.GetKpiStatusRequest(streamGroupId=dsource_id))
            resp2 = stub.GetDataSourceKpiFileStatus2(
                datasource_pb2.DataSourceRequest(dsourceID=[dsource_id]))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        return SignalMetricsStatus(resp, resp2)


def get_kpi_params(addr, dsource_id) -> pd.DataFrame:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        try:
            resp = stub.GetKpiParam(
                datasource_pb2.DataSourceRequest(dsourceID=[dsource_id]))
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        p = {'ntv_idx': [], 'chan_enabled': [], 'thr_activated': [], 'thr': [], 'thr_sd': [], 'thr_wdw': [],
             'shadow': [], 'weak_thr_activated': [], 'weak_thr': [], 'weak_thr_sd': [], 'thr_wdw_pts': [], 'shadow_pts': []}
        for v in resp.rec:
            p['ntv_idx'].append(v.ntvChanIdx)
            p['chan_enabled'].append(v.isEnabled)
            p['thr_activated'].append(v.isSetThr)
            p['thr'].append(np.array(v.thr))
            p['thr_sd'].append(np.array(v.thrSd))
            p['thr_wdw'].append(np.around(np.array(v.thrWdw) * 1000.0, 5))
            p['shadow'].append(np.around(np.array(v.shadow) * 1000.0, 5))
            p['weak_thr_activated'].append(np.array(v.isSetWeakThr))
            p['weak_thr'].append(np.array(v.weakThr))
            p['weak_thr_sd'].append(np.array(v.weakThrSd))
            p['thr_wdw_pts'].append(v.thrWdwPts)
            p['shadow_pts'].append(v.shadowPts)
        return pd.DataFrame(p)


def command_dashboard(addr, req) -> str:
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.DashboardsStub(chan)
        try:
            stub.CommandDashboard(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)

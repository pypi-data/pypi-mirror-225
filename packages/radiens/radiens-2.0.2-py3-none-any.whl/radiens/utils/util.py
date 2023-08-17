import numpy as np
import datetime
from pathlib import Path
from typing import Union
from radiens.grpc_radiens import (allegoserver_pb2, allegoserver_pb2_grpc,
                                  common_pb2, spikesorter_pb2, biointerface_pb2)
from radiens.utils.constants import (TIME_SPEC, TIME_RANGE, NEIGHBORS_DESC, NEURON_DESC,
                                     NEURON_EXTENDED_METADATA, SITE_POS_CARTESIAN, SIG_SELECT, KeyIndex)


def time_now():
    return datetime.datetime.now().strftime(TIME_SPEC)


def file_types(category='all'):
    '''
    File extensions for supported Radiens file types. 

    Parameters:
        category (str): optional, requested file category: 'all', 'recording', 'spikes', default='all'

    Returns:
        ext (list): list of requested category file extensions.

    Example:
        >>> file_types("recording")
        ['rhd', 'xdat', 'csv', 'hdf5', 'h5', 'nwb', 'kilosort2', 'nsx', 'pl2', 'tdt']

    '''
    rec = ['rhd', 'xdat', 'csv', 'hdf5', 'h5', 'nwb', 'kilosort2', 'nsx', 'pl2', 'tdt']
    spikes = ['spikes']
    if category in ['recording']:
        return rec
    if category in ['spikes']:
        return spikes
    if category in ['all']:
        rec.extend(spikes)
        return rec
    raise ValueError("category must be 'rec', 'spikes', 'all'")


def is_xdat_file(p: Path) -> bool:
    return Path(p.parent, p.stem+'_data.xdat').expanduser().resolve().is_file()


def rm_xdat_file(p: Path) -> None:
    if not is_xdat_file(p):
        return
    Path(p.parent, p.stem+'_data.xdat').expanduser().resolve().unlink()
    Path(p.parent, p.stem+'_timestamp.xdat').expanduser().resolve().unlink()
    Path(p.parent, p.stem+'.xdat.json').expanduser().resolve().unlink()


def make_site_pos(probe, tissue):
    return SITE_POS_CARTESIAN(probe_x=probe[0], probe_y=probe[1], probe_z=probe[2],
                              tissue_x=tissue[0], tissue_y=tissue[1], tissue_z=tissue[2])


def make_time_range(time_range: Union[list, np.ndarray] = None, timestamp: Union[list, np.ndarray] = None, fs: float = None, walltime: datetime.datetime = None, pbTR: common_pb2.TimeRange = None):
    '''
    Utility function to compose the TIME_RANGE named tuple composed from either a time range or timestamp list. 

    Parameters:
        time_range (list | numpy.ndarray): time range in seconds as [time start, time end] (optional, default=None). 
        timestamp (list | numpy.ndarray): timestamp in seconds as [timestamp start, timestamp end]  (optional, default=None). 
        fs (float): sampling frequency in samples/sec (required, default=None)
        walltime (datetime.datetime): wall time of the time range start.
        pbTR : low-level system parameter not available to user.

    Notes:

    TIME_RANGE named tuple fields: 
        `sec` (numpy.ndarray): [time start, time end]
        `timestamp` (numpy.ndarray): [timestamp start, timestamp end]
        `fs` (float): sampling frequency
        `walltime`: wall time of the time range start
        `dur_sec` (float): imputed time range duration equal to `TR.time_range[1]`-`TR.time_range[0]`.
        `N` (int): imputednumber of sample points equal to `TR.timestamp[1]`-`TR.timestamp[0]`.

    Either `timestamp` or `time_range` must be provided, with `timestamp` having preference. 
    `walltime` is optional.  `dur_sec` and `N` are imputed from the arguments. 

    System use only (not available to user)
    Either `pbTR` or (`fs` and either `time_range` or `timestamp`) must be provided as arguments. 
    `pbTR` has preference.  
    '''
    if isinstance(pbTR, common_pb2.TimeRange):
        return time_range_from_protobuf(pbTR)
    if fs in [None]:
        raise ValueError('missing fs')
    if walltime in [None]:
        walltime = datetime.datetime.min
    if isinstance(timestamp, (list, np.ndarray)):
        ts = np.array(timestamp).astype(np.int64)
        tr = np.array([ts[0]/fs, ts[1]/fs], dtype=np.float64)
    elif isinstance(time_range, (list, np.ndarray)):
        tr = np.array(time_range, dtype=np.float64)
        ts = np.array([tr[0]*fs, tr[1]*fs]).astype(np.int64)
    else:
        raise ValueError('missing both time_range and timestamp arg')
    return TIME_RANGE(sec=tr, timestamp=ts, fs=fs, walltime=walltime, N=ts[1]-ts[0], dur_sec=tr[1]-tr[0])


def time_range_to_protobuf(tr: TIME_RANGE) -> common_pb2.TimeRange:
    if not isinstance(tr, TIME_RANGE):
        raise ValueError('argument must be a TIME_RANGE')
    if len(tr.timestamp) != 2:
        raise ValueError('argument timestamp field does not have len=2')
    pbTR = common_pb2.TimeRange(timestamp=tr.timestamp.tolist(), fs=tr.fs)
    pbTimestamp = common_pb2.google_dot_protobuf_dot_timestamp__pb2.Timestamp()
    pbTimestamp.FromDatetime(tr.walltime)
    pbTR.wallTime.CopyFrom(pbTimestamp)
    return pbTR


def time_range_from_protobuf(pbTR: common_pb2.TimeRange) -> TIME_RANGE:
    if not isinstance(pbTR, common_pb2.TimeRange):
        raise ValueError('argument must be a common_pb2.TimeRange')
    if pbTR.timestamp not in [None] and len(pbTR.timestamp) == 2:
        ts = np.array(pbTR.timestamp).astype(np.int64)
        tr = np.array([ts[0]/pbTR.fs, ts[1]/pbTR.fs], dtype=np.float64)
    elif pbTR.timeRangeSec not in [None] and len(pbTR.timeRangeSec) == 2:
        tr = np.array(pbTR.timeRangeSec).astype(np.float64)
        ts = np.array([tr[0]*pbTR.fs, tr[1]*pbTR.fs], dtype=np.int64)
    if pbTR.wallTime not in [None]:
        wt = pbTR.wallTime.ToDatetime()
        if wt.year == 0:
            wt = datetime.datetime.min
    else:
        wt = datetime.datetime.min
    return make_time_range(timestamp=ts, fs=pbTR.fs, walltime=wt)


def sig_sel_to_protobuf(sig_sel: SIG_SELECT) -> common_pb2.SigSelector:
    if not isinstance(sig_sel, SIG_SELECT):
        raise ValueError('argument must be a SIG_SELECT')
    if sig_sel.key_idx not in [KeyIndex.NTV]:
        raise ValueError('sig_sel must use KeyIndex.NTV as the key index')
    return common_pb2.SigSelector(ampNtvIdxs=sig_sel.amp.tolist(),
                                  ainNtvIdxs=sig_sel.gpio_ain.tolist(),
                                  dinNtvIdxs=sig_sel.gpio_din.tolist(),
                                  doutNtvIdxs=sig_sel.gpio_dout.tolist())


def make_signal_selector(amp: Union[list, np.array] = None, ain: Union[list, np.array] = None, din: Union[list, np.array] = None, dout: Union[list, np.array] = None) -> SIG_SELECT:
    amp = np.array([], dtype=np.int64) if amp is None else np.array(amp, dtype=np.int64)
    ain = np.array([], dtype=np.int64) if ain is None else np.array(ain, dtype=np.int64)
    din = np.array([], dtype=np.int64) if din is None else np.array(din, dtype=np.int64)
    dout = np.array([], dtype=np.int64) if dout is None else np.array(dout, dtype=np.int64)
    return SIG_SELECT(amp=amp, gpio_ain=ain, gpio_din=din, gpio_dout=dout, key_idx=KeyIndex.NTV)


def make_neighbors_desc(nbr: biointerface_pb2.NeighborDescriptor):
    if not isinstance(nbr, biointerface_pb2.NeighborDescriptor):
        raise ValueError('arg must be pb.NeighborDescriptor')
    return NEIGHBORS_DESC(radius_um=nbr.radius, ntv_idxs=nbr.ntvChanIdx, distance_um=nbr.distance, theta_deg=nbr.thetaDeg,
                          phi_deg=nbr.phiDeg, N=nbr.num, pos=make_site_pos(nbr.SiteCenterUm, nbr.SiteCenterTcsUm))


def make_neuron_desc(msg: biointerface_pb2.NeuronDescriptor):
    if not isinstance(msg, biointerface_pb2.NeuronDescriptor):
        raise ValueError('arg must be pb.NeuronDescriptor')
    return NEURON_DESC(id=msg.neuronID, ntv_idx=msg.siteNtvChanIdx, label=msg.spikeLabel,
                       pos=make_site_pos(msg.posProbe, msg.posTissue), spike_count=msg.spikeCount,
                       spike_rate=msg.spikeRate, mean_abs_peak_waveform=msg.meanAbsPeakWfm, snr=msg.snr,
                       metadata=NEURON_EXTENDED_METADATA(neuron_uid=msg.metaData.neuronCatalogUID,
                                                         ensemble_uid=msg.metaData.ensembleUID,
                                                         func_assembly_uid=msg.metaData.funcAssemblyUID,
                                                         dataset_uid=msg.metaData.datasetUID,
                                                         probe_uid=msg.metaData.probeUID))


def from_dense_matrix(mtx: common_pb2.DenseMatrix) -> np.ndarray:
    return np.reshape(np.frombuffer(mtx.data, dtype=np.float64), (mtx.rows, mtx.cols))

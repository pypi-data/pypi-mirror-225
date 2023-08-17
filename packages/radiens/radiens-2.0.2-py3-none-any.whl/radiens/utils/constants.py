from collections import namedtuple
from enum import Enum
from pathlib import Path

from radiens.grpc_radiens import (allegoserver_pb2, allegoserver_pb2_grpc,
                                  common_pb2, spikesorter_pb2)

TIME_SPEC = "%Y-%m-%d %H:%M:%S"
SITE_POS_CARTESIAN = namedtuple("SitePositionCartesian", [
                                'probe_x', 'probe_y', 'probe_z', 'tissue_x', 'tissue_y', 'tissue_z'])
TIME_RANGE = namedtuple(
    "TIME_RANGE", ['sec', 'timestamp', 'fs', 'dur_sec', 'walltime', 'N'])

NEIGHBORS_DESC = namedtuple('NeighborsDescriptor', ['radius_um', 'ntv_idxs', 'distance_um', 'theta_deg',
                                                    'phi_deg', 'N', 'pos'])
NEURON_DESC = namedtuple('NeuronDescriptor', ['id', 'ntv_idx', 'label', 'pos', 'spike_count',
                                              'spike_rate', 'mean_abs_peak_waveform', 'snr', 'metadata'])
NEURON_EXTENDED_METADATA = namedtuple(
    'NeuronExtendedMetadata', ['neuron_uid', 'ensemble_uid', 'func_assembly_uid', 'dataset_uid', 'probe_uid'])

PORT_ENUM = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
SIGNAL_TYPE_ENUM = {0: 'amp', 1: 'gpio_ain', 2: 'gpio_din', 3: 'gpio_dout'}

SIGNALS = namedtuple("SIGNALS", ['amp', 'gpio_ain', 'gpio_din', 'gpio_dout'])
KEY_IDXS = namedtuple("KEY_IDXS", ['ntv', 'dset', 'sys'])

SIG_SELECT = namedtuple(
    "SIG_SELECT", ['amp', 'gpio_ain', 'gpio_din', 'gpio_dout', 'key_idx'])
''' SIG_SELECT is used for selecting signals by the given key index type, `key_idx`. The elements are numpy arrays '''


class SStat(Enum):
    MIN = 0
    MAX = 1
    MEAN = 2
    SD = 3
    Q1 = 4
    Q2 = 5
    Q3 = 6
    MODE = 4
    COUNT = 5


class KeyIndex(Enum):
    """
    An enumeration of key index types 

    Example: 
        >>> key_ind = KeyIndex.NTV 

    Valid values are as follows:
    """

    NTV = 0  #: native
    DATA = 1  #: data
    SYS = 2  #: system


class SignalType(Enum):
    """
    An enumeration of signal types

    Example:
        >>> sig_type = SignalType.AMP

    Valid values are as follows:
    """

    AMP = 0  #: primary signals
    AIN = 1  #: analog in
    DIN = 2  #: digital in
    DOUT = 3  #: digital out


ALL_SIGNAL_TYPES = [SignalType.AMP, SignalType.AIN,
                    SignalType.DIN, SignalType.DOUT]


class TRS_MODE(Enum):
    """
    TRS_MODE is the time range selector (TRS) enum used to control time range selection in calls to get signals, spikes, power spectral density, or similar data sets.  

    Example:
        >>> sel_mode = TRS_MODE.SUBSET 

    Given a time range [start, end) in seconds (dataset time), the selector modes are:
    """

    SUBSET = 0  #: selects [start, end)
    TO_HEAD = 1  #: selects [start, head of stream/cache/file]
    FROM_HEAD = 2  #: selects [(head of stream/cache/file - start)


class PSD_SCALING(Enum):
    '''PSD_SCALING is used to set the power spectral density (PSD) scale. 
    '''
    SPECTRUM = 0
    DENSITY = 1


class FFT_WINDOW(Enum):
    '''FFT_WINDOW is used to set the time-domain window function for power spectral density (PSD) analysis.  
    '''
    HAMMING_p01 = 0
    HAMMING_p05 = 1
    PASS_THROUGH = 2


DEFAULT_IP = 'localhost'
DEFAULT_HUB = 'default'


# ports
ALLEGO_CORE_PORT = 50051
PCACHE_PORT = 50052
KPI_PORT = 50053
NEURONS1_PORT = 50054

# default server addresses
CORE_ADDR = '{}:{}'.format(DEFAULT_IP, ALLEGO_CORE_PORT)
PCACHE_ADDR = '{}:{}'.format(DEFAULT_IP, PCACHE_PORT)
KPI_ADDR = '{}:{}'.format(DEFAULT_IP, KPI_PORT)
NEURONS1_ADDR = '{}:{}'.format(DEFAULT_IP, NEURONS1_PORT)

MAX_PB_MSG_SIZE_BYTES = 60e6  # actually limit is 64MB


# services
CORE_SERVICE = 'core'
PCACHE_SERVICE = 'pcache'
DASH_SERVICE = 'dash'
SPIKE_SORTER_SERVICE = 'sorter'

# only allego stream group
PRIMARY_CACHE_STREAM_GROUP_ID = 'Live Signals'
NEURONS_SINK_DSOURCE_ID = 'sorter-sink:primary_cache'
SPIKE_SORTER_ID = PRIMARY_CACHE_STREAM_GROUP_ID

# default datasource paths
DATASOURCE_PATHS = {
    'dsrc_path': Path(Path.home(), 'radix', 'data'),
    'dsrc_type': 'xdat',
    'dsrc_name': 'sbpro'
}

# ports/signals
PORT_ENUM = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
PORT_ = {'A': common_pb2.A,  'B': common_pb2.B, 'C': common_pb2.C,  'D': common_pb2.D,
         'E': common_pb2.E,  'F': common_pb2.F, 'G': common_pb2.G,  'H': common_pb2.H}
SIGNAL_TYPE_ENUM = {0: 'amp', 1: 'adc', 2: 'din', 3: 'dout'}
SIGNAL_TYPES = ['amp', 'adc', 'din', 'dout']

# system
SYSTEM_MODE = {
    'sbpro': allegoserver_pb2.SMARTBOX_PRO,
    'sbpro-sinaps-256': allegoserver_pb2.SMARTBOX_PRO_SINAPS_256,
    'sbpro-sinaps-1024': allegoserver_pb2.SMARTBOX_PRO_SINAPS_1024,
    'sb-classic': allegoserver_pb2.SMARTBOX_CLASSIC,
    'sim-sine': allegoserver_pb2.SMARTBOX_SIM_GEN_SINE,
    'sim-sine-mapped': allegoserver_pb2.SMARTBOX_SIM_GEN_SINE_MAPPED,
    'sim-sine-high-freq': allegoserver_pb2.SMARTBOX_SIM_GEN_SINE_HIGH_FREQ,
    'sim-sine-multi-band': allegoserver_pb2.SMARTBOX_SIM_GEN_SINE_MULTI_BAND,
    'sim-spikes': allegoserver_pb2.SMARTBOX_SIM_GEN_SPIKES,
    'open-ephys_usb2': allegoserver_pb2.OPEN_EPHYS_USB2,
    'open-ephys_usb3': allegoserver_pb2.OPEN_EPHYS_USB3,
    'intan-usb2': allegoserver_pb2.INTAN_USB2,
    'intan-1024': allegoserver_pb2.INTAN_RECORDING_CONTROLLER_1024,
    'intan-512': allegoserver_pb2.INTAN_RECORDING_CONTROLLER_512,
    'xdaq-one-rec': allegoserver_pb2.XDAQ_ONE_REC,
    'xdaq-one-stim': allegoserver_pb2.XDAQ_ONE_STIM,
    'xdaq-core-rec': allegoserver_pb2.XDAQ_CORE_REC,
    'xdaq-core-stim': allegoserver_pb2.XDAQ_CORE_STIM,
}

SYSTEM_MODE_DECODE = {
    0: 'sbox-pro',
    1: 'sim-sine',
    2: 'sim-spikes',
    4: 'open-ephys-usb3',
    5: 'intan-1024',
    6: 'sb-classic',
    7: 'intan-512',
    8: 'open-ephys-usb2',
    9: 'intan-usb2',
    10: 'sim-sine-mapped',
    11: 'sim-sine-high-freq',
    12: 'sim-sine-multi-band',
    13: 'sbpro-sinaps-256',
    14: 'sbpro-sinaps-1024',
    15: 'xdaq-one-rec',
    16: 'xdaq-one-stim',
    17: 'xdaq-core-rec',
    18: 'xdaq-core-stim',
}

DOUT_MODE_OUT = {
    0: 'manual',
    1: 'events',
    2: 'gated'
}

APPS_ = {0: 'allego', 1: 'curate', 2: 'videre'}

# stream/record
STREAM_MODE = {'S_OFF': 0, 'S_ON': 1}
RECORD_MODE = {'R_OFF': 0, 'R_ON': 1}
STREAM_MODE_OUT = {0: 'S_OFF', 1: 'S_ON'}
RECORD_MODE_OUT = {0: 'R_OFF', 1: 'R_ON'}

# sensors
HEADSTAGE_ALIAS = {'smart-16': 'acute_smartlink_A16', 'smart-32': 'chronic_smartlink_CM32',
                   'pass-32': 'passthrough_32',  'pass-64': 'passthrough_64', 'chronic-64': 'chronic_smartlink_H64'}

PROBE_ALIAS = {'v1x16-16': 'v1x16_edge_10mm200_177', '4x8-32': 'a4x8_5mm100_200_177',
               '8x1tet-32': 'a8x1_tet_7mm_200_121',  'buz-32': 'buz32', 'poly3-32': 'a1x32_poly3_8mm50s_177',
               ' poly5-32': 'a1x32_poly5_6mm35s_100',  '8x8-64': 'a8x8_5mm200_200_413', 'poly3-64': 'v1x64_poly3_10mm25s_177',
               'buz-64': 'buz64'}

SPK_SORTER_STATE_DECODE = {0: 'on', 1: 'off', 2: 'not_configured'}

import datetime
from collections import namedtuple
from pathlib import Path

import numpy as np
import pandas as pd
from radiens.api.api_utils.util import (to_matrix_from_protobuf_dense_matrix,
                                        to_matrix_from_protobuf_radix_matrix)
from radiens.grpc_radiens import common_pb2, datasource_pb2
from radiens.lib.channel_metadata import ChannelMetadata
from radiens.utils.constants import (FFT_WINDOW, PSD_SCALING, SIGNALS,
                                     TIME_RANGE)
from radiens.utils.util import time_range_from_protobuf


class Signals():
    '''
    Container for a multi-channel (multi-trace) dataset for amplifier, GPIO analog in, GPIO digital in, and GPIO digital out signals. 

    All traces for all signal types have the same sampling frequency and start and end times.  Thus, the set of traces of each signal type is a 2-D matrix.  
    '''

    def __init__(self, raw: common_pb2.HDSnapshot2):
        """
        """
        if not isinstance(raw, common_pb2.HDSnapshot2):
            raise TypeError('raw must be common_pb2.HDSnapshot2')
        self._d = {'dsource_id': raw.dsourceID}
        self._sgrp = ChannelMetadata(raw.sigs.sG)
        self._tr = time_range_from_protobuf(raw.sigs.tR)
        self._sigs = SIGNALS(amp=to_matrix_from_protobuf_radix_matrix(raw.sigs.amp),
                             gpio_ain=to_matrix_from_protobuf_radix_matrix(raw.sigs.ain),
                             gpio_din=to_matrix_from_protobuf_radix_matrix(raw.sigs.din),
                             gpio_dout=to_matrix_from_protobuf_radix_matrix(raw.sigs.dout))

    @ property
    def time_range(self) -> TIME_RANGE:
        """
        dataset time range in seconds
        """
        return self._tr

    @ property
    def TR(self) -> TIME_RANGE:
        """
        Aliases dataset time range.
        """
        return self._tr

    @ property
    def signals(self) -> SIGNALS:
        """
        Time-series signals as a named tuple by signal type.  

        For each signal type, the multi-channel dataset is a 2-D numpy array, with dim 0=trace position and dim 1 is the sample values over the time range. 
        """
        return self._sigs

    @ property
    def attributes(self) -> dict:
        """
        Dataset attributes
        """
        return self._d

    @ property
    def channel_metadata(self) -> ChannelMetadata:
        """
        Dataset channel metadata 
        """
        return self._sgrp


class PSD():
    '''
    Container for a multi-channel (multi-trace) power spectrum density (PSD) dataset. 
    '''

    def __init__(self, raw: common_pb2.PSD):
        """
        """
        if not isinstance(raw, common_pb2.PSD):
            raise TypeError('raw must be common_pb2.PSD')
        self._d = {'dsource_id': raw.dsourceID, 'wdw_type': FFT_WINDOW(raw.wdwType),
                   'scaling': PSD_SCALING(raw.scaling), 'freq_bin_width': raw.freqBinWidth}
        self._sgrp = ChannelMetadata(raw.sG)
        self._tr = time_range_from_protobuf(raw.tR)
        self._psd = to_matrix_from_protobuf_dense_matrix(raw.psd)
        self._freq = np.array(raw.freq, dtype=np.float64)
        self._freq_range = np.array(raw.freqRange, dtype=np.float64)

    @ property
    def time_range(self) -> TIME_RANGE:
        """
        dataset time range in seconds.
        """
        return self._tr

    @ property
    def TR(self) -> TIME_RANGE:
        """
        Aliases dataset time range.
        """
        return self._tr

    @ property
    def psd(self) -> np.ndarray:
        """
        Power spectral density   

        """
        return self._psd

    @ property
    def frequencies(self) -> np.ndarray:
        """
        PSD frequencies

        """
        return self._freq

    @ property
    def freq_range(self) -> np.ndarray:
        """
        PSD frequency range as [freq start, obj.frequencies[-1]+obj.freq_bin_width) in Hz.

        """
        return self._freq_range

    @ property
    def freq_bin_width(self) -> float:
        """
        PSD frequency bin width in Hz 

        """
        return self._d['freq_bin_width']

    @ property
    def attributes(self) -> dict:
        """
        Dataset attributes
        """
        return self._d

    @ property
    def channel_metadata(self) -> ChannelMetadata:
        """
        Dataset channel metadata 
        """
        return self._sgrp

import pandas as pd
import numpy as np
import datetime
from collections import namedtuple
from pathlib import Path
from enum import Enum
from radiens.grpc_radiens import (common_pb2, allegoserver_pb2, datasource_pb2, biointerface_pb2)
from radiens.api.api_utils.util import (to_file_ext)
from radiens.utils.constants import (TIME_RANGE)
from radiens.utils.util import (make_time_range, make_neighbors_desc, make_neuron_desc)
from radiens.lib.channel_metadata import (ChannelMetadata)


class SelectorTables():
    '''
    Radiens container for selector tables
    '''

    def __init__(self, msg):
        """
        """

        if not isinstance(msg, common_pb2.SelectorTablesReply):
            raise TypeError('invalid msg type')

        self._tables = {'sig': None}
        p = {'index': [], 'criterion': [], 'ntv_idxs': [], 'num_sigs': []}
        self._tables['sig'] = pd.DataFrame(p)
        for rec in msg.sig:
            p['index'].append(rec.index)
            p['criterion'].append(rec.criterionDesc)
            p['ntv_idxs'].append(rec.ntvIdxs)
            p['num_sigs'].append(rec.numSigs)
        self._tables['sig'] = pd.DataFrame(p).sort_values(by='index')

    @ property
    def df_signals(self) -> pd.DataFrame:
        """
        Table of signal selectors
        """
        return self._tables['sig']

    @ property
    def tables(self) -> dict:
        """
        Dictionary of signal selector tables
        """
        return self._tables

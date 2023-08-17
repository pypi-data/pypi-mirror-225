from collections.abc import Iterable
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
import radiens.api.api_videre as api
import radiens.api.api_videre as api_videre
from numpy.random import default_rng
from radiens.api.api_utils.util import (BaseClient, get_dataset_id,
                                        get_dataset_idx_from_id,
                                        to_radiens_file_type)
from radiens.grpc_radiens import common_pb2, datasource_pb2
from radiens.lib.dataset_metadata import DatasetMetadata
from radiens.lib.sig_metrics import METRIC, METRIC_ID, METRIC_MODE
from radiens.metrics_client import MetricsClient
from radiens.signals_client import SignalsClient
from radiens.spike_sorter import SpikeSorterClient
from radiens.spikes_client import SpikesClient
from radiens.utils.constants import (CORE_SERVICE, DASH_SERVICE, DEFAULT_HUB,
                                     SIG_SELECT, TIME_RANGE, TRS_MODE,
                                     KeyIndex)


class VidereClient(BaseClient):
    """
    VidereClient implements the radiens API for offline analysis and visualization.
    It matches and extends the functionality of the Radiens Videre UI app.
    """

    def __init__(self, hub_name=DEFAULT_HUB):
        """
        """
        super().__init__()
        self._default_hub = hub_name
        self._sorter = SpikeSorterClient(self)
        self._spikes = SpikesClient(self)
        self._metrics = MetricsClient(self)
        self._signals = SignalsClient(self)

    @property
    def hubs(self) -> dict:
        """
        dict of active radiens hubs, with hub ID as key.
        """
        return self._hubs()

    @property
    def hub(self) -> str:
        """
        Radiens hub for this instance of VidereClient.
        """
        return self._default_hub

    @property
    def id(self) -> str:
        """
        UID of this client session.
        """
        return self._id()

    @property
    def type(self) -> str:
        """
        Returns 'videre'
        """
        return 'videre'

    def signal_metrics(self) -> MetricsClient:
        """
        Videre signal metrics API
        """
        return self._metrics

    def spike_sorter(self) -> SpikeSorterClient:
        """
        Videre spike sorter API
        """
        return self._sorter

    def spikes(self) -> SpikesClient:
        """
        Videre spikes API
        """
        return self._spikes

    def signals(self) -> SignalsClient:
        """
        Signals API
        """
        return self._signals

    def link_data_file(self, path:  Union[Path, str], calc_metrics: bool = True, force: bool = False, hub_name=DEFAULT_HUB) -> DatasetMetadata:
        """
            Links a Radiens data file to the Radiens hub and returns the data set meta data.
            If force=False (default) and the 'path' is already linked then nothing is done and existing data set meta data is returned.
            Use force=True to always link the source as a new dataset. All instances of a linked data set are backed by the same data files.

            This is a power user function.

            Parameters:
                path (str, pathlib.Path): path to source file
                calc_metrics (bool) optional: use True to calculate signal metrics (default=True)
                force (bool) optional: use True to force the source to be linked to the hub (default=False)
                hub_name (str) optional: radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

            Returns:
                data_source (DatasetMetadata): data file metadata

            See Also:
                :py:meth:`rename_file`
                :py:meth:`clear_dataset()`
                :py:meth:`get_dataset_ids()`
        """
        if isinstance(path, (Path, str)):
            path = Path(path).expanduser().resolve()
        else:
            raise TypeError('source must be string or Path')
        req = datasource_pb2.DataSourceSetSaveRequest(path=str(path.parent), baseName=path.stem, fileType=to_radiens_file_type(
            path), dsourceID=path.stem+self.id, isBackgroundKPI=calc_metrics, isForce=force)
        return api_videre.set_datasource(self._server_address(hub_name, CORE_SERVICE), req)

    def get_data_file_metadata(self, dataset_idx: int = None, dataset_id: str = None, path: Union[Path, str] = None, hub_name=DEFAULT_HUB, fail_hard=False) -> DatasetMetadata:
        """
            Returns meta data for one Radiens dataset or file.  The dataset can be requested by index, ID or full path, in that order of preference.

            Parameters:
                dataset_idx (int): index of dataset in table returned by :py:meth:`get_dataset_ids` or :py:meth:`get_selector_tables`
                dataset_id (str): dataset ID as listed in table returned by :py:meth:`get_dataset_ids` or :py:meth:`get_selector_tables`
                path (str, pathlib.Path): full path to data file set in form of `path/base_name.ext`.
                hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)
                fail_hard (bool): if True, then an exception is raised if the requested dataset is not available.

            Returns:
                dataset_meta (DatasetMetadata): data set metadata

            Side Effects:
                If the requested dataset is specified by `path`, then it is linked to the hub and remains linked.

            See Also:
                :py:meth:`rename_file`
                :py:meth:`_clear_dataset`
                :py:meth:`get_dataset_ids`
        """
        dataset_id, path = get_dataset_id(self.get_dataset_ids(), self.id, hub_name, dataset_idx=dataset_idx,
                                          dataset_id=dataset_id, path=path, fail_hard=fail_hard)
        if dataset_id is not None:
            if path is None:
                req = datasource_pb2.DataSourceSetSaveRequest(
                    dsourceID=dataset_id, isBackgroundKPI=False, isForce=False)
            else:
                req = datasource_pb2.DataSourceSetSaveRequest(path=str(path.expanduser().resolve().parent), baseName=path.stem, fileType=to_radiens_file_type(
                    path), isBackgroundKPI=False, isForce=False)
            return api_videre.set_datasource(self._server_address(hub_name, CORE_SERVICE), req)
        return DatasetMetadata(raw_msg=None)

    def clear_dataset(self, dataset_idx: int = None, dataset_id: str = None, path: Union[Path, str] = None, hub_name=DEFAULT_HUB, fail_hard=False) -> any:
        """
            Clears one or more datasets of this Curate session from the Radiens hub.
            Use dataset_id='all' to clear all session datasets.
            This is a power user function.

            Parameters:
                source (str, list) optional: data source file or list of data source files.
                dataset_id (str, list) optional: dataset ID or list of dataset IDs (default=[], 'all' clears all datasets for the Curate session)
                hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

            Returns:
                num_unlinked (int): number of unlinked datasets
                dataset_ids (pandas.DataFrame): linked dataset IDs on the Radiens hub.

            See Also:
                :py:meth:`link_data_file()`
                :py:meth:`get_dataset_ids()`
        """
        available_dataset_ids = self.get_dataset_ids()
        if dataset_id in ['all'] or dataset_idx in ['all']:
            dataset_id = available_dataset_ids['dataset ID'].values
            api_videre.unlink_datasource(self._server_address(
                hub_name, CORE_SERVICE), dataset_id)
        else:
            dataset_id, _ = get_dataset_id(available_dataset_ids, self.id, hub_name, dataset_idx=dataset_idx,
                                           dataset_id=dataset_id, path=path, fail_hard=fail_hard)
            if dataset_id is not None:
                api_videre.unlink_datasource(self._server_address(
                    hub_name, CORE_SERVICE), [dataset_id])
        new_avail = self.get_dataset_ids(hub_name=hub_name)
        return len(available_dataset_ids)-len(new_avail), new_avail

    def get_dataset_ids(self, hub_name=DEFAULT_HUB) -> pd.DataFrame:
        """
            Returns sorted list of linked dataset IDs on the Radiens hub.

            Returns:
                dataset_ids (pandas.DataFrame): linked dataset IDs on the Radiens hub.

            See Also:
                :py:meth:`link_data_file()`
                :py:meth:`clear_dataset()`
        """
        resp = api_videre.list_datasource_ids(
            self._server_address(hub_name, CORE_SERVICE))
        df = pd.DataFrame({'dataset ID': resp, 'base name': [x[:x.find('_-_')]
                                                             for x in resp]}).sort_values(by='dataset ID', axis=0).reset_index(drop=True)
        df.index.name = 'index'
        return df

    def dashboard(self, close: bool = False, hub_name=DEFAULT_HUB) -> None:
        """
            Launches a dashboard for the Radiens Hub

            Returns:
                None
        """
        if self.type in ['allego']:
            raise ValueError('dashboards are not implemented for Allego')
        args = common_pb2.DashboardCommandRequest.Args(
            cmd=common_pb2.DASH_CMD_CLOSE) if close else common_pb2.DashboardCommandRequest.Args(cmd=common_pb2.DASH_CMD_OPEN)
        req = common_pb2.DashboardCommandRequest(
            args=args, dashType=common_pb2.DASH_1)
        api_videre.command_dashboard(
            self._server_address(hub_name, DASH_SERVICE), req)

import time
import warnings
import uuid
from pathlib import Path
from tqdm.autonotebook import tqdm
import radiens.api.api_curate as api_allego
import radiens.api.api_videre as api_videre
import radiens.utils.config as cfg
from radiens.api.api_utils.protocols import (ProtocolAPI, TransformEdge, TransformNode)
from radiens.api.api_utils.util import to_file_ext, to_radiens_file_type
from radiens.grpc_radiens import common_pb2, datasource_pb2
from radiens.base_client import BaseClient
from radiens.utils.constants import (CORE_SERVICE, DEFAULT_HUB, DEFAULT_IP)
from radiens.utils.util import rm_xdat_file


class MetricsBaseClient(BaseClient):
    """
    Base metrics client object for CurateClient, VidereClient
    """

    def __init__(self):
        """
        """
        super().__init__()

    def get_metrics_status(self, dataset_id: str, hub_name=DEFAULT_HUB):
        """
        Returns the status of the stream metrics service

        Parameters:
            dataset_id (str, list) optional: dataset ID or list of dataset IDs (default=[], 'all' clears all datasets for the Curate session)
            hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

        Returns:
            status (dict): dict of status parameters, with keys='time_range','packet_dur_sec', 'beta', 'is_tracking_cache',
                'wall_time_start', 'persistence_sec'
        """
        resp = api_videre.get_kpi_status(self._server_address(hub_name, CORE_SERVICE), dataset_id)
        return {'time_range': [resp.timeRange[0], resp.timeRange[1]], 'packet_dur_sec': resp.packetDur, 'beta': resp.beta, 'is_tracking_cache': resp.isTrackingSignalCache,
                'wall_time_start': resp.wallTimeStart, 'persistence_sec': resp.persistence}

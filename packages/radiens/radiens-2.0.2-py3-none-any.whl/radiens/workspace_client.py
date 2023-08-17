import time
import uuid
import warnings
from pathlib import Path

import radiens.api.api_allego as api
from radiens.api.api_utils.protocols import (ProtocolAPI, TransformEdge,
                                             TransformNode)
from radiens.api.api_utils.util import BaseClient
from radiens.grpc_radiens import common_pb2, datasource_pb2
from radiens.utils.constants import (CORE_ADDR, CORE_SERVICE, DEFAULT_HUB,
                                     DEFAULT_IP)
from radiens.utils.util import rm_xdat_file
from tqdm.autonotebook import tqdm


class WorkspaceClient(BaseClient):
    """
    Workspace client object for AllegoClient
    """

    def __init__(self):
        """
        """
        super().__init__()

    @property
    def hubs(self) -> dict:
        """
        dict of active radiens hubs, with hub ID as key.
        """
        return self._hubs()

    @property
    def id(self) -> str:
        """
        UID of this client session.
        """
        return self._id()

    def workspace_save(self, workspace_id=None, tags='', notes=''):
        """
        Saves current workspace

        Parameters:
            workspace_id (str): optional workspace ID
            tags (str): optional tags
            notes (str): optional notes

        Returns:
            None

        Example:
            >>> client.workspace_save(workspace_id='my_wspace', tags='my_tags', notes='my_notes)
            None
        """
        if workspace_id is None:
            return api.workspace_save(CORE_ADDR, True, tags, notes)
        else:
            return api.workspace_save_as(CORE_ADDR, workspace_id, True, tags, notes)

    def workspace_switch(self, workspace_id: str):
        """
        Switches to requested workspace

        Parameters:
            workspace_id (str): workspace ID

        Returns:
            None

        Example:
            >>> client.workspace_switch('my_wspace')
            None
        """
        return api.workspace_switch(CORE_ADDR, workspace_id)

    def workspace_delete(self, workspace_id: str):
        """
        Deletes requested workspace 

        Parameters:
            workspace_id (str): workspace ID

        Returns:
            None

        Example:
            >>> client.workspace_delete('my_wspace')
            None
        """
        return api.workspace_delete(CORE_ADDR, workspace_id)

    def workspace_current(self):
        """
        Returns current workspace ID

        Returns:
            workspaces (pandas.DataFrame)

        Example:
            >>> client.workspace_current()
            df
        """
        return api.workspace_current(CORE_ADDR)

    def workspace_list(self):
        """
        Returns table of all available workspaces

        Returns:
            workspaces (pandas.DataFrame)

        Example:
            >>> client.workspace_list()
            df
        """
        return api.workspace_list(CORE_ADDR)

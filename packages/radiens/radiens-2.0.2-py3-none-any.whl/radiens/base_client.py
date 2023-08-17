import uuid
from collections.abc import Iterable
from pathlib import Path

import radiens.api.api_curate as api_allego
import radiens.api.api_videre as api_videre
import radiens.utils.config as cfg
from radiens.api.api_utils.util import to_radiens_file_type
from radiens.grpc_radiens import common_pb2, datasource_pb2
from radiens.lib.dataset_metadata import DatasetMetadata
from radiens.lib.fsys import FileSysResponse
from radiens.utils.constants import CORE_SERVICE, DEFAULT_HUB, DEFAULT_IP, SPIKE_SORTER_SERVICE


class BaseClient:
    """
    Base client object for AllegoClient, CurateClient, VidereClient
    """

    def __init__(self):
        """
        """
        self._client_id = '_-_'+str(uuid.uuid4())[4:13]
        self.__core_port = cfg.get_radiens_service_port(CORE_SERVICE)
        self._hubs = {DEFAULT_HUB: {'ip_address': DEFAULT_IP, 'port': self.__core_port}}
        self._dsp_stream = {}

    def add_hub(self, new_hub: dict):
        # Add a hub (ip address of radiens server)
        #   Args:
        #       hub : dict
        #           key(s) (str): hub name(s)
        #           values (dict): {'ip_address': ip_address}
        for k in new_hub:
            if 'ip_address' in new_hub[k]:
                self._hubs[k] = {
                    'ip_address': new_hub[k]['ip_address'],
                    'port': new_hub[k]['port'] if 'port' in new_hub[k] else self.__core_port
                }

    def _server_address(self, hub_name, service):
        # creates server address from hub and service
        if service == 'core':
            return '{}:{}'.format(self._hubs[hub_name]['ip_address'], self._hubs[hub_name]['port'])
        else:
            raise AssertionError('invalid service name = {}'.format(service))

    @property
    def hubs(self) -> dict:
        """
        dict of active radiens hubs, with hub ID as key.
        """
        return self._hubs

    @property
    def id(self) -> str:
        """
        UID of this client session.
        """
        return self._client_id

    def ls(self, req_dir: any, sort_by='date', hub_name=DEFAULT_HUB) -> FileSysResponse:
        """
            Aliases client.list_dir() to lists Radiens recording and/or spikes files in the requested directory.

            See Also:
                :py:meth:`list_dir()`
        """
        pArgs = []
        if isinstance(req_dir, (Path, str)):
            pArgs = [str(Path(req_dir).expanduser().resolve())]
        elif isinstance(req_dir, (list, tuple, Iterable)):
            for x in req_dir:
                pArgs.append(str(Path(x).expanduser().resolve()))
        else:
            raise TypeError('req_dir must be list, tuple, string or Path')
        return api_allego.dsrc_list_dir(self._server_address(hub_name, CORE_SERVICE),  pArgs, sort_by)

    def list_dir(self, req_dir: any, sort_by='date', include='all', hub_name=DEFAULT_HUB) -> FileSysResponse:
        """
            Lists Radiens recording and/or spikes files in the requested directory.

            Parameters:
                req_dir (str, pathlib.Path): requested directory
                sort_by (str): flag to specify the ordering of the returned file list, 'date', 'name', 'size', 'type' (default='date)
                include (str): flag to specify file types, 'recording', 'time-series', 'spikes', 'all' (default='all')
                hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

            Returns:
                file_type (pandas.DataFrame): table of files in the requested directory

            Example:
                >>> client.list_dir("./")
                pandas.DataFrame

            Notes:
                Directory name wildcards are allowed, but must resolve to only one directory.

            See Also:
                :py:meth:`ls`
        """
        return self.ls(req_dir, sort_by, include, hub_name)

    def copy_files(self, source: any, dest: any, force=False,  hub_name=DEFAULT_HUB) -> FileSysResponse:
        """
            Copies one or more Radiens files.

            Parameters:
                source (str, pathlib.Path, list): path to source file(s)
                dest (str, pathlib.Path): path to destination file(s)
                force (bool): flag to force copy if destination file already exists (default=False)
                hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

            Returns:
                file_type (pandas.DataFrame): table of copied files.

            Example:
                >>> client.copy_files("./my_rec_file.xdat", './targ_dir/new_file')
                pandas.DataFrame

            Notes:
                The destination file type is always the same as the source file type.
                File name wildcards are allowed, but must resolve to only one file.

            See Also:
                :py:meth:`cp`
        """
        return self.cp(source, dest, force, hub_name)

    def cp(self, source: any, dest: any, force=True,  hub_name=DEFAULT_HUB) -> FileSysResponse:
        """
            Aliases client.copy_files() to copy one or more Radiens files.

            See Also:
                :py:meth:`copy_files`
        """
        src_one = None
        src_many = None
        if isinstance(source, (Path, str)):
            src_one = Path(source).expanduser().resolve()
        elif isinstance(source, (list, Iterable)):
            src_many = []
            for file in source:
                src_many.append(Path(file).expanduser().resolve())
        else:
            raise ValueError('source must be string, Path, or list')

        if not isinstance(dest, (Path, str)):
            raise ValueError('dest must be string or Path')

        dest = Path(dest).expanduser().resolve()
        if src_one is not None:
            src_desc = common_pb2.FileDescriptor(
                path=str(src_one.parent), baseName=src_one.stem, fileType=to_radiens_file_type(src_one))
            if dest.is_dir():
                dest = Path(dest, src_one.name)
            dest_desc = common_pb2.FileDescriptor(
                path=str(dest.parent), baseName=dest.stem, fileType=to_radiens_file_type(src_one))
            req_one = datasource_pb2.CopyRemoveDataSourceFileRequest.OneFile(src=src_desc, dest=dest_desc)
            req = datasource_pb2.CopyRemoveDataSourceFileRequest(isForce=bool(force), one=req_one)
            return api_allego.dsrc_copy(self._server_address(hub_name, CORE_SERVICE), req)

        # many files
        if not dest.is_dir():
            raise ValueError('dest must be a path when copying multiple files')
        src_desc = []
        for file in src_many:
            src_desc.append(common_pb2.FileDescriptor(
                path=str(file.parent), baseName=file.stem, fileType=to_radiens_file_type(file)))
        req_many = datasource_pb2.CopyRemoveDataSourceFileRequest.MultipleFiles(
            src=src_desc, destPath=str(dest), destFileType=to_radiens_file_type(Path(file)))
        req = datasource_pb2.CopyRemoveDataSourceFileRequest(isForce=bool(force), many=req_many)
        return api_allego.dsrc_copy(self._server_address(hub_name, CORE_SERVICE), req)

    def delete_files(self, source: any, dry_run=False,  hub_name=DEFAULT_HUB) -> FileSysResponse:
        """
            Deletes (aka removes) one or more Radiens files.

            Parameters:
                source (str, pathlib.Path, list): path to source file(s)
                dry_run (bool): flag to list the requested files without deleting them (default=False)
                hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

            Returns:
                file_type (pandas.DataFrame): table of copied files.

            Example:
                >>> client.delete_files("./my_rec_file.xdat")
                pandas.DataFrame

            Notes:
                The requested files are permanently deleted from the file system.
                File name wildcards are allowed, but must resolve to only one file.

            See Also:
                :py:meth:`rm`
        """
        return self.rm(source, dry_run, hub_name)

    def rm(self, source: any, hub_name=DEFAULT_HUB) -> FileSysResponse:
        """
            Aliases client.delete_files() to delete (aka remove) one or more Radiens files.

            See Also:
                :py:meth:`delete_files`
        """
        src_many = []
        if isinstance(source, (Path, str)):
            src_many = [Path(source).expanduser().resolve()]
        elif isinstance(source, (list, Iterable)):
            for file in source:
                src_many.append(Path(file).expanduser().resolve())
        else:
            raise ValueError('source type must be string, Path, or list')

        src_desc = []
        for file in src_many:
            src_desc.append(common_pb2.FileDescriptor(
                path=str(file.parent), baseName=file.stem, fileType=to_radiens_file_type(file)))
        req_many = datasource_pb2.CopyRemoveDataSourceFileRequest.MultipleFiles(src=src_desc)
        req = datasource_pb2.CopyRemoveDataSourceFileRequest(isForce=True, many=req_many)
        return api_allego.dsrc_remove(self._server_address(hub_name, CORE_SERVICE), req)

    def rename_file(self, source: any, dest=any, force=False, validate=True, hub_name=DEFAULT_HUB) -> FileSysResponse:
        """
            Renames (aka moves) one Radiens file.

            Parameters:
                source (str, pathlib.Path): path to source file
                dest (str, pathlib.Path): path to destination file
                dry_run (bool): flag to list the requested files without deleting them (default=False)
                force (bool): flag to force renaming if the destination file exists (default=False)
                hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

            Returns:
                file_type (pandas.DataFrame): table of renamed file.

            Example:
                >>> client.rename_files("./my_rec_file.xdat", "./targ_dir/my_rec_file")
                pandas.DataFrame

            Notes:
                The destination file type is the same as the source file type.
                File name wildcards are allowed, but must resolve to only one file.

            See Also:
                :py:meth:`mv`
        """
        return self.mv(source, dest, force, validate, hub_name)

    def mv(self, source: any, dest=any, force=True, validate=True, hub_name=DEFAULT_HUB) -> FileSysResponse:
        """
            Aliases client.rename_file() to rename (aka move) one Radiens file.

            See Also:
                :py:meth:`rename_file`
        """
        if isinstance(source, (Path, str)):
            src = Path(source).expanduser().resolve()
        else:
            raise ValueError('source must be string or Path')
        if isinstance(dest, (Path, str)):
            dest = Path(dest).expanduser().resolve()
        else:
            raise ValueError('dest must be string or Path')

        src_desc = common_pb2.FileDescriptor(
            path=str(src.parent), baseName=src.stem, fileType=to_radiens_file_type(src))
        dest_desc = common_pb2.FileDescriptor(
            path=str(dest.parent), baseName=dest.stem, fileType=to_radiens_file_type(dest))
        req = datasource_pb2.MoveDataSourceFileRequest(isForce=force, isValidate=validate, src=src_desc, dest=dest_desc)
        return api_allego.dsrc_move(self._server_address(hub_name, CORE_SERVICE), req)

    def link_data_file(self, source: any, calc_metrics=False, hub_name=DEFAULT_HUB) -> DatasetMetadata:
        """
            Links a Radiens data file to the Radiens hub as a new dataset.
            This is a power user function.

            Parameters:
                source (str, pathlib.Path): path to source file
                calc_metrics (bool) optional: set True to calculate signal metrics (default=False)
                hub_name (str) optional: radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

            Returns:
                data_source (DatasetMetadata): data file metadata

            See Also:
                :py:meth:`rename_file`
                :py:meth:`clear_dataset()`
                :py:meth:`get_dataset_ids()`
        """
        if isinstance(source, (Path, str)):
            source = Path(source).expanduser().resolve()
        else:
            raise ValueError('source must be string or Path')
        req = datasource_pb2.DataSourceSetSaveRequest(path=str(source.parent), baseName=source.stem, fileType=to_radiens_file_type(
            source), dsourceID=source.stem+self.id, isBackgroundKPI=calc_metrics)
        return api_videre.set_datasource(self._server_address(hub_name, CORE_SERVICE), req)

    def get_data_file_metadata(self, source: any, hub_name=DEFAULT_HUB) -> DatasetMetadata:
        """
            Returns the meta data for a Radiens data file. 

            Parameters:
                source (str, pathlib.Path): path to source file
                hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

            Returns:
                data_source (DatasetMetadata): data file metadata

            See Also:
                :py:meth:`rename_file`
                :py:meth:`clear_dataset()`
                :py:meth:`get_dataset_ids()`
        """
        if isinstance(source, (Path, str)):
            source = Path(source).expanduser().resolve()
        else:
            raise ValueError('source must be string or Path')
        req = datasource_pb2.DataSourceSetSaveRequest(path=str(source.parent), baseName=source.stem, fileType=to_radiens_file_type(
            source), dsourceID=source.stem+self.id, isBackgroundKPI=False)
        dsrc = api_videre.set_datasource(self._server_address(hub_name, CORE_SERVICE), req)
        self.clear_dataset(dsrc.id)
        dsrc.clear_dataset_id()
        return dsrc

    def clear_dataset(self, source=[], dataset_id=[], hub_name=DEFAULT_HUB) -> str:
        """
            Clears one or more datasets of this Curate session from the Radiens hub.
            Use dataset_id='all' to clear all session datasets. 
            This is a power user function.

            Parameters:
                source (str, list) optional: data source file or list of data source files.
                dataset_id (str, list) optional: dataset ID or list of dataset IDs (default=[], 'all' clears all datasets for the Curate session)
                hub_name (str): radiens hub name (default=radiens.utils.constants.DEFAULT_HUB)

            Returns:
                dataset ids of data file(s) that were unlinked.

            See Also:
                :py:meth:`link_data_file()`
                :py:meth:`get_dataset_ids()`
        """
        if not isinstance(dataset_id, (list, str, Iterable)):
            raise ValueError('dataset_id must be string or list of strings')
        if isinstance(dataset_id, str):
            dataset_id = [dataset_id]
        if isinstance(source, (str, Path)):
            source = [Path(source)]
        _get_ids = []
        for _id in self.get_dataset_ids(hub_name):
            if len(dataset_id) > 0 and dataset_id[0] == 'all' and _id.find(self.id) > 0:
                _get_ids.append(_id)
            else:
                for req_id in dataset_id:
                    if req_id == _id:
                        _get_ids.append(_id)
            for src in source:
                if _id.find(Path(src).stem) > 0 and _id.find(self.id) > 0:
                    _get_ids.append(_id)
        return api_videre.unlink_datasource(self._server_address(hub_name, CORE_SERVICE), _get_ids)

    def get_dataset_ids(self, hub_name=DEFAULT_HUB) -> list:
        """
            Returns the list of dataset IDs on the Radiens hub.

            Returns:
                dataset_ids (list): linked dataset IDs on the Radiens hub.

            See Also:
                :py:meth:`link_data_file()`
                :py:meth:`clear_dataset()`
        """
        return api_videre.list_datasource_ids(self._server_address(hub_name, CORE_SERVICE))

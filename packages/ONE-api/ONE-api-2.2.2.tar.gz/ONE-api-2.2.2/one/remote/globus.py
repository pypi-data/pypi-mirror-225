"""A module for handling file operations through the Globus SDK.

Setup
-----

To set up Globus simply instantiate the `Globus` class for the first time and follow the prompts.
Providing a client name string to the constructor allows one to set up multiple Globus clients
(i.e. when switching between different Globus client IDs).

Examples
--------

Asynchronously transfer data between Alyx repositories

>>> alyx = AlyxClient()
>>> glo = Globus('admin')
>>> glo.add_endpoint('flatiron_cortexlab', alyx=alyx)
>>> glo.add_endpoint('cortex_lab_SR', alyx=alyx)
>>> task_id = glo.transfer_data('path/to/file', 'flatiron_cortexlab', 'cortex_lab_SR')

Synchronously transfer data to an alternate local location

>>> from functools import partial
>>> root_path = '/path/to/new/location'
>>> glo.add_endpoint(get_local_endpoint_id(), label='alternate_local', root_path=root_path)
>>> folder = 'camera/ZFM-01867/2021-03-23/002'  # An example folder to download
>>> task = partial(glo.transfer_data, folder, 'integration', 'integration_local',
...                label='alternate data', recursive=True)
>>> task_id = glo.run_task(task)  # Submit task to Globus and await completion

Temporarily change local data root path and synchronously download file

>>> glo.endpoints['local']['root_path'] = '/path/to/new/location'
>>> file = glo.download_file('path/to/file.ext', 'source_endpoint')
Path('/path/to/new/location/path/to/file.ext')
"""
import os
import re
import sys
import logging
from uuid import UUID
from pathlib import Path, PurePosixPath, PurePath, PureWindowsPath
import warnings
from functools import partial

import globus_sdk
from globus_sdk import TransferAPIError, GlobusAPIError, NetworkError, GlobusTimeoutError, \
    GlobusConnectionError, GlobusConnectionTimeoutError
from iblutil.io import params as iopar

from one.alf.spec import is_uuid
from one.alf.files import remove_uuid_string
import one.params
from one.webclient import AlyxClient
from one.util import ensure_list
from .base import DownloadClient, load_client_params, save_client_params

_logger = logging.getLogger(__name__)
CLIENT_KEY = 'globus'
DEFAULT_PAR = {'GLOBUS_CLIENT_ID': None, 'local_endpoint': None, 'local_path': None}


def setup(par_id=None):
    """
    Sets up Globus as a backend for ONE functions.
    In order to use this function you need:

    1. The Client ID of an existing Globus Client, or to create one
       (https://globus-sdk-python.readthedocs.io/en/stable/tutorial.html).
    2. Set up Global Connect on your local device (https://www.globus.org/globus-connect-personal).
    3. Register your local device as an Endpoint in your Globus Client (https://app.globus.org/).

    Parameters
    ----------
    par_id : str
        Parameter profile name to set up e.g. 'default', 'admin'.

    """

    print('Setting up Globus parameter file. See docstring for help.')
    if not par_id:
        default_par_id = 'default'
        par_id = input(
            f'Enter name for this client or press Enter to keep value "{default_par_id}": '
        )
        par_id = par_id.strip() or default_par_id

    # Read existing globus params if present
    globus_pars = iopar.as_dict(load_client_params(CLIENT_KEY, assert_present=False) or {})
    pars = {**DEFAULT_PAR, **globus_pars.get(par_id, {})}

    # Set GLOBUS_CLIENT_ID
    current_id = pars['GLOBUS_CLIENT_ID']
    if current_id:
        prompt = (f'Found Globus client ID in parameter file ({current_id}). '
                  'Press Enter to keep it, or enter a new ID here: ')
        pars['GLOBUS_CLIENT_ID'] = input(prompt).strip() or current_id
    else:
        new_id = input('Please enter the Globus client ID: ').strip()
        if not new_id:
            raise ValueError('Globus client ID is a required field')
        pars['GLOBUS_CLIENT_ID'] = new_id

    # Find and set local ID
    message = 'Please enter the local endpoint ID'
    try:
        default_endpoint = str(pars['local_endpoint'] or get_local_endpoint_id())
        message += f' (default: {default_endpoint})'
    except AssertionError:
        default_endpoint = ''
        warnings.warn(
            'Cannot find local endpoint ID. Beware that this might mean that Globus Connect '
            'is not set up properly.')
    pars['local_endpoint'] = input(message + ':').strip() or default_endpoint
    if not is_uuid(pars['local_endpoint'], (1, 2)):
        raise ValueError('Globus local endpoint ID must be a UUID version 1 or 2')

    # Check for local path
    message = 'Please enter the local endpoint path'
    local_path = pars['local_path'] or one.params.get(silent=True).CACHE_DIR
    message += f' (default: {local_path})'
    pars['local_path'] = input(message + ':').strip() or local_path

    # Log in manually and get refresh token to avoid having to login repeatedly
    client = globus_sdk.NativeAppAuthClient(pars['GLOBUS_CLIENT_ID'])
    client.oauth2_start_flow(refresh_tokens=True)
    authorize_url = client.oauth2_get_authorize_url()
    print('To get a new token, go to this URL and login: {0}'.format(authorize_url))
    auth_code = input('Enter the code you get after login here (press "c" to cancel): ').strip()
    if auth_code and auth_code.lower() != 'c':
        token_response = client.oauth2_exchange_code_for_tokens(auth_code)
        globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
        for par in ['refresh_token', 'access_token', 'expires_at_seconds']:
            pars[par] = globus_transfer_data[par]

    globus_pars[par_id] = pars
    save_client_params(globus_pars, client_key=CLIENT_KEY)
    print('Finished setup.')


def create_globus_client(client_name='default'):
    """
    Creates a Globus transfer client based on existing parameter file.

    Parameters
    ----------
    client_name : str
        Defines the parameter name to use (globus.client_name), e.g. 'default', 'admin'.

    Returns
    -------
    globus_sdk.TransferClient
        Globus transfer client instance
    """
    try:
        globus_pars = load_client_params(f'{CLIENT_KEY}.{client_name}')
    except (AttributeError, FileNotFoundError):
        setup(client_name)
        globus_pars = load_client_params(f'{CLIENT_KEY}.{client_name}', assert_present=False) or {}
    required_fields = {'refresh_token', 'GLOBUS_CLIENT_ID'}
    if not (globus_pars and required_fields.issubset(iopar.as_dict(globus_pars))):
        raise ValueError('No token in client parameter file. Run one.remote.globus.setup first')
    client = globus_sdk.NativeAppAuthClient(globus_pars.GLOBUS_CLIENT_ID)
    client.oauth2_start_flow(refresh_tokens=True)
    authorizer = globus_sdk.RefreshTokenAuthorizer(globus_pars.refresh_token, client)
    return globus_sdk.TransferClient(authorizer=authorizer)


def get_local_endpoint_id():
    """
    Extracts the ID of the local Globus Connect endpoint.

    Returns
    -------
    uuid.UUID
        The local Globus endpoint ID
    """
    msg = ('Cannot find local endpoint ID, check if Globus Connect is set up correctly, '
           '{} exists and contains a UUID.')
    if sys.platform in ('win32', 'cygwin'):
        id_path = Path(os.environ['LOCALAPPDATA']).joinpath('Globus Connect')
    else:
        id_path = Path.home().joinpath('.globusonline', 'lta')

    id_file = id_path.joinpath('client-id.txt')
    assert id_file.exists(), msg.format(id_file)
    local_id = id_file.read_text().strip()
    assert isinstance(local_id, str), msg.format(id_file)
    print(f'Found local endpoint ID in Globus Connect settings {local_id}')
    return UUID(local_id)


def get_local_endpoint_paths():
    """
    Extracts the local endpoint paths accessible by Globus Connect.  NB: This is only supported
    on Linux.

    Returns
    -------
    list of pathlib.Path
        Local endpoint paths set in Globus Connect.
    """
    if sys.platform in ('win32', 'cygwin'):
        print('On windows the local Globus path needs to be entered manually')
        return []
    else:
        path_file = Path.home().joinpath('.globusonline', 'lta', 'config-paths')
        if path_file.exists():
            local_paths = map(Path, filter(None, path_file.read_text().strip().split(',')))
            _logger.debug('Found local endpoint paths in Globus Connect settings')
        else:
            msg = ('Cannot find local endpoint path, check if Globus Connect is set up correctly, '
                   '{} exists and contains a valid path.')
            warnings.warn(msg.format(path_file))
            local_paths = []
        return list(local_paths)


def get_lab_from_endpoint_id(endpoint=None, alyx=None):
    """
    Extracts lab names associated with a given an endpoint UUID.

    Finds the lab names that are associated to data repositories with the provided Globus endpoint
    UUID.

    Parameters
    ----------
    endpoint : uuid.UUID, str
        Endpoint UUID, optional if not given will get attempt to find local endpoint UUID.
    alyx : one.webclient.AlyxClient
        An instance of AlyxClient to use.

    Returns
    -------
    list
        The lab names associated with the endpoint UUID.
    """

    alyx = alyx or AlyxClient(silent=True)
    if not endpoint:
        endpoint = get_local_endpoint_id()
    lab = alyx.rest('labs', 'list', django=f'repositories__globus_endpoint_id,{endpoint}')
    if len(lab):
        lab_names = [la['name'] for la in lab]
        return lab_names


def as_globus_path(path):
    """
    Convert a path into one suitable for the Globus TransferClient.

    Parameters
    ----------
    path : pathlib.Path, pathlib.PurePath, str
        A path to convert to a Globus-complient path string.

    Returns
    -------
    str
        A formatted path string.

    Notes
    -----
    - If using tilda in path, the home folder of your Globus Connect instance must be the same as
      the OS home dir.
    - If validating a path for another system ensure the input path is a PurePath, in particular,
      on a Linux computer a remote Windows should first be made into a PureWindowsPath.

    Examples
    --------
    A Windows path (on Windows OS)

    >>> as_globus_path('E:\\FlatIron\\integration')
    '/E/FlatIron/integration'

    When explicitly a POSIX path, remains unchanged

    >>> as_globus_path(PurePosixPath('E:\\FlatIron\\integration'))
    'E:\\FlatIron\\integration'

    A relative POSIX path (on *nix OS)

    >>> as_globus_path('../data/integration')
    '/mnt/data/integration'

    A valid Globus path remains unchanged

    >>> as_globus_path('/E/FlatIron/integration')
    '/E/FlatIron/integration'
    """
    is_pure_path = isinstance(path, PurePath)
    is_win = sys.platform in ('win32', 'cygwin') or isinstance(path, PureWindowsPath)
    if isinstance(path, str):
        path = Path(path)
    if (
        re.match(r'/[A-Z]($|/)', path.as_posix())
        if is_win
        else path.is_absolute()
    ):
        return path.as_posix()
    if not is_pure_path:
        path = path.resolve()
    if path.drive:
        path = '/' + str(path.as_posix().replace(':', '', 1))
    return str(path)


class Globus(DownloadClient):
    """Wrapper for managing files on Globus endpoints."""
    def __init__(self, client_name='default'):
        """
        Wrapper for managing files on Globus endpoints.

        Parameters
        ----------
        client_name : str
            Parameter profile name to load e.g. 'default', 'admin'.
        """
        # Setting up transfer client
        super().__init__()
        self.client = create_globus_client(client_name=client_name)
        self.pars = load_client_params(f'{CLIENT_KEY}.{client_name}')
        # Try adding local endpoint
        self.endpoints = {'local': {'id': UUID(self.pars.local_endpoint)}}
        _logger.info('Adding local endpoint.')
        self.endpoints['local']['root_path'] = self.pars.local_path

    def fetch_endpoints_from_alyx(self, alyx=None, overwrite=False):
        """
        Update endpoints property with Alyx Globus data repositories.

        Parameters
        ----------
        alyx : one.webclient.AlyxClient
            An optional AlyxClient.
        overwrite : bool
            Whether existing endpoint with the same label should be replaced.

        Returns
        -------
        dict
            The endpoints added from Alyx.
        """
        alyx = alyx or AlyxClient()
        alyx_endpoints = alyx.rest('data-repository', 'list')
        for endpoint in alyx_endpoints:
            if not endpoint['globus_endpoint_id']:
                continue
            uid = UUID(endpoint['globus_endpoint_id'])
            self.add_endpoint(
                uid, label=endpoint['name'], root_path=endpoint['globus_path'], overwrite=overwrite
            )
        endpoint_names = {e['name'] for e in alyx_endpoints}
        return {k: v for k, v in self.endpoints.items() if k in endpoint_names}

    def to_address(self, data_path, endpoint):
        """
        Get full path for a given endpoint.

        Parameters
        ----------
        data_path : Path, PurePath, str
            An absolute or relative POSIX path
        endpoint : str, uuid.UUID
            An endpoint label or UUID.

        Returns
        -------
        str
            A complete path string formatted for Globus.

        Examples
        --------
        >>> glo = Globus()
        >>> glo.add_endpoint('0ec47586-3a19-11eb-b173-0ee0d5d9299f',
        ...                  label='foobar', root_path='/foo')
        >>> glo.to_address('bar/baz.ext', 'foobar')
        '/foo/bar/baz.ext'
        """
        _, root_path = self._endpoint_id_root(endpoint)
        return self._endpoint_path(data_path, root_path)

    def download_file(self, file_address, source_endpoint, recursive=False, **kwargs):
        """
        Download one or more files via Globus.

        Parameters
        ----------
        file_address : str, list of str
            One or more relative POSIX paths to download.
        source_endpoint : str, uuid.UUID
            The source endpoint name or uuid.
        recursive : bool
            If true, transfer the contents of nested directories (NB: all data_paths must be
            directories).
        **kwargs
            See Globus.transfer_data.

        Returns
        -------
        pathlib.Path, list of pathlib.Path
            The downloaded file path(s). If recursive is True, a list is always returned.

        Notes
        -----
        - Assumes that the local endpoint root path is NOT POSIX style on Windows.

        TODO Return None for failed files

        Examples
        --------
        Download a single file

        >>> file = Globus().download_file('path/to/file', '0ec47586-3a19-11eb-b173-0ee0d5d9299f')

        Download multiple files and verify checksum

        >>> files = ['relative/file/path.ext', 'foo.bar']
        >>> files = Globus().download_file(files, 'source_endpoint_name', verify_checksum=True)

        Download a folder

        >>> files = Globus().download_file('folder/path', 'source_endpoint_name', recursive=True)
        """
        return_single = isinstance(file_address, str) and recursive is False
        kwargs['label'] = kwargs.get('label', 'ONE download')
        task = partial(self.transfer_data, file_address, source_endpoint, 'local',
                       sync_level='mtime', recursive=recursive, **kwargs)
        task_id = self.run_task(task)
        files = []
        root = Path(self.endpoints['local']['root_path'])
        idx = len(self._endpoint_path(PurePosixPath(as_globus_path(root))))
        for info in self.client.task_successful_transfers(task_id):
            files.append(info['destination_path'][idx:].strip('/'))

        if return_single:
            file = root / files[0]
            assert file.exists()
            return file

        # Order files by input
        def _best_match(x):
            """Return the index of the input file that best matches downloaded file."""
            spans = [len(frag) / len(x) if frag in x else 0 for frag in ensure_list(file_address)]
            return spans.index(max(spans))
        files = list(map(root.joinpath, sorted(files, key=_best_match)))
        assert all(map(Path.exists, filter(None, files)))
        return files

    @staticmethod
    def setup(client_name='default'):
        """
        Setup a Globus client.

        Parameters
        ----------
        client_name : str
            Parameter profile name to set up e.g. 'default', 'admin'.

        Returns
        -------
        Globus
            A new Globus client object.
        """
        setup(client_name)
        return Globus(client_name)

    def add_endpoint(self, endpoint, label=None, root_path=None, overwrite=False, alyx=None):
        """
        Add an endpoint to the Globus instance to be used by other functions.

        Parameters
        ----------
        endpoint : uuid.UUID, str
            The endpoint UUID or database repository name of the endpoint.
        label : str
            Label to access the endpoint. If endpoint is UUID this has to be set, otherwise is
            optional.
        root_path : str, pathlib.Path, pathlib.PurePath
            File path to be accessed by Globus on the endpoint.
        overwrite : bool
            Whether existing endpoint with the same label should be replaced.
        alyx : one.webclient.AlyxClient
            An AlyxClient instance for looking up repository information.
        """
        if is_uuid(endpoint, versions=(1, 2)):  # MAC address UUID
            if label is None:
                raise ValueError('If "endpoint" is a UUID, "label" cannot be None.')
            endpoint_id = self._ensure_uuid(endpoint)
        else:
            repo = self.repo_from_alyx(endpoint, alyx=alyx)
            endpoint_id = UUID(repo['globus_endpoint_id'])
            root_path = root_path or repo['globus_path']
            label = label or endpoint
        if label in self.endpoints.keys() and overwrite is False:
            _logger.error(f'An endpoint called "{label}" already exists. Choose a different label '
                          'or set overwrite=True')
        else:
            self.endpoints[label] = {'id': endpoint_id}
            if root_path:
                self.endpoints[label]['root_path'] = root_path

    @staticmethod
    def _endpoint_path(path, root_path=None):
        """
        Given an absolute path or relative path with a root path, return a Globus path str.

        Note: Paths must be POSIX or Globus-compliant paths.  In other words for Windows systems
        the input root_path or absolute path must be passed through `as_globus_path` before
        calling this method.

        TODO include globus_path_from_dataset

        Parameters
        ----------
        path : Path, PurePath, str
            An absolute or relative POSIX path
        root_path : Path, PurePath, str
            A root path to prepend.  Optional if `path` is absolute.

        Returns
        -------
        str
            A path string formatted for Globus.

        See Also
        --------
        as_globus_path

        Raises
        ------
        ValueError
            Path was not absolute and no root path was given.  An absolute path must start with
            a slash on *nix systems.
        """
        if isinstance(path, str):
            path = PurePosixPath(path)
        if root_path and not str(path).startswith(str(root_path)):
            path = PurePosixPath(root_path) / path
        if not path.is_absolute():
            raise ValueError(f'{path} is relative and no root_path defined')
        return as_globus_path(path)

    @staticmethod
    def _ensure_uuid(uid):
        """
        Ensures UUID object returned.

        Parameters
        ----------
        uid : str, uuid.UUID
            A UUID to cast to UUID object.

        Returns
        -------
        uuid.UUID
            A UUID object.
        """
        return UUID(uid) if not isinstance(uid, UUID) else uid

    def _endpoint_id_root(self, endpoint):
        """
        Return endpoint UUID and root path from a given endpoint identifier.

        Parameters
        ----------
        endpoint : str, uuid.UUID
            An endpoint label or UUID.

        Returns
        -------
        uuid.UUID
            The endpoint UUID.
        str, None
            The POSIX-style endpoint root path (if defined).

        Warnings
        --------
        UserWarning
            If endpoint UUID is associated with multiple root paths, it is better to provide the
            endpoint label to avoid this warning and to ensure the intended root path is returned.

        See Also
        --------
        Globus._sanitize_local
        """
        root_path = None
        if endpoint in self.endpoints.keys():
            endpoint_id = self.endpoints[endpoint]['id']
            if 'root_path' in self.endpoints[endpoint].keys():
                root_path = self.endpoints[endpoint]['root_path']
            return self._sanitize_local(endpoint_id, root_path)
        elif is_uuid(endpoint, range(1, 5)):
            # If a UUID was provided, find the first endpoint with a root path with the UUID
            endpoint_id = self._ensure_uuid(endpoint)
            matching = (
                k for k, v in self.endpoints.items() if v['id'] == endpoint_id and 'root_path' in v
            )
            if name := next(matching, None):
                # Warn of ambiguity if multiple endpoints share a UUID
                if next(matching, None) is not None:
                    warnings.warn(
                        f'Multiple endpoints added with the same UUID, '
                        f'using root path from "{name}"')
                root_path = self.endpoints[name]['root_path']
            else:
                root_path = None
            return self._sanitize_local(endpoint_id, root_path)
        else:
            raise ValueError(
                '"endpoint" must be a UUID or the label of an endpoint registered in this '
                'Globus instance. You can add endpoints via the add_endpoints method')

    def _sanitize_local(self, endpoint_id, root_path):
        """
        Ensure local root path on Windows is POSIX-style.

        Parameters
        ----------
        endpoint_id : uuid.UUID
            The endpoint UUID to determine if root path is local.
        root_path : pathlib.Path, str, None
            The root path to sanitize.

        Returns
        -------
        endpoint_id : uuid.UUID
            The endpoint UUID, returned unchanged to match `Globus._endpoint_id_root` signature.
        str, None
            The root path as a POSIX style string, or None if root_path is None.

        Examples
        --------
        Providing a local root path on Windows

        >>> glo = Globus()
        >>> uid = glo.endpoints['local']['id']
        >>> glo._sanitize_local(uid, 'C:\\Data')
        UUID('50282ed5-3124-11ee-b977-482ae33bf6ca'), '/C/Data'

        Path left unchanged on *nix systems or when endpoint ID is not local

        >>> uid = UUID('c7c46cec-3124-11ee-bf50-482ae33bf6ca')
        >>> glo._sanitize_local(uid, 'C:\\Data')
        UUID('c7c46cec-3124-11ee-bf50-482ae33bf6ca'), 'C:\\Data'
        """
        if not root_path:
            return endpoint_id, None
        # If the local root path is not explicitly a Windows Path and we're on windows, make sure
        # it's converted correctly to a POSIX style path
        if isinstance(root_path, str):
            is_win = sys.platform in ('win32', 'cygwin')
            if endpoint_id == self.endpoints['local']['id'] and is_win:
                root_path = PureWindowsPath(root_path)
            else:
                root_path = PurePosixPath(root_path)
        return endpoint_id, as_globus_path(root_path)

    def transfer_data(self, data_path, source_endpoint, destination_endpoint,
                      recursive=False, **kwargs):
        """
        Transfer one or more paths between endpoints.

        At least one of the endpoints must be a server endpoint.  Both file and directory paths may
        be provided, however if recursive is true, all paths must be directories.

        Parameters
        ----------
        data_path : str, list of str
            One or more data paths, relative to the endpoint root path.
        source_endpoint : str, uuid.UUID
            The name or UUID of the source endpoint.
        destination_endpoint : str, uuid.UUID
            The name or UUID of the destination endpoint.
        recursive : bool
            If true, transfer the contents of nested directories (NB: all data_paths must be
            directories).
        **kwargs
            See globus_sdk.TransferData.

        Returns
        -------
        uuid.UUID
            The Globus transfer ID.

        Examples
        --------
        Transfer two files (asynchronous)

        >>> glo = Globus()
        >>> files = ['file.ext', 'foo.bar']
        >>> task_id = glo.transfer_data(files, 'source_endpoint', 'destination_endpoint')

        Transfer a folder (asynchronous)

        >>> folder = 'path/to/folder'
        >>> task_id = glo.transfer_data(
        ...    folder, 'source_endpoint', 'destination_endpoint', recursive=True)
        """
        kwargs['source_endpoint'] = (source_endpoint
                                     if is_uuid(source_endpoint, versions=(1,))
                                     else self.endpoints.get(source_endpoint)['id'])
        kwargs['destination_endpoint'] = (destination_endpoint
                                          if is_uuid(destination_endpoint, versions=(1,))
                                          else self.endpoints.get(destination_endpoint)['id'])
        transfer_object = globus_sdk.TransferData(self.client, **kwargs)

        # add any number of items to the submission data
        for path in ensure_list(data_path):
            src = self._endpoint_path(path, self._endpoint_id_root(source_endpoint)[1])
            dst = self._endpoint_path(path, self._endpoint_id_root(destination_endpoint)[1])
            transfer_object.add_item(src, dst, recursive=recursive)
        response = self.client.submit_transfer(transfer_object)
        return UUID(response.data['task_id'])

    def ls(self, endpoint, path, remove_uuid=False, return_size=False, max_retries=1):
        """
        Return the list of (filename, filesize) in a given endpoint directory.
        NB: If you're using ls routinely when transferring or deleting files you're probably doing
        something wrong!

        Parameters
        ----------
        endpoint : uuid.UUID, str
            The Globus endpoint. May be a UUID or a key in the Globus.endpoints attribute.
        path : Path, PurePath, str
            The absolute or relative Globus path to list.  Note: if endpoint is a UUID, the path
            must be absolute.
        remove_uuid : bool
            If True, remove the UUID from the returned filenames.
        return_size : bool
            If True, return the size of each listed file in bytes.

        Returns
        -------
        list
            A list of PurePosixPath objects of the files and folders listed, or if return_size is
            True, tuples of PurePosixPath objects and the corresponding file sizes.
        """
        # Check if endpoint is a UUID, if not try to get UUID from registered endpoints
        endpoint_id, root_path = self._endpoint_id_root(endpoint)
        # Check if root_path should be added and if path is absolute
        path = self._endpoint_path(path, root_path)
        # Do the actual listing
        out = []
        response = []
        for i in range(max_retries + 1):
            try:
                response = self.client.operation_ls(endpoint_id, path=path)
                break
            except (GlobusConnectionError, GlobusAPIError) as ex:
                if i == max_retries:
                    raise ex
        for entry in response:
            fn = PurePosixPath(remove_uuid_string(entry['name']) if remove_uuid else entry['name'])
            if return_size:
                size = entry['size'] if entry['type'] == 'file' else None
                out.append((fn, size))
            else:
                out.append(fn)

        return out

    # TODO: allow to move all content of a directory with 'recursive' keyword in add_item
    def mv(self, source_endpoint, target_endpoint, source_paths, target_paths,
           timeout=None, **kwargs):
        """
        Move files from one endpoint to another.

        Parameters
        ----------
        source_endpoint : uuid.UUID, str
            The Globus source endpoint. May be a UUID or a key in the Globus.endpoints attribute.
        target_endpoint : uuid.UUID, str
            The Globus destination endpoint. May be a UUID or a key in the Globus.endpoints
            attribute.
        source_paths : list of str, Path or PurePath
            The absolute or relative Globus paths of source files to moves.  Note: if endpoint is
            a UUID, the path must be absolute.
        target_paths : list of str, Path or PurePath
            The absolute or relative Globus paths of destination files to moves.  Note: if endpoint
            is a UUID, the path must be absolute.
        timeout : int
            Maximum time in seconds to wait for the task to complete.
        kwargs
            Optional arguments for globus_sdk.TransferData.

        Returns
        -------
        uuid.UUID
            A Globus task ID.
        """
        source_endpoint, source_root = self._endpoint_id_root(source_endpoint)
        target_endpoint, target_root = self._endpoint_id_root(target_endpoint)
        source_paths = [str(self._endpoint_path(path, source_root)) for path in source_paths]
        target_paths = [str(self._endpoint_path(path, target_root)) for path in target_paths]

        tdata = globus_sdk.TransferData(self.client, source_endpoint, target_endpoint,
                                        verify_checksum=True, sync_level='checksum',
                                        label='ONE globus', **kwargs)
        for source_path, target_path in zip(source_paths, target_paths):
            tdata.add_item(source_path, target_path)

        def wrapper():
            """Function to submit Globus transfer and return the resulting task ID"""
            response = self.client.submit_transfer(tdata)
            task_id = response.get('task_id', None)
            return task_id

        return self.run_task(wrapper, timeout=timeout)

    def run_task(self, globus_func, retries=3, timeout=None):
        """
        Block until a Globus task finishes and retry upon Network or REST Errors.
        globus_func needs to submit a task to the client and return a task_id.

        Parameters
        ----------
        globus_func : function, Callable
            A function that returns a Globus task ID, typically it will submit a transfer.
        retries : int
            The number of times to call globus_func if it raises a Globus error.
        timeout : int
            Maximum time in seconds to wait for the task to complete.

        Returns
        -------
        uuid.UUID
            Globus task ID.

        Raises
        ------
        IOError
            Timed out waiting for task to complete.

        TODO Add a quick fail option that returns when files missing, etc.
        """
        try:
            task_id = globus_func()
            assert is_uuid(task_id, versions=(1, 2)), 'invalid UUID returned'
            print(f'Waiting for Globus task {task_id} to complete')
            # While the task with task is active, print a dot every second. Timeout after timeout
            i = 0
            while not self.client.task_wait(task_id, timeout=5, polling_interval=1):
                print('.', end='')
                i += 1
                if timeout and i >= timeout:
                    task = self.client.get_task(task_id)
                    raise IOError(f'Globus task {task_id} timed out after {timeout} seconds, '
                                  f'with task status {task["status"]}')
            task = self.client.get_task(task_id)
            if task['status'] == 'SUCCEEDED':
                # Sometime Globus sets the status to SUCCEEDED but doesn't truly finish.
                # Handle error thrown when querying task_successful_transfers too early
                try:
                    successful = self.client.task_successful_transfers(task_id)
                    skipped = self.client.task_skipped_errors(task_id)
                    print(f'\nGlobus task {task_id} completed.'
                          f'\nSkipped transfers: {len(list(skipped))}'
                          f'\nSuccessful transfers: {len(list(successful))}')
                    for info in successful:
                        _logger.debug(f'{info["source_path"]} -> {info["destination_path"]}')
                except TransferAPIError:
                    _logger.warning(f'\nGlobus task {task_id} SUCCEEDED but querying transfers was'
                                    f'unsuccessful')
            else:
                raise IOError(f'Globus task finished unsuccessfully with status {task["status"]}')
            return self._ensure_uuid(task_id)
        except (GlobusAPIError, NetworkError, GlobusTimeoutError, GlobusConnectionError,
                GlobusConnectionTimeoutError) as e:
            if retries < 1:
                _logger.error('\nMax retries exceeded.')
                raise e
            else:
                _logger.debug('\nGlobus experienced a network error', exc_info=True)
                # if we reach this point without returning or erring, retry
                _logger.warning('\nGlobus experienced a network error, retrying.')
                self.run_task(globus_func, retries=(retries - 1), timeout=timeout)

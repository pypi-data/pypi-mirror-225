"""Official Python client for Driverless AI."""

import enum
import importlib
import json
import pathlib
import re
import warnings
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import TYPE_CHECKING
from typing import Union

import requests

from driverlessai import __version__
from driverlessai import _admin
from driverlessai import _autoviz
from driverlessai import _datasets
from driverlessai import _experiments
from driverlessai import _mli
from driverlessai import _model_diagnostics
from driverlessai import _projects
from driverlessai import _recipes
from driverlessai import _server
from driverlessai import _utils


if TYPE_CHECKING:
    import fsspec  # noqa F401


###############################
# Custom Exceptions
###############################


# If we're not able to communicate with the DAI
# server, this exception is thrown.
class ServerDownException(_utils.ClientException):
    pass


class ServerLicenseInvalid(_utils.ClientException):
    pass


class ServerVersionExtractionFailed(_utils.ClientException):
    pass


class ServerVersionNotSupported(_utils.ClientException):
    pass


###############################
# Helper Functions
###############################


def is_server_up(
    address: str, timeout: int = 10, verify: Union[bool, str] = False
) -> bool:
    """Checks if a Driverless AI server is running.

    Args:
        address: full URL of the Driverless AI server to connect to
        timeout: timeout if the server has not issued a response in this many seconds
        verify: when using https on the Driverless AI server, setting this to
            False will disable SSL certificates verification. A path to
            cert(s) can also be passed to verify, see:
            https://requests.readthedocs.io/en/master/user/advanced/#ssl-cert-verification

    Examples::

        driverlessai.is_server_up(
            address='http://localhost:12345',
        )
    """
    try:
        return requests.get(address, timeout=timeout, verify=verify).status_code == 200
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return False


###############################
# DAI Python Client
###############################


class DownloadType(str, enum.Enum):
    """Used to determine what type of resources to download"""

    FILES = "files"
    DATASETS = "datasets_files"
    LOGS = "log_files"


class Client:
    """Connect to and interact with a Driverless AI server.

    Args:
        address: full URL of the Driverless AI server to connect to
        username: username for authentication on the Driverless AI server
        password: password for authentication on the Driverless AI server
        token_provider: callable that provides an authentication token,
            if provided, will ignore ``username`` and ``password`` values
        verify: when using https on the Driverless AI server, setting this to
            False will disable SSL certificates verification. A path to
            cert(s) can also be passed to verify, see:
            https://requests.readthedocs.io/en/master/user/advanced/#ssl-cert-verification
        backend_version_override: version of client backend to use, overrides
            Driverless AI server version detection. Specify ``"latest"`` to get
            the most recent backend supported. In most cases the user should
            rely on Driverless AI server version detection and leave this as
            the default ``None``.

    Examples::

        ### Connect with username and password
        dai = driverlessai.Client(
            address='http://localhost:12345',
            username='py',
            password='py'
        )

        ### Connect with token (assumes the Driverless AI server is configured
        ### to allow clients to authenticate through tokens)

        # 1) setup a token provider with a refresh token from the Driverless AI web UI
        token_provider = driverlessai.token_providers.OAuth2TokenProvider(
            refresh_token="eyJhbGciOiJIUzI1N...",
            client_id="python_client",
            token_endpoint_url="https://keycloak-server/auth/realms/..."
            token_introspection_url="https://keycloak-server/auth/realms/..."
        )

        # 2) use the token provider to get authorization to connect to the
        # Driverless AI server
        dai = driverlessai.Client(
            address="https://localhost:12345",
            token_provider=token_provider.ensure_fresh_token
        )
    """

    def __init__(
        self,
        address: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token_provider: Optional[Callable[[], str]] = None,
        verify: Union[bool, str] = True,
        backend_version_override: Optional[str] = None,
    ) -> None:

        address = address.rstrip("/")

        # Check if the server is up, if we're unable to ping it we fail.
        if not is_server_up(address, verify=verify):
            if address.startswith("https"):
                raise ServerDownException(
                    "Unable to communicate with Driverless AI server. "
                    "Please make sure the server is running, "
                    "the address is correct, and `verify` is specified."
                )
            raise ServerDownException(
                "Unable to communicate with Driverless AI server. "
                "Please make sure the server is running and the address is correct."
            )

        # Try to get server version, if we can't we fail.
        if backend_version_override is None:
            server_version = self._detect_server_version(address, verify)
        else:
            if backend_version_override == "latest":
                backend_version_override = re.search("[0-9.]+", __version__)[0].rstrip(
                    "."
                )
            server_version = backend_version_override

        # Import backend that matches server version, if we can't we fail.
        server_module_path = (
            f"driverlessai._h2oai_client_{server_version.replace('.', '_')}"
        )
        try:
            self._server_module: Any = importlib.import_module(server_module_path)
        except ModuleNotFoundError:
            raise ServerVersionNotSupported(
                f"Server version {server_version} is not supported, "
                "try updating to the latest client."
            )

        if server_version[:3] == "1.8":
            warnings.warn(
                "Support for version 1.8.x will be removed in the next release \
                (1.10.6). Please upgrade to a newer version to ensure \
                compatibility and continued support. If you have any concerns or \
                questions, please contact our support team for assistance.",
                DeprecationWarning,
                stacklevel=2,
            )

        self._backend = self._server_module.protocol.Client(
            address=address,
            username=username,
            password=password,
            token_provider=token_provider,
            verify=verify,
        )
        if server_version[:3] == "1.8":
            self._gui_sep = "/#"
        else:
            self._gui_sep = "/#/"
        self._server = _server.Server(
            client=self,
            address=address,
        )
        self._autoviz = _autoviz.AutoViz(self)
        self._admin = _admin.Admin(self)
        self._connectors = _datasets.Connectors(self)
        self._datasets = _datasets.Datasets(self)
        self._experiments = _experiments.Experiments(self)
        self._mli = _mli.MLI(self)
        self._model_diagnostics = _model_diagnostics.ModelDiagnostics(self)
        self._projects = _projects.Projects(self)
        self._recipes = _recipes.Recipes(self)

        if not self.server.license.is_valid():
            raise ServerLicenseInvalid(self._backend.have_valid_license().message)

        # retry patch for connection issues
        if hasattr(self._backend, "_session"):
            from urllib3.util.retry import Retry

            retries = Retry(
                total=5,
                backoff_factor=0.2,
                status_forcelist=[403, 500, 502, 503, 504],
                allowed_methods=["POST"],
            )

            self._backend._session.mount(
                "http://", requests.adapters.HTTPAdapter(max_retries=retries)
            )
            self._backend._session.mount(
                "https://", requests.adapters.HTTPAdapter(max_retries=retries)
            )

        # Better error handling for versions older than 1.10.5
        if (
            hasattr(self._backend, "_session")
            and hasattr(self._backend, "_get_authorization_headers")
            and _utils.is_server_version_less_than(self, "1.10.5")
        ):
            RequestError = self._server_module.protocol.RequestError
            RemoteError = self._server_module.protocol.RemoteError

            def _request(self, method: str, params: dict) -> Any:  # type: ignore
                self._cid = self._cid + 1
                req = json.dumps(
                    dict(id=self._cid, method="api_" + method, params=params)
                )
                res = self._session.post(
                    self.address + "/rpc",
                    data=req,
                    headers=self._get_authorization_headers(),
                )
                try:
                    res.raise_for_status()
                except requests.HTTPError as e:
                    msg = f"Driverless AI server responded with {res.status_code}."
                    print(f"[ERROR] {msg}\n\n{res.content}")
                    raise RequestError(msg) from e

                try:
                    response = res.json()
                except json.JSONDecodeError as e:
                    msg = "Driverless AI server response is not a valid JSON."
                    print(f"[ERROR] {msg}\n\n{res.content}")
                    raise RequestError(msg) from e

                if "error" in response:
                    raise RemoteError(response["error"])

                return response["result"]

            self._server_module.protocol.Client._request = _request

    @property
    def admin(self) -> _admin.Admin:
        """Performs administrative tasks on Driverless AI server.
        Admin API is not supported for Driverless AI version < 1.10.3"""
        _utils.check_server_support(self, "1.10.3", "Admin API")
        return self._admin

    @property
    def autoviz(self) -> _autoviz.AutoViz:
        """Interact with dataset visualizations on the Driverless AI server."""
        return self._autoviz

    @property
    def connectors(self) -> _datasets.Connectors:
        """Interact with connectors on the Driverless AI server."""
        return self._connectors

    @property
    def datasets(self) -> _datasets.Datasets:
        """Interact with datasets on the Driverless AI server."""
        return self._datasets

    @property
    def experiments(self) -> _experiments.Experiments:
        """Interact with experiments on the Driverless AI server."""
        return self._experiments

    @property
    def mli(self) -> _mli.MLI:
        """Interact with experiment interpretations on the Driverless AI server."""
        return self._mli

    @property
    def model_diagnostics(self) -> _model_diagnostics.ModelDiagnostics:
        """Interact with model diagnostics on the Driverless AI server."""
        return self._model_diagnostics

    @property
    def projects(self) -> _projects.Projects:
        """Interact with projects on the Driverless AI server."""
        return self._projects

    @property
    def recipes(self) -> _recipes.Recipes:
        """Interact with recipes on the Driverless AI server."""
        return self._recipes

    @property
    def server(self) -> _server.Server:
        """Get information about the Driverless AI server."""
        return self._server

    def __repr__(self) -> str:
        return f"{self.__class__} {self!s}"

    def __str__(self) -> str:
        return self.server.address

    @staticmethod
    def _detect_server_version(address: str, verify: Union[bool, str]) -> str:
        """Trys multiple methods to retrieve server version."""
        # query server version endpoint
        response = requests.get(f"{address}/serverversion", verify=verify)
        if response.status_code == 200:
            try:
                return response.json()["serverVersion"]
            except json.JSONDecodeError:
                pass
        # extract the version by scraping the login page
        response = requests.get(address, verify=verify)
        scrapings = re.search("DRIVERLESS AI ([0-9.]+)", response.text)
        if scrapings:
            return scrapings[1]
        # if login is disabled, get cookie and make rpc call
        with requests.Session() as s:
            s.get(f"{address}/login", verify=verify)
            response = s.post(
                f"{address}/rpc",
                data=json.dumps(
                    {"id": "", "method": "api_get_app_version", "params": {}}
                ),
            )
            try:
                return response.json()["result"]["version"]
            except json.JSONDecodeError:
                pass
        # fail
        raise ServerVersionExtractionFailed(
            "Unable to extract server version. "
            "Please make sure the address is correct."
        )

    def _download(
        self,
        server_path: str,
        dst_dir: str,
        dst_file: Optional[str] = None,
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
        timeout: float = 30,
        verbose: bool = True,
        download_type: DownloadType = DownloadType.FILES,
    ) -> str:
        """Download a file from the user's files on the Driverless AI server -
        assuming you know the path.

        Args:
            server_path: path to user's file
            dst_dir: directory where file will be saved
            dst_file: file to be saved to
            file_system: FSSPEC based file system to download to,
                instead of local file system
            overwrite: overwrite existing files
            timeout: seconds to wait for server to respond before throwing error
            verbose: whether to print messages about download status
            download_type: download type, whether to choose from a file, dataset, or log
        """
        if not dst_file:
            dst_file = pathlib.Path(server_path).name
        dst_path = str(pathlib.Path(dst_dir, dst_file))
        res = self._get_file(server_path, timeout, download_type=download_type)
        try:
            if file_system is None:
                if overwrite:
                    mode = "wb"
                else:
                    mode = "xb"
                with open(dst_path, mode) as f:
                    f.write(res.content)
                if verbose:
                    print(f"Downloaded '{dst_path}'")
            else:
                if not overwrite and file_system.exists(dst_path):
                    raise FileExistsError(f"File exists: {dst_path}")
                with file_system.open(dst_path, "wb") as f:
                    f.write(res.content)
                if verbose:
                    print(f"Downloaded '{dst_path}' to {file_system}")
        except FileExistsError:
            print(f"{dst_path} already exists. Use `overwrite` to force download.")
            raise

        return dst_path

    def _get_file(
        self,
        server_path: str,
        timeout: float = 5,
        download_type: DownloadType = DownloadType.FILES,
    ) -> requests.models.Response:
        """Retrieve a requests response for any file from the user's files on
        the Driverless AI server - assuming you know the path.

        Args:
            server_path: path to user's file
            timeout: seconds to wait for server to respond before throwing error
            download_type: download type, whether to choose from a file, dataset, or log
        """
        if _utils.is_server_version_less_than(self, "1.10.5"):
            # the different types of downloads were only introduced in 1.10.5
            download_type = DownloadType.FILES

        url = f"{self.server.address}/{download_type.value}/{server_path}"
        if hasattr(self._backend, "_session") and hasattr(
            self._backend, "_get_authorization_headers"
        ):
            res = self._backend._session.get(
                url,
                headers=self._backend._get_authorization_headers(),
                timeout=timeout,
            )
        elif hasattr(self._backend, "_session"):
            res = self._backend._session.get(url, timeout=timeout)
        else:
            res = requests.get(
                url,
                cookies=self._backend._cookies,
                verify=self._backend._verify,
                timeout=timeout,
            )
        res.raise_for_status()
        return res

    def _get_json_file(self, server_path: str, timeout: float = 5) -> Dict[Any, Any]:
        """Retrieve a dictionary representation of a json file from the user's
        files on the Driverless AI server - assuming you know the path.

        Args:
            server_path: path to user's file
            timeout: seconds to wait for server to respond before throwing error
        """
        return self._get_file(server_path, timeout).json()

    def _get_text_file(self, server_path: str, timeout: float = 5) -> str:
        """Retrieve a string representation of a text based file from the user's
        files on the Driverless AI server - assuming you know the path.

        Args:
            server_path: path to user's file
            timeout: seconds to wait for server to respond before throwing error
        """
        return self._get_file(server_path, timeout).text

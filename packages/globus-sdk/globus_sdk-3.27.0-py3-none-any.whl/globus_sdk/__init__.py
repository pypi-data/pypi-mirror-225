# isort:skip_file
# fmt:off
#
# this __init__.py file is generated by _generate_init.py
# do not edit it directly or testing will fail
import importlib
import logging
import sys
import typing as t

from .version import __version__


def _force_eager_imports() -> None:
    current_module = sys.modules[__name__]

    for attribute_set in _LAZY_IMPORT_TABLE.values():
        for attr in attribute_set:
            getattr(current_module, attr)


_LAZY_IMPORT_TABLE = {
    "authorizers": {
        "AccessTokenAuthorizer",
        "BasicAuthorizer",
        "ClientCredentialsAuthorizer",
        "NullAuthorizer",
        "RefreshTokenAuthorizer",
    },
    "client": {
        "BaseClient",
    },
    "exc": {
        "GlobusAPIError",
        "ErrorSubdocument",
        "GlobusConnectionError",
        "GlobusConnectionTimeoutError",
        "GlobusError",
        "GlobusSDKUsageError",
        "GlobusTimeoutError",
        "NetworkError",
        "RemovedInV4Warning",
    },
    "local_endpoint": {
        "GlobusConnectPersonalOwnerInfo",
        "LocalGlobusConnectPersonal",
        "LocalGlobusConnectServer",
    },
    "response": {
        "GlobusHTTPResponse",
        "IterableResponse",
        "ArrayResponse",
    },
    "services.auth": {
        "AuthAPIError",
        "AuthClient",
        "ConfidentialAppAuthClient",
        "IdentityMap",
        "NativeAppAuthClient",
        "GetIdentitiesResponse",
        "OAuthDependentTokenResponse",
        "OAuthTokenResponse",
    },
    "services.gcs": {
        "CollectionDocument",
        "GCSAPIError",
        "GCSClient",
        "GCSRoleDocument",
        "GuestCollectionDocument",
        "MappedCollectionDocument",
        "CollectionPolicies",
        "POSIXCollectionPolicies",
        "POSIXStagingCollectionPolicies",
        "GoogleCloudStorageCollectionPolicies",
        "StorageGatewayDocument",
        "StorageGatewayPolicies",
        "POSIXStoragePolicies",
        "POSIXStagingStoragePolicies",
        "BlackPearlStoragePolicies",
        "BoxStoragePolicies",
        "CephStoragePolicies",
        "GoogleDriveStoragePolicies",
        "GoogleCloudStoragePolicies",
        "OneDriveStoragePolicies",
        "AzureBlobStoragePolicies",
        "S3StoragePolicies",
        "ActiveScaleStoragePolicies",
        "IrodsStoragePolicies",
        "HPSSStoragePolicies",
        "UserCredentialDocument",
    },
    "services.flows": {
        "FlowsClient",
        "FlowsAPIError",
        "IterableFlowsResponse",
        "SpecificFlowClient",
    },
    "services.groups": {
        "BatchMembershipActions",
        "GroupMemberVisibility",
        "GroupPolicies",
        "GroupRequiredSignupFields",
        "GroupRole",
        "GroupsAPIError",
        "GroupsClient",
        "GroupsManager",
        "GroupVisibility",
    },
    "services.search": {
        "SearchAPIError",
        "SearchClient",
        "SearchQuery",
        "SearchScrollQuery",
    },
    "services.timer": {
        "TimerAPIError",
        "TimerClient",
        "TimerJob",
    },
    "services.transfer": {
        "ActivationRequirementsResponse",
        "DeleteData",
        "IterableTransferResponse",
        "TransferAPIError",
        "TransferClient",
        "TransferData",
    },
}

if t.TYPE_CHECKING:
    from .authorizers import AccessTokenAuthorizer
    from .authorizers import BasicAuthorizer
    from .authorizers import ClientCredentialsAuthorizer
    from .authorizers import NullAuthorizer
    from .authorizers import RefreshTokenAuthorizer
    from .client import BaseClient
    from .exc import GlobusAPIError
    from .exc import ErrorSubdocument
    from .exc import GlobusConnectionError
    from .exc import GlobusConnectionTimeoutError
    from .exc import GlobusError
    from .exc import GlobusSDKUsageError
    from .exc import GlobusTimeoutError
    from .exc import NetworkError
    from .exc import RemovedInV4Warning
    from .local_endpoint import GlobusConnectPersonalOwnerInfo
    from .local_endpoint import LocalGlobusConnectPersonal
    from .local_endpoint import LocalGlobusConnectServer
    from .response import GlobusHTTPResponse
    from .response import IterableResponse
    from .response import ArrayResponse
    from .services.auth import AuthAPIError
    from .services.auth import AuthClient
    from .services.auth import ConfidentialAppAuthClient
    from .services.auth import IdentityMap
    from .services.auth import NativeAppAuthClient
    from .services.auth import GetIdentitiesResponse
    from .services.auth import OAuthDependentTokenResponse
    from .services.auth import OAuthTokenResponse
    from .services.gcs import CollectionDocument
    from .services.gcs import GCSAPIError
    from .services.gcs import GCSClient
    from .services.gcs import GCSRoleDocument
    from .services.gcs import GuestCollectionDocument
    from .services.gcs import MappedCollectionDocument
    from .services.gcs import CollectionPolicies
    from .services.gcs import POSIXCollectionPolicies
    from .services.gcs import POSIXStagingCollectionPolicies
    from .services.gcs import GoogleCloudStorageCollectionPolicies
    from .services.gcs import StorageGatewayDocument
    from .services.gcs import StorageGatewayPolicies
    from .services.gcs import POSIXStoragePolicies
    from .services.gcs import POSIXStagingStoragePolicies
    from .services.gcs import BlackPearlStoragePolicies
    from .services.gcs import BoxStoragePolicies
    from .services.gcs import CephStoragePolicies
    from .services.gcs import GoogleDriveStoragePolicies
    from .services.gcs import GoogleCloudStoragePolicies
    from .services.gcs import OneDriveStoragePolicies
    from .services.gcs import AzureBlobStoragePolicies
    from .services.gcs import S3StoragePolicies
    from .services.gcs import ActiveScaleStoragePolicies
    from .services.gcs import IrodsStoragePolicies
    from .services.gcs import HPSSStoragePolicies
    from .services.gcs import UserCredentialDocument
    from .services.flows import FlowsClient
    from .services.flows import FlowsAPIError
    from .services.flows import IterableFlowsResponse
    from .services.flows import SpecificFlowClient
    from .services.groups import BatchMembershipActions
    from .services.groups import GroupMemberVisibility
    from .services.groups import GroupPolicies
    from .services.groups import GroupRequiredSignupFields
    from .services.groups import GroupRole
    from .services.groups import GroupsAPIError
    from .services.groups import GroupsClient
    from .services.groups import GroupsManager
    from .services.groups import GroupVisibility
    from .services.search import SearchAPIError
    from .services.search import SearchClient
    from .services.search import SearchQuery
    from .services.search import SearchScrollQuery
    from .services.timer import TimerAPIError
    from .services.timer import TimerClient
    from .services.timer import TimerJob
    from .services.transfer import ActivationRequirementsResponse
    from .services.transfer import DeleteData
    from .services.transfer import IterableTransferResponse
    from .services.transfer import TransferAPIError
    from .services.transfer import TransferClient
    from .services.transfer import TransferData


def __dir__() -> t.List[str]:
    # dir(globus_sdk) should include everything exported in __all__
    # as well as some explicitly selected attributes from the default dir() output
    # on a module
    #
    # see also:
    # https://discuss.python.org/t/how-to-properly-extend-standard-dir-search-with-module-level-dir/4202
    return list(__all__) + [
        # __all__ itself can be inspected
        "__all__",
        # useful to figure out where a package is installed
        "__file__",
        "__path__",
    ]


def __getattr__(name: str) -> t.Any:
    for modname, items in _LAZY_IMPORT_TABLE.items():
        if name in items:
            mod = importlib.import_module("." + modname, __name__)
            value = getattr(mod, name)
            setattr(sys.modules[__name__], name, value)
            return value

    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = (
    "__version__",
    "_force_eager_imports",
    "AccessTokenAuthorizer",
    "ActivationRequirementsResponse",
    "ActiveScaleStoragePolicies",
    "ArrayResponse",
    "AuthAPIError",
    "AuthClient",
    "AzureBlobStoragePolicies",
    "BaseClient",
    "BasicAuthorizer",
    "BatchMembershipActions",
    "BlackPearlStoragePolicies",
    "BoxStoragePolicies",
    "CephStoragePolicies",
    "ClientCredentialsAuthorizer",
    "CollectionDocument",
    "CollectionPolicies",
    "ConfidentialAppAuthClient",
    "DeleteData",
    "ErrorSubdocument",
    "FlowsAPIError",
    "FlowsClient",
    "GCSAPIError",
    "GCSClient",
    "GCSRoleDocument",
    "GetIdentitiesResponse",
    "GlobusAPIError",
    "GlobusConnectPersonalOwnerInfo",
    "GlobusConnectionError",
    "GlobusConnectionTimeoutError",
    "GlobusError",
    "GlobusHTTPResponse",
    "GlobusSDKUsageError",
    "GlobusTimeoutError",
    "GoogleCloudStorageCollectionPolicies",
    "GoogleCloudStoragePolicies",
    "GoogleDriveStoragePolicies",
    "GroupMemberVisibility",
    "GroupPolicies",
    "GroupRequiredSignupFields",
    "GroupRole",
    "GroupVisibility",
    "GroupsAPIError",
    "GroupsClient",
    "GroupsManager",
    "GuestCollectionDocument",
    "HPSSStoragePolicies",
    "IdentityMap",
    "IrodsStoragePolicies",
    "IterableFlowsResponse",
    "IterableResponse",
    "IterableTransferResponse",
    "LocalGlobusConnectPersonal",
    "LocalGlobusConnectServer",
    "MappedCollectionDocument",
    "NativeAppAuthClient",
    "NetworkError",
    "NullAuthorizer",
    "OAuthDependentTokenResponse",
    "OAuthTokenResponse",
    "OneDriveStoragePolicies",
    "POSIXCollectionPolicies",
    "POSIXStagingCollectionPolicies",
    "POSIXStagingStoragePolicies",
    "POSIXStoragePolicies",
    "RefreshTokenAuthorizer",
    "RemovedInV4Warning",
    "S3StoragePolicies",
    "SearchAPIError",
    "SearchClient",
    "SearchQuery",
    "SearchScrollQuery",
    "SpecificFlowClient",
    "StorageGatewayDocument",
    "StorageGatewayPolicies",
    "TimerAPIError",
    "TimerClient",
    "TimerJob",
    "TransferAPIError",
    "TransferClient",
    "TransferData",
    "UserCredentialDocument",
)


# configure logging for a library, per python best practices:
# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger("globus_sdk").addHandler(logging.NullHandler())

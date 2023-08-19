from .azure_pomes import (
    AZURE_CONNECTION_STRING, AZURE_STORAGE_BUCKET,
    azure_verify, azure_blob_exists, azure_blob_retrieve,
    azure_blob_store, azure_blob_delete, azure_blob_get_mimetype,
)

__all__ = [
    # azure_pomes
    "AZURE_CONNECTION_STRING", "AZURE_STORAGE_BUCKET",
    "azure_verify", "azure_blob_exists", "azure_blob_retrieve",
    "azure_blob_store", "azure_blob_delete", "azure_blob_get_mimetype",
]

from importlib.metadata import version
__version__ = version("pypomes_cloud")
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())

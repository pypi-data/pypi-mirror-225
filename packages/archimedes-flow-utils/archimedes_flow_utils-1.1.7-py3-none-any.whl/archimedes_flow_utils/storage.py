from functools import partial
from io import BytesIO

from azure.storage.blob import BlobClient

from .logger import logger


class AzureStorage:
    def __init__(self, azure_storage_account_name, azure_storage_account_key):
        self.blob_client = partial(
            BlobClient.from_connection_string,
            conn_str=self._get_azure_connection_string(
                azure_storage_account_name, azure_storage_account_key
            ),
            timeout=120,
        )

    def read(self, container_name, blob_name):
        download_stream = self.blob_client(
            container_name=container_name, blob_name=blob_name
        ).download_blob()
        data_text = download_stream.readall()
        return data_text

    def store(
        self,
        container_name: str,
        blob_name: str,
        contents: BytesIO,
        overwrite: bool = False,
    ):
        logger.info(
            f"Writing blob '{blob_name}' to container '{container_name}' ({contents.getbuffer().nbytes} bytes)"
        )

        file_info = self.blob_client(
            container_name=container_name, blob_name=blob_name
        ).upload_blob(
            data=contents,
            overwrite=overwrite,
        )

        etag = file_info["etag"]
        logger.info(f"Stored with etag {etag}")

    @staticmethod
    def _get_azure_connection_string(
        azure_storage_account_name, azure_storage_account_key
    ):
        """
        Return the connection string used to connect to Azure
        """

        return ";".join(
            [
                "DefaultEndpointsProtocol=https",
                f"AccountName={azure_storage_account_name}",
                f"AccountKey={azure_storage_account_key}",
                "EndpointSuffix=core.windows.net",
            ]
        )

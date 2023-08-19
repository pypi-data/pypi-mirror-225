import io
import sys
from azure.storage.blob import BlobClient, BlobServiceClient, BlobProperties
from typing import Final
from logging import Logger
from pypomes_core import APP_PREFIX, env_get_str, exc_format

# connection string to Azure
AZURE_CONNECTION_STRING: Final[str] = env_get_str(f"{APP_PREFIX}_AZURE_CONNECTION_STRING")

#  storage bucket name
AZURE_STORAGE_BUCKET: Final[str] = env_get_str(f"{APP_PREFIX}_AZURE_STORAGE_BUCKET")


def azure_verify(errors: list[str] | None, logger: Logger = None) -> bool:
    """
    Verify whether a connection to the Azure cloud services is possible.

    :param errors: incidental errors
    :param logger: optional logger
    :return: True if a connection is possible, or False otherwise
    """
    # initialize the return variable
    result: bool = False

    err_msg: str | None = None
    try:
        client: BlobServiceClient = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        client.close()
        result = True
    except Exception as e:
        err_msg = __azure_except_msg(e)

    __azure_log(errors, err_msg, logger, "Verified connection")

    return result


def azure_blob_exists(errors: list[str] | None, blob_path: str,
                      bucket_name: str = AZURE_STORAGE_BUCKET, logger: Logger = None) -> bool:
    """
    Verify whether the file referred to by *blob_path*, within *bucket_name*, exists.

    :param errors: incidental errors
    :param blob_path: file path within the bucket
    :param bucket_name: name of bucket (defaults to AZURE_STORAGE_BUCKET)
    :param logger: optional logger
    :return: True if the file exists, False otherwise, or None if error
    """
    # initialize the return variable
    result: bool | None = None

    err_msg: str | None = None
    try:
        with BlobClient.from_connection_string(
            conn_str=AZURE_CONNECTION_STRING,
            container_name=bucket_name,
            blob_name=blob_path
        ) as client:
            result = client.exists()
    except Exception as e:
        err_msg = __azure_except_msg(e)

    __azure_log(errors, err_msg, logger, f"Checked if blob '{blob_path}' exists")

    return result


def azure_blob_retrieve(errors: list[str] | None, blob_path: str,
                        bucket_name: str = AZURE_STORAGE_BUCKET, logger: Logger = None) -> bytes:
    """
    Obtem e retorna o conteúdo *raw* do arquivo apontado por *blob_path*, dentro de *bucket_name*.

    :param errors: incidental errors
    :param blob_path: file path within the bucket
    :param bucket_name: name of bucket (defaults to AZURE_STORAGE_BUCKET)
    :param logger: optional logger
    :return: file contents, or None if error
    """
    # initialize the return variable
    result: bytes | None = None

    err_msg: str | None = None
    try:
        with BlobClient.from_connection_string(
            conn_str=AZURE_CONNECTION_STRING,
            container_name=bucket_name,
            blob_name=blob_path
        ) as client:
            stream: io.BytesIO = io.BytesIO()
            client.download_blob().readinto(stream)
            stream.seek(0)
            result = stream.read()
    except Exception as e:
        err_msg = __azure_except_msg(e)

    __azure_log(errors, err_msg, logger, f"Retrieved blob '{blob_path}'")

    return result


def azure_blob_store(errors: list[str] | None, content: bytes, blob_path: str,
                     bucket_name: str = AZURE_STORAGE_BUCKET, logger: Logger = None) -> bool:
    """
    Armazena o conteúdo *content* no caminho apontado por *blob_path*, dentro de *bucket_name*.

    :param errors: incidental errors
    :param content: conteúdo a ser armazenado
    :param blob_path: file path within the bucket
    :param bucket_name: name of bucket (defaults to AZURE_STORAGE_BUCKET)
    :param logger: optional logger
    :return: True if success, or False otherwise
    """
    # declare the return variable
    result: bool

    err_msg: str | None = None
    try:
        with BlobClient.from_connection_string(
            conn_str=AZURE_CONNECTION_STRING,
            container_name=bucket_name,
            blob_name=blob_path
        ) as client:
            stream: io.BytesIO = io.BytesIO(content)
            stream.seek(0)
            client.upload_blob(data=stream,
                               blob_type="BlockBlob",
                               length=len(content),
                               overwrite=True)
            result = True
    except Exception as e:
        result = False
        err_msg = __azure_except_msg(e)

    __azure_log(errors, err_msg, logger, f"Stored blob '{blob_path}'")

    return result


def azure_blob_delete(errors: list[str] | None, blob_path: str,
                      bucket_name: str = AZURE_STORAGE_BUCKET, logger: Logger = None) -> bool:
    """
    Remove o arquivo apontado por *blob_path*, dentro de *bucket_name*, e todos os seus *snapshots*.

    :param errors: incidental errors
    :param blob_path: file path within the bucket
    :param bucket_name: name of bucket (defaults to AZURE_STORAGE_BUCKET)
    :param logger: optional logger
    :return: True if success, or False otherwise
    """
    # declare the return variable
    result: bool

    err_msg: str | None = None
    try:
        with BlobClient.from_connection_string(
            conn_str=AZURE_CONNECTION_STRING,
            container_name=bucket_name,
            blob_name=blob_path
        ) as client:
            client.delete_blob(delete_snapshots="include")
            result = True
    except Exception as e:
        result = False
        err_msg = __azure_except_msg(e)

    __azure_log(errors, err_msg, logger, f"Deleted blob '{blob_path}'")

    return result


def azure_blob_get_mimetype(errors: list[str] | None, blob_path: str,
                            bucket_name: str = AZURE_STORAGE_BUCKET, logger: Logger = None) -> str:
    """
    Return the mimetype of the file referred to by *file_path*, within  *bucket_name*.

    :param errors: incidental errors
    :param blob_path: file path within the bucket
    :param bucket_name: name of bucket (defaults to AZURE_STORAGE_BUCKET)
    :param logger: optional logger
    :return: the file mimetype, or None if error
    """
    # initialize the return variable
    result: str | None = None

    err_msg: str | None = None
    try:
        with BlobClient.from_connection_string(
            conn_str=AZURE_CONNECTION_STRING,
            container_name=bucket_name,
            blob_name=blob_path
        ) as client:
            props: BlobProperties = client.get_blob_properties()
            result = props.get("content_settings").get("content_type")
    except Exception as e:
        err_msg = __azure_except_msg(e)

    __azure_log(errors, err_msg, logger, f"Got mimetype for blob '{blob_path}'")

    return result


def __azure_except_msg(exception: Exception) -> str:
    """
    Format and return the error message in the exception raised on acessing Azure.

    :param exception: the raised exception
    :return: the formatted error message
    """
    # TODO
    return exc_format(exception, sys.exc_info())


def __azure_log(errors: list[str] | None, err_msg: str, logger: Logger, debug_msg: str) -> None:
    """
    Log *err_msg* and add it to *errors*, or log *debug_msg*, whatever is applicable.

    :param errors: incidental errors
    :param err_msg: the error message
    :param logger: optional logger
    :param debug_msg: a debug message
    """
    if err_msg:
        if logger:
            logger.error(err_msg)
        if errors is not None:
            errors.append(err_msg)
    elif logger:
        logger.debug(debug_msg)


# test Azure operations
if __name__ == "__main__":

    # ruff: noqa: S101

    def __print_errors(errors: list[str], op: str) -> None:
        if len(errors) > 0:
            print(f"\nErrors in '{op}':")
            for error in errors:
                print(error)

    errors: list[str] = []
    content: bytes = b"This is the content of a sample text file."
    file_path: str = "/temp/sample.txt"

    # verify if file exists
    exists: bool = azure_blob_exists(errors, file_path)
    __print_errors(errors, "blob_exists")
    assert exists is not None, "Failed verifying file"

    # store file
    if not exists:
        success = azure_blob_store(errors, content, file_path)
        __print_errors(errors, "blob_store")
        assert success, "Failed storing file"

    # retrieve file type
    mimetype: str = azure_blob_get_mimetype(errors, file_path)
    __print_errors(errors, "blob_get_mimetype")
    assert mimetype is not None, "Failed retrieving file mimetype"

    # retrieve file contents
    retrieved: bytes = azure_blob_retrieve(errors, file_path)
    __print_errors(errors, "blob_retrieve")
    assert retrieved is not None, "Failed retrieving file content"
    print(f"Conteudo recuperado: {content}")

    # remove the file
    success = azure_blob_delete(errors, file_path)
    __print_errors(errors, "blob_delete")
    assert success, "Failed Deleting file"

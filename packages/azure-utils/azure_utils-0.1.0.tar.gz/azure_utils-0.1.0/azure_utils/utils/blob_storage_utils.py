import os, hashlib, json, pathlib


def validate_path(path: str, is_remote: bool, is_folder: bool) -> None:
    """
    Function:

    Validates a path string

    Parameters:

    - `path` (str): The path to validate
    - `is_remote` (bool): Whether the path is remote or local
    - `is_folder` (bool): Whether the path is a folder or file

    Returns:

    - `None`

    Raises:

    - `Exception`: If the path is invalid

    Example:

    ```python
    from azure_utils.blob_storage import validate_path
    validate_path(path='/path/to/folder/', is_remote=True, is_folder=True)
    # This will return `None`
    # This will raise an exception if the path is invalid
    ```
    """
    posix_path = str(pathlib.PurePosixPath(path))
    if path.endswith("/") or path.endswith("\\"):
        if posix_path != "/":
            posix_path = posix_path + "/"
    if is_remote:
        if posix_path != path:
            raise Exception(
                f"Path Error: Remote storage uses posix paths. Received: `{path}`"
            )
    else:
        if posix_path == "/":
            raise Exception(
                f"Path Error: Cannot use the root folder for local storage. Received: `{path}`"
            )
    if not posix_path.startswith("/"):
        raise Exception(
            f"Path Error: Path must be absolute. Received: `{path}`"
        )
    if is_folder and not posix_path.endswith("/"):
        raise Exception(
            f"Path Error: A folder is required for this path. You may need to include a trailing slash. Received: `{path}`"
        )
    if not is_folder and posix_path.endswith("/"):
        raise Exception(
            f"Path Error: A file is required for this path. Received: `{path}`"
        )


class MetaFile:
    def __init__(self, filepath: str):
        """
        Function:

        - Creates a MetaFile object
        - Can be used to associate arbitrary meta data to any file
        - Includes a built in method to calculate the md5 hash of the file

        Parameters:

        - `filepath` (str): The path to the file

        Returns:

        - The MetaFile object

        Example:

        ```python
        from azure_utils.blob_storage import MetaFile
        meta_file = MetaFile(filepath='/path/to/file.txt')
        meta_file.data['my_meta_key'] = 'my_meta_value'
        meta_file.update()
        # This will create a file at `/path/to/.meta.file.txt`
        # The file will contain the following json:
        # {
        #     "my_meta_key": "my_meta_value",
        # }
        ```
        """
        validate_path(path=filepath, is_remote=False, is_folder=False)
        self.filepath = filepath
        self.meta_filepath = self.__get_meta_filepath__(filepath)
        self.data = (
            self.__get_data__() if os.path.isfile(self.meta_filepath) else {}
        )

    def __get_meta_filepath__(self, filepath: str) -> str:
        """
        Function:

        - Gets the path to the meta file

        Parameters:

        - `filepath` (str): The path to the file

        Returns:

        - The path to the meta file

        Example:

        ```python
        from azure_utils.blob_storage import MetaFile
        meta_file = MetaFile(filepath='/path/to/file.txt')
        meta_file.__get_meta_filepath__(filepath='/path/to/file.txt')
        # This will return `/path/to/.meta.file.txt`
        ```
        """
        return os.path.join(
            os.path.dirname(filepath), ".meta." + os.path.basename(filepath)
        )

    def __get_data__(self) -> dict:
        """
        Function:

        - Gets the data from the meta file

        Parameters:

        - `None`

        Returns:

        - The data from the meta file

        Example:

        ```python
        from azure_utils.blob_storage import MetaFile
        meta_file = MetaFile(filepath='/path/to/file.txt')
        meta_file.__get_data__()
        # This will return the data from the meta file
        ```
        """
        with open(self.meta_filepath, "r") as meta_file:
            return json.load(meta_file)

    def __calc_md5__(self) -> str:
        """
        Function:

        - Calculates the md5 hash of the file

        Parameters:

        - `None`

        Returns:

        - The md5 hash of the file

        Example:

        ```python
        from azure_utils.blob_storage import MetaFile
        meta_file = MetaFile(filepath='/path/to/file.txt')
        meta_file.__calc_md5__()
        # This will return the md5 hash of `/path/to/file.txt`
        ```
        """
        if not os.path.isfile(self.filepath):
            return None
        with open(self.filepath, "rb") as blob_file:
            return hashlib.md5(blob_file.read()).hexdigest()

    def validate_md5(self) -> bool:
        """

        Function:

        - Validates the md5 hash of the file

        Parameters:

        - `None`

        Returns:

        - Whether the md5 hash of the file is valid


        """
        return self.data["md5"] == self.__calc_md5__()

    def update(self, include_md5: bool = True) -> None:
        """
        Function:

        - Updates the meta file

        Parameters:

        - `include_md5` (bool): Whether to include the md5 hash of the file

        Returns:

        - `None`

        Example:

        ```python
        from azure_utils.blob_storage import MetaFile
        meta_file = MetaFile(filepath='/path/to/file.txt')
        meta_file.data['my_meta_key'] = 'my_meta_value'
        meta_file.update()
        # This will create a file at `/path/to/.meta.file.txt`
        # The file will contain the following json:
        # {
        #     "my_meta_key": "my_meta_value",
        # }
        ```
        """
        if include_md5:
            self.data["md5"] = self.__calc_md5__()
        with open(self.meta_filepath, "w") as meta_file:
            json.dump(self.data, meta_file)


class AZBlob:
    def __init__(self, blob_client):
        """
        Function:

        - Creates an AZBlob object

        Parameters:

        - `blob_client` (azure.storage.blob.BlobClient): The blob client

        Returns:

        - The AZBlob object

        Example:

        ```python
        from azure.storage.blob import BlobClient
        from azure_utils.blob_storage import AZBlob
        myblob = AZBlob(
            blob_client=BlobClient.from_connection_string(
                conn_str="my_connection_string",
                container_name="my_container",
                blob_name="/path/to/my/blob/file.txt"
            )
        )
        myblob.download(filepath='/path/to/file.txt')
        ```
        """
        self.blob_client = blob_client

    def download(self, filepath) -> None:
        """
        Function:

        - Downloads a blob from the remote to a local file

        Parameters:

        - `filepath` (str): The path to the local file

        Returns:

        - `None`
        """
        validate_path(path=filepath, is_remote=False, is_folder=False)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as blob_file:
            self.blob_client.download_blob().readinto(blob_file)

    def delete(self) -> None:
        """
        Function:

        - Deletes a blob from the remote

        Parameters:

        - `None`

        Returns:

        - `None`
        """
        self.blob_client.delete_blob(delete_snapshots="include")


class MetaBlob(AZBlob):
    def __init__(
        self,
        blob_client,
        filepath: str,
        smart_sync: bool = False,
        remote_etag: [str, None] = None,
        overwrite: bool = False,
    ):
        """
        Function:

        - Creates a MetaBlob object

        Parameters:

        - `blob_client` (azure.storage.blob.BlobClient): The blob client
        - `filepath` (str): The path to the local file
        - `smart_sync` (bool): Whether to skip downloading if the remote etag and md5 hash match the local meta file
            - Optional: Defaults to `False`
        - `remote_etag` (str): The remote etag. Used to avoid fetching the etag from the remote if it is already known
            - Optional: Defaults to the current etag of the remote blob
        - `overwrite` (bool): Whether to overwrite the local file if it already exists
            - Optional: Defaults to `False`

        Returns:

        - The MetaBlob object

        Example:

        ```python

        from azure.storage.blob import BlobClient
        from azure_utils.blob_storage import MetaBlob
        myblob = MetaBlob(
            blob_client=BlobClient.from_connection_string(
                conn_str="my_connection_string",
                container_name="my_container",
                blob_name="/path/to/my/blob/file.txt"
            ),
            filepath='/path/to/file.txt',
            smart_sync=True,
            overwrite=True
        )
        myblob.download()
        """
        super().__init__(blob_client)
        validate_path(path=filepath, is_remote=False, is_folder=False)
        self.filepath = filepath
        self.meta = MetaFile(filepath)
        if remote_etag is None:
            self.update_etag()
        else:
            self.remote_etag = remote_etag
        self.block_download = False
        if smart_sync:
            if self.meta.data.get("etag") == self.remote_etag:
                if self.meta.validate_md5():
                    self.block_download = True
        if not overwrite and os.path.isfile(filepath):
            self.block_download = True

    def update_etag(self) -> None:
        """
        Function:

        - Updates the local etag with the current etag of the remote blob

        Parameters:

        - `None`

        Returns:

        - `None`
        """
        self.remote_etag = self.blob_client.get_blob_properties().etag

    def update_meta(self) -> None:
        """
        Function:

        - Updates the local meta file

        Parameters:

        - `None`

        Returns:

        - `None`
        """
        self.meta.data["etag"] = self.remote_etag
        self.meta.update(include_md5=True)

    def download(self) -> None:
        """
        Function:

        - Downloads a blob from the remote to a local file

        Parameters:

        - `None`

        Returns:

        - `None`
        """
        if self.block_download:
            return
        super().download(filepath=self.filepath)
        self.update_meta()

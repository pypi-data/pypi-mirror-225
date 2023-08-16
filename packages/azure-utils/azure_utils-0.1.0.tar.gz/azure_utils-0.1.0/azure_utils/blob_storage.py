import os, pathlib
from azure.storage.blob import ContainerClient

from azure_utils.utils.blob_storage_utils import AZBlob, MetaBlob, validate_path


class AZContainer:
    def __init__(self, account_url: str, account_key: str, container_name: str):
        """
        Function:

        - Creates an AZContainer object

        Parameters:

        - `account_url` (str): The account url
        - `account_key` (str): The account key
        - `container_name` (str): The container name

        Returns:

        - The AZContainer object

        Example:

        ```python
        from azure_utils.blob_storage import AZContainer
        mycontainer = AZContainer(
            account_url="my_account_url",
            account_key="my_account_key",
            container_name="my_container"
        )
        print(mycontainer.list_files(remote_folderpath='/path/to/folder/')
        # This will print a list of all files in the remote folder `/path/to/folder/`
        ```
        """
        self.client = ContainerClient(
            account_url=account_url,
            container_name=container_name,
            credential=account_key,
        )

    def list_files(self, remote_folderpath: str) -> list:
        """
        Function:

        - Lists all files in a remote folder

        Parameters:

        - `remote_folderpath` (str): The path to the remote folder

        Returns:

        - A list of all files (as strings) in the remote folder (including subfolders)

        Example:

        ```python
        from azure_utils.blob_storage import AZContainer
        mycontainer = AZContainer(
            account_url="my_account_url",
            account_key="my_account_key",
            container_name="my_container"
        )
        print(mycontainer.list_files(remote_folderpath='/path/to/folder/')
        # This will print a list of all files in the remote folder `/path/to/folder/`
        ```
        """
        validate_path(path=remote_folderpath, is_remote=True, is_folder=True)
        return [
            i.name
            for i in self.client.list_blobs(name_starts_with=remote_folderpath)
        ]

    def upload_file(
        self, remote_filepath: str, local_filepath: str, overwrite: bool = False
    ) -> None:
        """
        Function:

        - Uploads a file from local to remote

        Parameters:

        - `remote_filepath` (str): The path to the remote file
        - `local_filepath` (str): The path to the local file
        - `overwrite` (bool): Whether to overwrite the remote file if it already exists
            - Optional: Defaults to `False`

        Returns:

        - `None`

        Example:

        ```python
        from azure_utils.blob_storage import AZContainer
        mycontainer = AZContainer(
            account_url="my_account_url",
            account_key="my_account_key",
            container_name="my_container"
        )
        mycontainer.upload_file(
            remote_filepath='/path/to/file.txt',
            local_filepath='/path/to/file.txt',
            overwrite=True
        )
        # This will upload the local file `/path/to/file.txt` to the remote file `/path/to/file.txt`
        ```
        """
        validate_path(path=local_filepath, is_remote=False, is_folder=False)
        validate_path(path=remote_filepath, is_remote=True, is_folder=False)
        with open(local_filepath, "rb") as data:
            blob = MetaBlob(
                blob_client=self.client.upload_blob(
                    name=remote_filepath, data=data, overwrite=overwrite
                ),
                filepath=local_filepath,
            )
        blob.update_meta()

    def download_file(
        self,
        remote_filepath: str,
        local_filepath: str,
        overwrite: bool = False,
        smart_sync: bool = False,
    ) -> None:
        """
        Function:

        - Downloads a file from remote to local

        Parameters:

        - `remote_filepath` (str): The path to the remote file
        - `local_filepath` (str): The path to the local file
        - `overwrite` (bool): Whether to overwrite the local file if it already exists
            - Optional: Defaults to `False`
        - `smart_sync` (bool): Whether to skip downloading if the remote etag and md5 hash match the local meta file
            - Optional: Defaults to `False`

        Returns:

        - `None`

        Example:

        ```python
        from azure_utils.blob_storage import AZContainer
        mycontainer = AZContainer(
            account_url="my_account_url",
            account_key="my_account_key",
            container_name="my_container"
        )
        mycontainer.download_file(
            remote_filepath='/path/to/file.txt',
            local_filepath='/path/to/file.txt',
            overwrite=True,
            smart_sync=True
        )
        # This will download the remote file `/path/to/file.txt` to the local file `/path/to/file.txt`
        ```
        """
        validate_path(path=local_filepath, is_remote=False, is_folder=False)
        validate_path(path=remote_filepath, is_remote=True, is_folder=False)
        blob = MetaBlob(
            blob_client=self.client.get_blob_client(blob=remote_filepath),
            filepath=local_filepath,
            smart_sync=smart_sync,
            overwrite=overwrite,
        )
        blob.download()

    def delete_file(self, remote_filepath: str) -> None:
        """
        Function:

        - Deletes a file from remote

        Parameters:

        - `remote_filepath` (str): The path to the remote file

        Returns:

        - `None`

        Example:
        ```python
        from azure_utils.blob_storage import AZContainer
        mycontainer = AZContainer(
            account_url="my_account_url",
            account_key="my_account_key",
            container_name="my_container"
        )
        mycontainer.delete_file(remote_filepath='/path/to/file.txt')
        ```
        """
        validate_path(path=remote_filepath, is_remote=True, is_folder=False)
        blob = AZBlob(
            blob_client=self.client.get_blob_client(blob=remote_filepath)
        )
        blob.delete()

    def sync_to_local(
        self,
        remote_folderpath: str,
        local_folderpath: str,
        overwrite: bool = False,
        smart_sync: bool = False,
        removal: bool = False,
    ) -> None:
        """
        Function:

        - Sync all files from a remote folder to a local folder

        Parameters:

        - `remote_folderpath` (str): The path to the remote folder
        - `local_folderpath` (str): The path to the local folder
        - `overwrite` (bool): Whether to overwrite the local file if it already exists
            - Optional: Defaults to `False`
        - `smart_sync` (bool): Whether to skip downloading if the remote etag and md5 hash match the local meta file
            - Optional: Defaults to `False`
        - `removal` (bool): Whether to remove local files that do not exist in the remote folder
            - Optional: Defaults to `False`

        Returns:

        - `None`

        Example:

        ```python
        from azure_utils.blob_storage import AZContainer
        mycontainer = AZContainer(
            account_url="my_account_url",
            account_key="my_account_key",
            container_name="my_container"
        )
        mycontainer.sync_to_local(
            remote_folderpath='/path/to/folder/',
            local_folderpath='/path/to/folder/',
            overwrite=True,
            smart_sync=True,
            removal=True
        )
        # This will sync the remote folder `/path/to/folder/` to the local folder `/path/to/folder/`
        # It will also remove any local files that do not exist in the remote folder
        ```
        """
        validate_path(path=local_folderpath, is_remote=False, is_folder=True)
        validate_path(path=remote_folderpath, is_remote=True, is_folder=True)
        blobs = [
            i
            for i in self.client.list_blobs(name_starts_with=remote_folderpath)
        ]
        for blobProperty in blobs:
            blob = MetaBlob(
                blob_client=None,
                filepath=local_folderpath
                + blobProperty.name.replace(remote_folderpath, ""),
                smart_sync=smart_sync,
                remote_etag=blobProperty.etag,
                overwrite=overwrite,
            )
            if blob.block_download:
                continue
            blob.blob_client = self.client.get_blob_client(
                blob=blobProperty.name
            )
            blob.download()
        if removal:
            posix_folderpath = str(pathlib.PurePosixPath(local_folderpath))
            if posix_folderpath == "/":
                raise Exception("Cannot do removal in the root folder")
            storage_filepaths = set(
                [i.name.replace(remote_folderpath, "") for i in blobs]
            )
            for local_filepath in [
                str(i) for i in pathlib.Path(local_folderpath).glob("**/*")
            ]:
                posix_filepath = str(pathlib.PurePosixPath(local_filepath))
                if (
                    posix_filepath.replace(posix_folderpath, "").replace(
                        ".meta.", ""
                    )
                    not in storage_filepaths
                ):
                    os.remove(local_filepath)

    def sync_to_remote(
        self,
        remote_folderpath: str,
        local_folderpath: str,
        overwrite: bool = False,
        omissions: list = [".meta."],
    ) -> None:
        """
        Function:

        - Sync all files from a local folder to a remote folder

        Parameters:

        - `remote_folderpath` (str): The path to the remote folder
        - `local_folderpath` (str): The path to the local folder
        - `overwrite` (bool): Whether to overwrite the remote file if it already exists
            - Optional: Defaults to `False`
        - `omissions` (list): A list of strings to omit from the upload
            - Optional: Defaults to `['.meta.']`

        Returns:

        - `None`

        Example:
        ```python
        from azure_utils.blob_storage import AZContainer
        mycontainer = AZContainer(
            account_url="my_account_url",
            account_key="my_account_key",
            container_name="my_container"
        )
        mycontainer.sync_to_remote(
            remote_folderpath='/path/to/folder/',
            local_folderpath='/path/to/folder/',
        )
        # This will sync the local folder `/path/to/folder/` to the remote folder `/path/to/folder/`
        ```
        """
        validate_path(path=local_folderpath, is_remote=False, is_folder=True)
        validate_path(path=remote_folderpath, is_remote=True, is_folder=True)
        local_filepaths = [
            str(i) for i in pathlib.Path(local_folderpath).glob("**/*")
        ]
        local_filepaths = [
            i for i in local_filepaths if not any([j in i for j in omissions])
        ]
        for local_filepath in local_filepaths:
            self.upload_file(
                remote_filepath=remote_folderpath
                + local_filepath.replace(local_folderpath, ""),
                local_filepath=local_filepath,
                overwrite=overwrite,
            )

    def delete_folder(self, remote_folderpath: str) -> None:
        """
        Function:

        - Deletes all files in a remote folder

        Parameters:

        - `remote_folderpath` (str): The path to the remote folder

        Returns:

        - `None`

        Example:

        ```python
        from azure_utils.blob_storage import AZContainer
        mycontainer = AZContainer(
            account_url="my_account_url",
            account_key="my_account_key",
            container_name="my_container"
        )
        mycontainer.delete_folder(remote_folderpath='/path/to/folder/')
        ```
        """
        validate_path(path=remote_folderpath, is_remote=True, is_folder=True)
        storage_filenames = self.client.list_blob_names(
            name_starts_with=remote_folderpath
        )
        for filename in storage_filenames:
            blob = AZBlob(
                blob_client=self.client.get_blob_client(blob=filename)
            )
            blob.delete()

    def clear_local_meta(
        self, local_folderpath: str, includsions: list = [".meta."]
    ) -> None:
        """
        Function:

        - Deletes all meta files in a local folder

        Parameters:

        - `local_folderpath` (str): The path to the local folder
        - `includsions` (list): A list of strings to include in the deletion
            - Optional: Defaults to `['.meta.']`

        Returns:

        - `None`

        Example:

        ```python
        from azure_utils.blob_storage import AZContainer
        mycontainer = AZContainer(
            account_url="my_account_url",
            account_key="my_account_key",
            container_name="my_container"
        )
        mycontainer.clear_local_meta(local_folderpath='/path/to/folder/')
        ```
        """
        validate_path(path=local_folderpath, is_remote=False, is_folder=True)
        local_filepaths = [
            str(i) for i in pathlib.Path(local_folderpath).glob("**/*")
        ]
        for filepath in [
            i for i in local_filepaths if any([j in i for j in includsions])
        ]:
            os.remove(filepath)

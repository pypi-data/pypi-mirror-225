import calendar
import os
import re
import sys
import time
from copy import deepcopy
from typing import List, Generator, Dict, Any, Optional, Tuple

import requests
from azure.storage.blob import BlobClient, ContainerClient
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk

from ._internal_utils import TokenHolder, _get_azure_storage_url, _sanitize_url
from .config import _ENVS, _ACCESS_TOKEN_ENV_KEY, _REFRESH_TOKEN_ENV_KEY


class SDKClient:
    f"""
    client class providing methods for accessing SDK services: 
        - organizationmanager (access to organizations/spaces)
        - opensearch
        - storage
    
    Authorization for the SDK services is done using JWT tokens, which are stored in memory.
    For every request, the access token is refreshed if it is about to expire or has already expired.
    If no login information is passed to the main class 'SDKClient' during initialization, the access and refresh tokens are expected to be stored in the 
    environment variables of the execution environment.

    Usage::
        If access/refresh token can be found int the env-variables {_ACCESS_TOKEN_ENV_KEY} / {_REFRESH_TOKEN_ENV_KEY}
        >>> import superbdataklient as sdk
        >>> client = sdk.SDKClient()

        or with explicit login:
        >>> import superbdataklient as sdk
        >>> client = sdk.SDKClient(username='hasslethehoff', password='lookingforfreedom')
        
        this module is pre configured for usage with the default instance of the SDK (found here https://sdk.efs.ai) and comes with settings for various 
        different instances
        
        choosing different environment:
        >>> client = sdk.SDKClient(env='sdk-dev')
        
        overwriting settings:
        >>> client = sdk.SDKClient(domain='mydomain.ai', client_id='my-client-id', api_version='v13.37')
    """

    def __init__(self, **kwargs: str) -> None:
        self._env = deepcopy(_ENVS.get(kwargs.get('env', 'sdk')))

        # overwrite settings from args
        if 'domain' in kwargs:
            self._env.domain = kwargs.get('domain')
        if 'realm' in kwargs:
            self._env.realm = kwargs.get('realm')
        if 'client_id' in kwargs:
            self._env.client_id = kwargs.get('client_id')
        if 'api_version' in kwargs:
            self._env.api_version = kwargs.get('api_version')
        self.org_endpoint = f'https://{self._env.domain}/organizationmanager/api/{self._env.api_version}/organization'
        self.space_endpoint = f'https://{self._env.domain}/organizationmanager/api/{self._env.api_version}/space'

        if 'username' in kwargs and 'password' in kwargs:
            self._token_holder = TokenHolder(domain=self._env.domain, realm=self._env.realm, client_id=self._env.client_id)
            self._token_holder.get_tokens_with_credentials(kwargs['username'], kwargs['password'])
        else:
            try:
                access_token = os.environ[_ACCESS_TOKEN_ENV_KEY]
                refresh_token = os.environ[_REFRESH_TOKEN_ENV_KEY]
                self._token_holder = TokenHolder(domain=self._env.domain,
                                                 realm=self._env.realm,
                                                 client_id=self._env.client_id,
                                                 access_token=access_token,
                                                 refresh_token=refresh_token)
            except KeyError:
                print(f'Cannot read token environment variables {_ACCESS_TOKEN_ENV_KEY}, {_REFRESH_TOKEN_ENV_KEY}', file=sys.stderr)
                print('Assert that variables are set or try login initializing with username and password.', file=sys.stderr)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ organizations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def organization_get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves a list of all organizations that the user can access.

        :return: A list of dictionaries, where each dictionary contains details of an organization.
        """
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(self.org_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def organization_get_by_id(self, organization_id: int) -> Dict[str, Any]:
        """
        Retrieves details of the organization with the specified ID.

        :param organization_id: The ID of the organization to be fetched.

        :return: A dictionary containing details of the requested organization.

        """
        url = f'{self.org_endpoint}/{organization_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def organization_get_by_name(self, organization: str) -> Dict[str, Any]:
        """
        Retrieves details of the organization with the specified name.

        :param organization: The name of the organization to be fetched.

        :return: A dictionary containing details of the requested organization.
        """
        url = f'{self.org_endpoint}/name/{organization}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ spaces ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def space_get_all(self, organization_id: int) -> List[Dict[str, Any]]:
        """
        Retrieves a list of all spaces within the specified organization.

        :param organization_id: The unique identifier of the organization whose spaces need to be fetched.

        :return: A list of dictionaries, where each dictionary represents the details of a space within the organization.
        """
        url = f'{self.space_endpoint}/{organization_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_get_by_id(self, organization_id: int, space_id: int) -> Dict[str, Any]:
        """
        Retrieves details of a space within a specified organization using the space's name.

        :param organization_id: The unique identifier for the organization under which the space resides.
        :param space_id: The unique identifier of the space to retrieve.

        :return: A dictionary representing the details of the requested space as returned by the API.

        Note:
        Ensure that the provided token has the necessary permissions to access the space details.
        """
        url = f'{self.space_endpoint}/{organization_id}/{space_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_get_by_name(self, organization_id: int, space: str) -> Dict[str, Any]:
        """
        Retrieves details of a space within a specified organization using the space's name.

        :param organization_id: The unique identifier for the organization under which the space resides.
        :param space: The name of the space to retrieve.

        :return: A dictionary representing the details of the requested space as returned by the API.
        """
        url = f'{self.space_endpoint}/{organization_id}/name/{space}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_create(self, organization_id: int, space: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new space within a specified organization using its ID.

        :param organization_id: The unique identifier for the organization in which the space will be created.
        :param space: A dictionary containing attributes and properties for the new space.

        :return: A dictionary representing the created space as returned by the API.
        """
        url = f'{self.space_endpoint}/{organization_id}'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.post(url, json=space, headers=headers)
        response.raise_for_status()
        return response.json()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ indexing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def index_get_all(self) -> Dict[str, Any]:
        """
        Retrieves all the OpenSearch indices that are accessible.

        :param: None

        :return: A dictionary containing information about all the accessible indices.
        """
        headers = {"Authorization": f"Bearer {self._token_holder.get_token()}"}
        url = f'https://{self._env.domain}/search/{self._env.api_version}/index'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        res = response.json()

        return res

    def index_search(self, index: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Executes a search query on the specified OpenSearch index and returns the matching documents.

        :param index: The name of the OpenSearch index to search.
        :param query: The search query represented as a dictionary, typically containing a DSL query structure.
        :return: A list of documents matching the search query. Each document is represented as a dictionary.

        Example:
        To search for documents with the title "sample" in the "MyIndex" index, you might use:
        `results = index_search("MyIndex", {"query": {"match": {"title": "sample"}}})`
        """
        headers = {
            "Authorization": f"Bearer {self._token_holder.get_token()}"
        }
        url = f'https://{self._env.domain}/elastic/api/{index}/_search'

        response = requests.get(url, headers=headers, json=query)
        response.raise_for_status()
        res = [hit['_source'] for hit in response.json()['hits']['hits']]

        return res

    def index_get_document(self, index: str, doc_id: str) -> Dict[str, Any]:
        """
        Retrieves a specific document from the specified OpenSearch index using its document ID.

        :param index: The name of the OpenSearch index where the document resides.
        :param doc_id: The unique identifier of the desired document within the index.
        :return: The requested document represented as a dictionary.

        Example:
        To fetch a document with ID "doc123" from an index named "SampleIndex", you can call:
        `document = index_get_document("SampleIndex", "doc123")`
        """
        headers = {"Authorization": f"Bearer {self._token_holder.get_token()}"}
        url = f'https://{self._env.domain}/elastic/api/{index}/_doc/{doc_id}'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        doc = response.json()['_source']

        return doc

    @staticmethod
    def _get_scroll_id_and_documents(url: str, headers: Dict[str, str]) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        response_json = response.json()
        scroll_id = response_json.get('_scroll_id', None)
        documents = [hit['_source'] for hit in response_json.get('hits', {}).get('hits', [])]

        return scroll_id, documents

    def _delete_scroll_id(self, scroll_id: str, headers: Dict[str, str]) -> None:
        delete_url = f"https://{self._env.domain}/elastic/api/_search/scroll/{scroll_id}"
        response = requests.delete(delete_url, headers=headers)
        response.raise_for_status()

    def index_get_documents(self, index: str, scroll_duration: str = '10m', batch_size: int = 10000) -> Generator[Dict[str, Any], None, None]:
        """
        Retrieves documents from a specified OpenSearch index using a generator.

        This method employs the scrolling mechanism of OpenSearch to fetch documents
        in batches, ensuring efficient memory usage, especially for large datasets.
        Each batch fetches a specified number of documents at once.

        :param index: The name of the OpenSearch index from which to retrieve documents.
        :param scroll_duration: Duration a scroll ID remains valid in OpenSearch. It determines
                                the window to keep the search context alive. Defaults to '10m'.
        :param batch_size: Number of documents to fetch in each request to OpenSearch. Defaults to 10,000.

        :yield: Yields individual documents from the OpenSearch index.

        Example:
        To retrieve documents from an index named "SampleIndex" using the default scroll duration
        and batch size, use:
        `documents = [doc for doc in index_get_documents("SampleIndex")]`
        """
        headers = {"Authorization": f"Bearer {self._token_holder.get_token()}"}
        url = f"https://{self._env.domain}/elastic/api/{index}/_search?scroll={scroll_duration}&size={batch_size}"

        scroll_id, documents = self._get_scroll_id_and_documents(url, headers)
        for document in documents:
            yield document

        while documents:
            url = f"https://{self._env.domain}/elastic/api/_search/scroll?scroll={scroll_duration}&scroll_id={scroll_id}"
            scroll_id, documents = self._get_scroll_id_and_documents(url, headers)
            for document in documents:
                yield document

        self._delete_scroll_id(scroll_id, headers)

    def index_get_all_documents(self, index: str) -> List[Dict[str, Any]]:
        """
        Retrieves all documents from a specified OpenSearch index.

        This method fetches every document from the named index and returns them
        as a list of dictionaries. If the index doesn't exist or is empty, the result
        will be an empty list.

        :param index: The name of the index from which to retrieve documents.
        :return: A list of all documents in the specified index. Each document is
                 represented as a dictionary. An empty list is returned if the index
                 doesn't contain any documents or doesn't exist.

        Example:
        To fetch all documents from an index named "SampleIndex", you can call:
        `all_docs = index_get_all_documents("SampleIndex")`

        Note:
        Ensure the OpenSearch instance is operational and the provided token has the
        necessary permissions to retrieve documents.
        """
        return [doc for doc in self.index_get_documents(index)]

    def index_documents(self, documents: List[Dict[str, Any]], index_name: str, timeout: int = 60, chunk_size: int = 10000) -> None:
        """
        Indexes multiple documents into the specified index in chunks using the bulk API.

        This method establishes a connection to the Opensearch instance and performs
        bulk indexing of the provided documents. Chunking ensures efficient ingestion
        and helps avoid potential timeouts for large datasets.

        :param documents: A list of dictionaries representing the documents to be indexed.
        :param index_name: The name of the index where the documents will be stored.
        :param timeout: Maximum time (in seconds) to wait for a response during the bulk operation. Defaults to 60 seconds.
        :param chunk_size: The number of documents that are indexed in a single bulk operation. Defaults to 10,000.

        Example:
        To index a list of documents into an index named "SampleIndex", you can call:
        `index_documents(document_list, "SampleIndex")`
        """
        url = f'https://{self._env.domain}/elastic/api/'
        es = OpenSearch(url, use_ssl=True, headers={"Authorization": "Bearer " + self._token_holder.get_token()}, timeout=timeout)

        # Create data for bulk api
        actions = [
            {
                "_index": index_name,
                "_id": entry.pop('_id') if '_id' in entry else None,
                "_source": entry
            } for entry in documents
        ]

        # Bulk ingest data
        bulk(es, actions, chunk_size=chunk_size)

        # Close Elasticsearch
        es.close()

    def index_filter_by_space(self, organization: str, space: str, index_type: str) -> List[str]:
        """
        Retrieves a list of indexes filtered by the specified organization, space, and index type.

        This method sends a GET request to the search endpoint, filtering indexes based on the provided
        organization name, space name, and index type. It's useful for narrowing down specific indexes
        associated with certain parameters.

        :param organization: The name of the organization associated with the desired indexes.
        :param space: The specific space or partition within the organization.
                      Use '*' to represent all spaces in the organization.
        :param index_type: Specifies the type of index to filter by, such as 'analysis' or 'measurement'.

        :return: A list containing details of the indexes that match the filter criteria.

        :raises: requests.exceptions.HTTPError If the request to filter the indexes fails.

        Example:
        To retrieve indexes of type 'analysis' for an organization "OrgName" and space "SpaceName", call:
        `indexes = index_filter_by_space("OrgName", "SpaceName", "analysis")`

        Note:
        Ensure that the provided token has the necessary permissions to retrieve index details.
        """
        headers = {"Authorization": f"Bearer {self._token_holder.get_token()}"}
        url = f'https://{self._env.domain}/search/{self._env.api_version}/index?filter={organization}_{space}_{index_type.lower()}.*'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        res = response.json()

        return res

    def application_index_create(self, index_name: str, organization: str, space: str, mapping: object, index_type: str = 'ANALYSIS') -> str:
        """
        Creates a new application index with the specified parameters.

        This method sends a POST request to the corresponding endpoint with the
        necessary data to create a new application index. The index can be utilized
        for various application-specific functionalities based on its type.

        :param index_name: A custom name assigned to the index for identification.
        :param organization: The name of the organization associated with the index.
        :param space: The specific space or partition within the organization where the index belongs.
        :param mapping: An object representing the structure and relationships of the data within the index.
        :param index_type: The type of the index. Defaults to 'ANALYSIS' if not provided.

        :return: The response body of the HTTP request, typically providing details or a confirmation of the index creation.

        :raises: requests.exceptions.HTTPError If the request to create the application index fails.

        Example:
        To create an index named "SampleIndex" for organization "OrgName" in space "SpaceName" with a specific mapping, you can call:
        `response = application_index_create("SampleIndex", "OrgName", "SpaceName", mapping_object)`
        """

        application_index = {
            "organizationName": organization,
            "spaceName": space,
            "customName": index_name,
            "indexType": index_type,
            "mappings": mapping
        }
        url = f'https://{self._env.domain}/metadata/{self._env.api_version}/application-index'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.post(url, json=application_index, headers=headers)
        response.raise_for_status()
        return response.text

    def application_index_delete(self, application_index_name: str) -> None:
        """
        Deletes the specified application index from the system.

        This method sends a DELETE request to the corresponding endpoint
        to remove an application index based on the provided name.

        :param application_index_name: The unique identifier or name of the application index to be deleted.

        :raises: requests.exceptions.HTTPError If the request to delete the application index fails

        Example:
        To delete an application index named "SampleIndex", you can call:
        `application_index_delete("SampleIndex")`
        """
        url = f'https://{self._env.domain}/metadata/{self._env.api_version}/application-index/{application_index_name}'
        headers = {"Authorization": f'Bearer {self._token_holder.get_token()}'}
        response = requests.delete(url, headers=headers)
        response.raise_for_status()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ storage ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def storage_list_blobs(self, organization: str, space: str) -> List[str]:
        """
        Retrieves a list of blob names from the specified storage belonging to the given organization and space.

        :param organization: The name of the organization associated with the storage.
        :param space: The specific space within the organization's storage.

        :return: A list of string names representing the blobs in the specified container.

        Example:
        If you want to get a list of blobs from a storage container for "OrgName" in "SpaceName",
        you might call the function like this:
        `blobs = storage_list_blobs("OrgName", "SpaceName")`
        """
        storage_url = _get_azure_storage_url(organization, space)
        sas_token = self._get_azure_sas_token(organization, space, 'read')
        blob_client = ContainerClient.from_container_url(f'{storage_url}?{sas_token}')
        blobs = blob_client.list_blobs()
        result = [(b['name']) for b in blobs]
        return result

    def storage_upload_files(self, organization: str, space: str, files: List[str], local_dir: str) -> None:
        """
        This method uploads the specified files from a local directory to a designated storage belonging to a space of a particular organization.

        if metadataGenerate is not set on the given space, a 'meta.json' file has to be included in the list of files

        :param organization: str
            The name of the organization to which the space belongs.
        :param space: str
            The name of the space to which to upload the files to.
        :param files: List[str]
            The list of file to be uploaded.
            These files should be present in the specified local directory.
            Each string in the list is a path relative to the local directory.
        :param local_dir: str
            The local directory path on your file system from where files are to be uploaded.
            This path should be accessible with appropriate read permissions.
        :return: None
            This method does not return a value.
            If any exceptions occur during the operation, they will be thrown and should be handled by the calling function.
        """
        if not organization:
            raise ValueError('missing organization name arg')
        if not space:
            raise ValueError('missing space name arg')
        if not files:
            raise ValueError('missing files arg')
        if not local_dir:
            raise ValueError('missing local_dir arg')

        # TODO: rework with api refactoring - this is quite inefficient (unnecessary call to organizationmanager)
        # check if meta.json is needed and/or provided
        org_object = self.organization_get_by_name(organization=organization)
        space_object = self.space_get_by_name(organization_id=org_object['id'], space=space)
        if space_object['metadataGenerate'] is False and 'meta.json' not in files:
            raise ValueError('metadataGenerate on space not set and meta.json is missing - required for upload.')

        json_file = open(f'{local_dir}/meta.json', 'r')
        json_string = json_file.read()
        json_file.close()
        validated = self._validate_json(json_string)
        if not validated:
            raise ValueError('meta.json invalid')

        storage_url = _get_azure_storage_url(organization, 'loadingzone')
        sas_token = self._get_azure_sas_token(organization, space, 'upload')
        timestamp = calendar.timegm(time.gmtime())  # timestamp to create the directory with
        for file in files:
            file_path = os.path.join(local_dir, file)
            if not os.path.exists(file_path):
                raise ValueError(f'File {file} does not exist in the specified directory.')
            blob_url = _sanitize_url(f'{storage_url}/{timestamp}/{file}?{sas_token}')
            self._upload_file_azure(blob_url, file_path)

        # start the ingest workflow
        url = f'{self._env.accessmanager_url}/commit?organization={organization}&space={space}&rootDir={timestamp}'
        url = _sanitize_url(url)

        payload = {}
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }

        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()

    @staticmethod
    def _upload_file_azure(blob_url: str, file_path: str) -> None:
        """
        Upload files to azure

        :param blob_url:
        :param file_path:
        """
        with BlobClient.from_blob_url(blob_url) as blob_client:
            if not blob_client.exists():
                with open(file_path, "rb") as data:
                    blob_client.upload_blob(data)
            else:
                print(f"The file already exists in the loadingzone: {file_path}")

    def storage_download_files(self, organization: str, space: str, files: List[str], local_dir: str, storage_dir: str = '') -> None:
        """
        Downloads specified files from a storage directory to a local directory.
        Files can be nested in the storage and will retain their nested structure when downloaded locally.

        :param organization: The name of the organization that owns the storage.
        :param space: The specific space within the organization's storage to access.
        :param files: List of file names or relative paths to be downloaded from the storage directory.
        :param local_dir: The local directory path where the files will be downloaded.
        :param storage_dir: The directory within the storage space to locate the files. Defaults to the root directory
                            if not provided.

        Example:
        To download files 'doc1.txt' and 'folder/doc2.txt' from the 'docs' directory in storage,
        you might call the function like this:
        `storage_download_files("OrgName", "SpaceName", ["doc1.txt", "folder/doc2.txt"], "/local/path", "docs")`
        """
        return self._storage_download_files_azure(organization, space, files, local_dir, storage_dir)

    def _storage_download_files_azure(self, organization: str, space: str, files: List[str], local_dir: str, storage_dir: str = '') -> None:
        """
        Download files from Azure storage directory to local directory.

        For nested blobs local directories are created inside the temporary directory as well.

        :param organization: organization name
        :param space: space name
        :param storage_dir: root directory inside the space to be used
        :param files: list of files to be downloaded
        :param local_dir: local directory to download the files to
        """
        if not organization:
            raise ValueError('missing organization name arg')
        if not space:
            raise ValueError('missing space name arg')
        if not files:
            raise ValueError('missing files arg')
        if not local_dir:
            raise ValueError('missing local_dir arg')

        storage_url = _get_azure_storage_url(organization, space)
        sas_token = self._get_azure_sas_token(organization, space, 'read')

        # download blobs to local directory
        for file in files:
            blob_url = _sanitize_url(f'{storage_url}/{storage_dir}/{file}?{sas_token}')
            with BlobClient.from_blob_url(blob_url) as blob_client:
                dest_file = os.path.join(local_dir, file)

                # for nested blobs, create local path as well!
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)

                with open(dest_file, "wb") as f:
                    data = blob_client.download_blob()
                    data.readinto(f)

    def storage_download_files_with_regex(self, organization: str, space: str, local_dir: str, regex: str, storage_dir: str = '') -> None:
        """
        Downloads files from a specified storage directory to a local directory based on a provided regular expression.

        This function searches for files in the storage directory that match the provided regular expression pattern.
        The full path of each file is considered during the pattern matching. Only the matching files are then downloaded
        to the specified local directory.

        :param organization: The name of the organization that owns the storage.
        :param space: The specific space within the organization's storage to search.
        :param local_dir: The local directory path where matching files will be downloaded.
        :param regex: The regular expression pattern used to filter files based on their full paths. Only files with paths matching this pattern will be
            considered for download.
        :param storage_dir: The directory within the storage space to search for files. Defaults to the root directory if not provided.

        Example:
        If we want to download all '.txt' files from the 'docs' directory in the storage,
        we might call the function like this:
        `storage_download_files_with_regex("OrgName", "SpaceName", "/local/path", r"docs/.*\.txt$")`
        """
        files = self.storage_list_blobs(organization, space)
        files_to_download = []

        for file in files:
            if storage_dir in file:
                x = re.search(regex, file)
                if x:
                    files_to_download.append(file)
        self.storage_download_files(organization, space, files_to_download, local_dir)

    def _validate_json(self, file: str) -> bool:
        """
        Validates the given json
        :param file:
            The json
        :return:
            Returns a bool, to show if the json is valid or not
        """
        url = f'https://{self._env.domain}/metadata/{self._env.api_version}/validateJson'
        payload = file
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }

        response = requests.post(url, headers=headers, data=payload)
        if 200 <= response.status_code < 300:  # valid meta.json
            return True
        if 400 <= response.status_code < 500:  # invalid meta.json
            return False
        else:
            response.raise_for_status()

    def _get_azure_sas_token(self, organization: str, space: str, reqtype: str = 'read') -> str:
        """
        Generates an upload-token via accessmanager (version > 1)

        Parameters
        ----------
        organization : str
            Organization the token shall be created for.
        space : str
            The space the token shall be created from
        reqtype : str
            Type of request. read|upload|delete

        Returns
        -------
        _type_
            The created SAS token.
        """
        url = f'{self._env.accessmanager_url}/{reqtype}?organization={organization}&space={space}'
        url = _sanitize_url(url)

        payload = {}
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }

        response = requests.post(url, headers=headers, data=payload)

        response.raise_for_status()

        return response.text

    def _storage_delete_files_azure(self, organization: str, space: str, files: List[str], storage_dir: str) -> None:
        """
        Deletes files from azure
        :param organization:
        :param space:
        :param files:
        :param storage_dir:
        """
        if not organization:
            raise ValueError('missing organization name arg')
        if not space:
            raise ValueError('missing space arg')
        if not files:
            raise ValueError('missing files arg')
        if not storage_dir:
            raise ValueError('missing storage_dir arg')

        storage_url = _get_azure_storage_url(organization, space)
        sas_token = self._get_azure_sas_token(organization, space, 'delete')

        for file in files:
            blob_url = _sanitize_url(f'{storage_url}/{storage_dir}/{file}?{sas_token}')
            with BlobClient.from_blob_url(blob_url) as blob_client:
                if blob_client.exists():
                    blob_client.delete_blob()

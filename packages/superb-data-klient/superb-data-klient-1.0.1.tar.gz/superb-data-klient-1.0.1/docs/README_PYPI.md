![PyPI - License](https://img.shields.io/pypi/l/superb-data-klient)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/superb-data-klient)
![PyPI](https://img.shields.io/pypi/v/superb-data-klient?label=version)
![PyPI - Downloads](https://img.shields.io/pypi/dm/superb-data-klient)


# superb-data-klient


**superb-data-klient** offers a streamlined interface to access various services of the *Superb Data Kraken platform* (**SDK**). With the library, you can
effortlessly fetch and index data, manage indices, spaces and organizations on the **SDK**.

Designed primarily for a Jupyter Hub environment within the platform, it's versatile enough to be set up in other environments too.


## Installation and Supported Versions

```console
$ python -m pip install superb-data-klient
```

## Usage


### Authentication


To begin, authenticate against the SDK's OIDC provider. This is achieved when instantiating the client object:

1. **System Environment Variables** (recommended for Jupyter environments):
    ```python
    import superbdataklient as sdk
    client = sdk.SDKClient()
    ```
   This approach leverages environment variables **SDK_ACCESS_TOKEN** and **SDK_REFRESH_TOKEN**.


2. **Login Credentials**:
    ``` python
    import superbdataklient as sdk
    sdk.SDKClient(username='hasslethehoff', password='lookingforfreedom')
    ```

### Configuration


While the default settings cater to the standard SDK instance, configurations for various other instances are also available.


#### Setting Environment

``` python
import superbdataklient as sdk
client = sdk.SDKClient(env='sdk-dev')
client = sdk.SDKClient(env='sdk')
```

#### Overwriting Settings

``` python
client = sdk.SDKClient(domain='mydomain.ai', realm='my-realm', client_id='my-client-id', api_version='v13.37')
```

---


### Examples


#### Organizations


Get details of all organizations, or retrieve by ID or name:

``` python
client.organization_get_all()
client.organization_get_by_id(1337)
client.organization_get_by_name('my-organization')
```

#### Spaces


To retrieve spaces related to an organization:

``` python
organization_id = 1234
client.space_get_all(organization_id)
client.space_get_by_id(organization_id, space_id)
client.space_get_by_name(organization_id, space)
```

#### Index


<!--
TODO: implement after search service works without all_access ()

List all accessible indices:

``` python
indices = client.index_get_all()
```
-->

Retrieve a specific document:

``` python
document = client.index_get_document(index_name, doc_id)
``` 

Fetch all documents within an index:

``` python
documents = client.index_get_all_documents("index_name")
```

Iterate through documents using a generator:

``` python
documents = client.index_get_documents("index-name")
for document in documents:
   print(document)
```

Index multiple documents:

``` python
documents = [
   {"_id": 123, "name": "document01", "value": "value"},
   {"_id": 1337, "name": "document02", "value": "value"}
]
index_name = "index"
client.index_documents(documents, index_name)
``` 

Note: The optional **_id** field is used as the document ID for indexing in OpenSearch.

Filter indices by organization, space, and type:

``` python
client.index_filter_by_space("my-organization", "my-space", "index-type")
```

For all spaces in an organization, use `*` instead of a space name. Available **index_type** values are **ANALYSIS** or **MEASUREMENTS**.

Create an application index:

``` python
mapping = {
   ...
}
client.application_index_create("my-application-index", "my-organization", "my-space", mapping)
```

Remove an application index by its name:

``` python
client.application_index_delete("my-organization_my-space_analysis_my-application-index")
```

#### Storage


List files in Storage:

``` python
files = client.storage_list_blobs("my-organization", "space")
```

Download specific files from Storage:

``` python
files = ['file01.txt', 'directory/file02.json']
client.storage_download_files(organization='my-organization', space='my-space', files=files, local_dir='tmp')
```

Use regex patterns for file downloads:

``` python
files = ['file01.txt', 'directory/file02.json']
client.storage_download_files_with_regex(organization='my-organization', space='my-space', files=files, local_dir='tmp', regex=r'.*json$')
```

Upload files from a local directory. Ensure the presence of a valid `meta.json`:

``` python
files = ['meta.json', 'file01.txt', 'file02.txt']
client.storage_upload_files_to_loadingzone(organization='my-organization', space='my-space', files= files, local_dir='tmp')
```


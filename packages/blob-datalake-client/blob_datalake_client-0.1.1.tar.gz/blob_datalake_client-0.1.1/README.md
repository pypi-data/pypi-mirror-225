# Blob Data Lake Client Description

A library built in the context of P2W for managing files and data frames in Azure Blob Storage.


**Main Features:**

- Uploading, listing, downloading and deleting Files from an Azure Blob Storage instance;
- Uploading Data Frames to an Azure Blob Storage instance;
- Managing directories.

---

## Installation and Execution

### 1. Install Python dependencies

```
$ pip3 install virtualenv
$ virtualenv -p python3 venv
$ . venv/bin/activate
$ pip3 install blob_datalake_client
```

## Module Usage

### 1. Module Import

```
from blob_datalake_client import DataLake
```

### 2. Instantiating Datalake Class

```
datalake_client = DataLake(storage_username, storage_user_key, storage_file_system_name)
```

The `storage_username`, `storage_user_key` and `storage_file_system_name` parameters should be set according to the usage scenario.

### 3. Managing Files

#### 3.1. Uploading File

```
datalake_client.upload_file(storage_data_path, filename, file_bytes, metadata, overwrite_flag)
```

Description of parameters:

- `storage_data_path` is the path where the file will be uploaded;
- `filename` is the name with which the file will be uploaded;
- `file_bytes` is the content of the file to be uploaded;
- `metadata` is an object with metadata about the file to be uploaded;
- `overwrite_flag` indicates whether the file should be overwritten if it already exists.

#### 3.2. Listing Files

```
datalake_client.list_files(storage_data_path)
```

Description of parameters:

- `storage_data_path` is the path that will have the files listed.

#### 3.3. Downloading File

```
file_data, file_type, file_metadata = datalake_client.get_file(storage_data_path, filename)
```

Description of parameters:

- `storage_data_path` is the path to fetch the file;
- `filename` is the name of the file to be downloaded.

#### 3.4. Removing File

```
datalake_client.rm_file(storage_data_path, filename)
```

Description of parameters:

- `storage_data_path` is the path to fetch the file;
- `filename` is the name of the file to be removed.

### 4. Managing Data Frames

#### 4.1. Uploading Data Frame

```
datalake_client.upload_data_frame(data_frame, storage_data_path, filename, output_format, metadata, overwrite_flag)
```

Description of parameters:

- `data_frame` is the data_frame to be uploaded;
- `storage_data_path` is the path where the data_frame will be uploaded;
- `filename` is the name with which the data_frame will be uploaded;
- `output_format` is the data_frame output format;
- `metadata` is an object with metadata about the data_frame to be uploaded;
- `overwrite_flag` indicates whether the data_frame should be overwritten if it already exists.

### 5. Managing Directories

#### 5.1. Creating Directory

```
datalake_client.mkdir(storage_data_path)
```

Description of parameters:

- `storage_data_path` is the path where the directory should be created.
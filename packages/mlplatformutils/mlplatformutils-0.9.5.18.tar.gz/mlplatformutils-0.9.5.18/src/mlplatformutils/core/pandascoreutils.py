import json

def read_from_delta_as_pandas(SOURCE_STORAGE_ACCOUNT_VALUE,\
                              SOURCE_READ_SPN_VALUE,\
                              SOURCE_READ_SPNKEY_VALUE,\
                              tenant_id,\
                              AML_STORAGE_EXPERIMENT_DELTA_ROOT_PATH):
    
    from deltalake import DeltaTable
    from adlfs import AzureBlobFileSystem

    fs = AzureBlobFileSystem(
        account_name=SOURCE_STORAGE_ACCOUNT_VALUE,\
        client_id=SOURCE_READ_SPN_VALUE,\
        client_secret=SOURCE_READ_SPNKEY_VALUE,\
        tenant_id=tenant_id
    )
    pandas_df = DeltaTable(AML_STORAGE_EXPERIMENT_DELTA_ROOT_PATH, file_system=fs).to_pandas()

    return pandas_df

def read_parquet_file_from_adlsgen2_as_pandas(SOURCE_STORAGE_ACCOUNT_VALUE,\
                                SOURCE_READ_SPN_VALUE,\
                                SOURCE_READ_SPNKEY_VALUE,\
                                tenant_id,\
                                AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH):
    #AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH "<your_container>/<directory>/<file_name>.parquet"
    from azure.identity import ClientSecretCredential
    import pyarrow.fs
    import pyarrowfs_adlgen2
    import pandas as pd
    import pyarrow.parquet as pq

    credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=SOURCE_READ_SPN_VALUE,
    client_secret=SOURCE_READ_SPNKEY_VALUE)
    
    handler=pyarrowfs_adlgen2.AccountHandler.from_account_name(SOURCE_STORAGE_ACCOUNT_VALUE,credential=credential)
    fs = pyarrow.fs.PyFileSystem(handler)
    #pandas_df = pd.read_parquet(AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH, filesystem=fs , engine="pyarrow")
    #pandas_df = pq.read_table(source=AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH, filesystem=fs, use_legacy_dataset= True).to_pandas()
    pandas_df = pq.ParquetDataset(AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH,filesystem=fs).read().to_pandas()

    return pandas_df

def list_directory_contents(storage_account_name,\
                            tenant_id,client_id,\
                            client_secret,\
                            directory_path):
    from azure.storage.filedatalake import DataLakeServiceClient
    from azure.identity import ClientSecretCredential
    try:
        container = directory_path.split("/")[0]
        directory_path ="/".join(directory_path.split("/")[1:])
        credential = ClientSecretCredential(tenant_id=tenant_id,
                                            client_id=client_id,
                                            client_secret=client_secret)
        
        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format("https", storage_account_name),\
                                               credential=credential)
        file_system_client = service_client.get_file_system_client(file_system=container)

        paths = file_system_client.get_paths(path=directory_path)
        filenames=[]
        for path in paths:
            if (path.name).endswith(".parquet"):
                filenames.append(container+"/"+path.name)
        return filenames
    except Exception as e:
     print(e)

def read_parquet_directory_from_adlsgen2_as_pandas(SOURCE_STORAGE_ACCOUNT_VALUE,\
                                SOURCE_READ_SPN_VALUE,\
                                SOURCE_READ_SPNKEY_VALUE,\
                                tenant_id,\
                                AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH):
    #AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH "<your_container>/<directory>"
    parquet_files_from_path_list = list_directory_contents(SOURCE_STORAGE_ACCOUNT_VALUE,\
                                                 tenant_id,\
                                                 SOURCE_READ_SPN_VALUE,\
                                                 SOURCE_READ_SPNKEY_VALUE,\
                                                 AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH)

    from azure.identity import ClientSecretCredential
    import pyarrow.fs
    import pyarrowfs_adlgen2
    import pandas as pd
    import pyarrow.parquet as pq

    credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=SOURCE_READ_SPN_VALUE,
    client_secret=SOURCE_READ_SPNKEY_VALUE)

    handler=pyarrowfs_adlgen2.AccountHandler.from_account_name(SOURCE_STORAGE_ACCOUNT_VALUE,credential=credential)
    fs = pyarrow.fs.PyFileSystem(handler)
    pandas_df = pq.ParquetDataset(parquet_files_from_path_list,filesystem=fs).read().to_pandas()

    return pandas_df

def write_pandas_as_parquet_file_to_adlsgen2(SOURCE_STORAGE_ACCOUNT_VALUE,\
                                SOURCE_READ_SPN_VALUE,\
                                SOURCE_READ_SPNKEY_VALUE,\
                                tenant_id,\
                                AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH,\
                                pandas_df):
    
    #AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH = "<your_container>/<directory>/<file_name>.parquet"
    from azure.identity import ClientSecretCredential
    import pyarrow.fs
    import pyarrow as pa
    import pyarrow.parquet
    import pyarrowfs_adlgen2
    import pyarrow.dataset

    credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=SOURCE_READ_SPN_VALUE,
    client_secret=SOURCE_READ_SPNKEY_VALUE)

    handler=pyarrowfs_adlgen2.AccountHandler.from_account_name(SOURCE_STORAGE_ACCOUNT_VALUE,credential=credential)
    fs = pyarrow.fs.PyFileSystem(handler)
    pyarrow_table = pa.Table.from_pandas(pandas_df)
    
    with fs.open_output_stream(AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH) as out:
        pyarrow.parquet.write_table(pyarrow_table, out)

    """
    pyarrow.dataset.write_dataset(
        pyarrow_table,
        AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH,
        format='parquet',
        filesystem=pyarrow.fs.PyFileSystem(handler)
    )
    """
    print("File Write Successful at "+AML_STORAGE_EXPERIMENT_PARQUET_ROOT_PATH+" !")
    return
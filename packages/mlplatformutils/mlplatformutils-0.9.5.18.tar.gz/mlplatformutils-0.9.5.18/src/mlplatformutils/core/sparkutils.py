import json
def get_max_properties_starting_with(id, prefix,dataprop,LineageLogger):

    document=LineageLogger.query_graph("g.V().hasLabel('amlrun').has('id', '"+id+"')")
    jsondump = json.dumps(document)
    jsonload = json.loads(jsondump)
    for item in jsonload:
        properties = item.get('properties')
    if properties:
        matching_props = [prop[-1] for prop in properties.keys() if prop.startswith(prefix)]
        max_val = max(int(prop) for prop in matching_props) if matching_props else 0
        datapropval = properties.get(dataprop)[0].get('value') if properties.get(dataprop) else None
    else:
        max_val = 0
    return str(max_val+1),datapropval

def read_from_adls_gen2(SOURCE_STORAGE_ACCOUNT_VALUE,\
                        AZURE_TENANT_ID,\
                        file_path,\
                        file_format,\
                        SOURCE_READ_SPN_VALUE,\
                        SOURCE_READ_SPNKEY_VALUE,\
                        RUN_ID,\
                        PIPELINE_STEP_NAME,\
                        LineageLogger):
    from pyspark.sql.session import SparkSession
    spark = SparkSession.builder.appName("Read from ADLS Gen2").getOrCreate()
    spark.conf.set("fs.azure.account.auth.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "OAuth")
    spark.conf.set("fs.azure.account.oauth.provider.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net",  "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
    spark.conf.set("fs.azure.account.oauth2.client.id."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_READ_SPN_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.secret."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_READ_SPNKEY_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.endpoint."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "https://login.microsoftonline.com/"+AZURE_TENANT_ID+"/oauth2/token")

    df = spark.read.format(file_format).load(file_path)
    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    sourcePostfix,dataprop=get_max_properties_starting_with(documentId,"DataReadSourceColumns","DataReadSource",LineageLogger)
    if dataprop is None:
        dataprop = str({"DataReadSource_"+sourcePostfix: file_path,\
                                    "Type":"ADLS"})
    else:
        dataprop = str(dataprop)+str(",")+str({"DataReadSource_"+sourcePostfix: file_path,\
                                    "Type":"ADLS"})
    dataprop = dataprop.replace("'",'"')
    LineageLogger.update_vertex(documentId, {"DataReadSource_"+sourcePostfix: str(file_path),\
                                             "FileFormat_"+sourcePostfix:str(file_format),\
                                             "DataReadSourceColumns_"+sourcePostfix:"["+",".join(df.columns)+"]",\
                                             "DataReadSource":dataprop})

    return df

def write_to_adls_gen2(SOURCE_STORAGE_ACCOUNT_VALUE,\
                       AZURE_TENANT_ID,\
                       file_path,\
                       file_format,\
                       repartition,\
                       partitionColumn,\
                       dynamicPartitionOverwriteMode,\
                       df,\
                       SOURCE_WRITE_SPN_VALUE,\
                       SOURCE_WRITE_SPNKEY_VALUE,\
                       RUN_ID,\
                       PIPELINE_STEP_NAME,\
                       LineageLogger):
    from pyspark.sql.session import SparkSession             
    spark = SparkSession.builder.appName("Read from ADLS Gen2").getOrCreate()
    spark.conf.set("fs.azure.account.auth.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "OAuth")
    spark.conf.set("fs.azure.account.oauth.provider.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net",  "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
    spark.conf.set("fs.azure.account.oauth2.client.id."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_WRITE_SPN_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.secret."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_WRITE_SPNKEY_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.endpoint."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "https://login.microsoftonline.com/"+AZURE_TENANT_ID+"/oauth2/token")
    
    if dynamicPartitionOverwriteMode:
        spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    
    if repartition is None:
        if partitionColumn:
            #partitionColumn accepted as list of columns
            df.write.format(file_format).partitionBy(partitionColumn).mode("overwrite").save(file_path)
        else: 
            df.write.format(file_format).mode('overwrite').save(file_path)
    else:
        if partitionColumn:
            df.repartition(repartition).write.format(file_format).partitionBy(partitionColumn).mode("overwrite").save(file_path)
        else:
            df.repartition(repartition).write.format(file_format).mode('overwrite').save(file_path)

    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    targetPostfix,dataprop=get_max_properties_starting_with(documentId,"DataWriteColumns","DataWriteTarget",LineageLogger)  
    if dataprop is None:
        dataprop = str({"DataWriteTarget_"+targetPostfix: file_path,\
                                    "Type":"ADLS"})
    else:
        dataprop = str(dataprop)+str(",")+str({"DataWriteTarget_"+targetPostfix: file_path,\
                                    "Type":"ADLS"})
    dataprop = dataprop.replace("'",'"')
    LineageLogger.update_vertex(documentId, {"DataWriteTarget_"+targetPostfix: str(file_path),\
                                             "FileFormat_"+targetPostfix:str(file_format),\
                                             "DataWriteColumns_"+targetPostfix:"["+",".join(df.columns)+"]",\
                                             "DataWriteTarget":dataprop})
    
    return

def read_from_kusto(kustoOptions,RUN_ID,PIPELINE_STEP_NAME,LineageLogger):
    from pyspark.sql.session import SparkSession
    pyKusto = SparkSession.builder.appName("kustoPySpark").getOrCreate()
    kustoDf  = pyKusto.read. \
                format("com.microsoft.kusto.spark.datasource"). \
                option("kustoCluster", kustoOptions["kustoCluster"]). \
                option("kustoDatabase", kustoOptions["kustoDatabase"]). \
                option("kustoQuery", kustoOptions["kustoTable"]). \
                option("kustoAadAppId", kustoOptions["kustoAADClientID"]). \
                option("kustoAadAppSecret", kustoOptions["kustoClientAADClientPassword"]). \
                option("kustoAadAuthorityID", kustoOptions["kustoAADAuthorityID"]). \
                load()
    
    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    sourcePostfix,dataprop=get_max_properties_starting_with(documentId,"DataReadSourceColumns","DataReadSource",LineageLogger)
    if dataprop is None:
        dataprop = str({"DataReadSource_"+sourcePostfix: "ADX-Cluster "+str(kustoOptions["kustoCluster"])+" ADX-Database"+str(kustoOptions["kustoDatabase"])+ " ADX-Table "+str(kustoOptions["kustoTable"]),\
                                    "Type":"ADX"})
    else:
        dataprop = str(dataprop)+str(",")+str({"DataReadSource_"+sourcePostfix: "ADX-Cluster "+str(kustoOptions["kustoCluster"])+" ADX-Database"+str(kustoOptions["kustoDatabase"])+ " ADX-Table "+str(kustoOptions["kustoTable"]),\
                                    "Type":"ADX"})
    dataprop = dataprop.replace("'",'"')
    LineageLogger.update_vertex(documentId, {"KustoDataReadCluster_"+sourcePostfix: str(kustoOptions["kustoCluster"]),\
                                        "KustoDataReadDatabase_"+sourcePostfix: str(kustoOptions["kustoDatabase"]),\
                                        "KustoDataReadQuery_"+sourcePostfix: str(kustoOptions["kustoTable"]),\
                                        "DataReadSourceColumns_"+sourcePostfix:"["+",".join(kustoDf.columns)+"]",\
                                        "DataReadSource":dataprop})            
    return kustoDf

def synapseread_from_kusto(SynapseLinkedService,Query,kustoDatabase,RUN_ID,PIPELINE_STEP_NAME,LineageLogger):
    from pyspark.sql.session import SparkSession
    pyKusto = SparkSession.builder.appName("kustoPySpark").getOrCreate()
    sc = pyKusto.sparkContext
    crp = sc._jvm.com.microsoft.azure.kusto.data.ClientRequestProperties()
    crp.setOption("norequesttimeout",True)
    crp.setOption("servertimeout", 100000 * 60)
    crp.toString()
    kustoDf  = pyKusto.read.\
                format("com.microsoft.kusto.spark.synapse.datasource").\
                option("spark.synapse.linkedService",SynapseLinkedService).\
                option("kustoDatabase", kustoDatabase).\
                option("kustoQuery", Query).\
                option("authType", "LS").\
                option("clientRequestPropertiesJson", crp.toString()).\
                option("readMode", 'ForceDistributedMode').\
                load()
    
    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    sourcePostfix,dataprop=get_max_properties_starting_with(documentId,"DataReadSourceColumns","DataReadSource",LineageLogger)
    if dataprop is None:
        dataprop = str({"DataReadSource_"+sourcePostfix: " ADX-Database"+str(kustoDatabase),\
                                    "Type":"ADX"})
    else:
        dataprop = str(dataprop)+str(",")+str({"DataReadSource_"+sourcePostfix: " ADX-Database"+str(kustoDatabase),\
                                    "Type":"ADX"})
    dataprop = dataprop.replace("'",'"')
    LineageLogger.update_vertex(documentId, {"KustoDataReadDatabase_"+sourcePostfix: str(kustoDatabase),\
                                        "DataReadSourceColumns_"+sourcePostfix:"["+",".join(kustoDf.columns)+"]",\
                                        "DataReadSource":dataprop})                 
    return kustoDf

def read_from_azsql(SQL_SERVER_INSTANCE,access_token,Query,RUN_ID,PIPELINE_STEP_NAME,LineageLogger):
    from pyspark.sql.session import SparkSession
    pySql = SparkSession.builder.appName("AzSQLPySpark").getOrCreate()
    df = pySql.read \
        .format("com.microsoft.sqlserver.jdbc.spark") \
        .option("url", SQL_SERVER_INSTANCE) \
        .option("query", Query) \
        .option("accessToken", access_token) \
        .option("encrypt", "true") \
        .option("hostNameInCertificate", "*.database.windows.net") \
        .load()

    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    sourcePostfix,dataprop=get_max_properties_starting_with(documentId,"DataReadSourceColumns","DataReadSource",LineageLogger)
    if dataprop is None:
        dataprop = str({"DataReadSource_"+sourcePostfix: "SQL SERVER INSTANCE "+str(SQL_SERVER_INSTANCE)+" SQL Query "+str(Query),\
                                    "Type":"AzureSQL"})
    else:
        dataprop = str(dataprop)+str(",")+str({"DataReadSource_"+sourcePostfix: "SQL SERVER INSTANCE "+str(SQL_SERVER_INSTANCE)+" SQL Query "+str(Query),\
                                    "Type":"AzureSQL"})
    dataprop = dataprop.replace("'",'"')
    LineageLogger.update_vertex(documentId, {"SqlDataReadServer_"+sourcePostfix: str(SQL_SERVER_INSTANCE),\
                                        "SqlDataReadQuery_"+sourcePostfix: str(Query),\
                                        "DataReadSourceColumns_"+sourcePostfix:"["+",".join(df.columns)+"]",\
                                        "DataReadSource":dataprop}) 
    return df

def read_sstream_from_adls_gen1(AZURE_TENANT_ID,\
                                file_path,\
                                SOURCE_READ_SPN_VALUE,\
                                SOURCE_READ_SPNKEY_VALUE,\
                                RUN_ID,\
                                PIPELINE_STEP_NAME,\
                                LineageLogger):
    import hashlib
    from pyspark.sql.session import SparkSession
    from pyspark.dbutils import DBUtils
    spark = SparkSession.builder.appName("Read SSTREAM from ADLS Gen1").getOrCreate()
    dbutils = DBUtils(spark)
    
    if '*' not in file_path:
        toHash = file_path[:file_path.rfind('/')]
        toAppend = file_path[file_path.rfind('/'):]
    else:
        toHash = file_path[:file_path.index('*')-1]
        toAppend = file_path[file_path.index('*')-1:]
    hash_object = hashlib.sha256(toHash.encode())
    mountpoint = "/mnt/"+hash_object.hexdigest()

    configs = {"fs.adl.oauth2.access.token.provider.type": "ClientCredential",
    "fs.adl.oauth2.client.id": SOURCE_READ_SPN_VALUE,
    "fs.adl.oauth2.credential": SOURCE_READ_SPNKEY_VALUE,
    "fs.adl.oauth2.refresh.url": "https://login.microsoftonline.com/"+AZURE_TENANT_ID+"/oauth2/token"}

    mountPoints = [mount.mountPoint for mount in dbutils.fs.mounts()]
    if mountpoint not in mountPoints:
        dbutils.fs.mount(source = toHash, mount_point = mountpoint, extra_configs = configs)
        print('Data successfully mounted at:', mountpoint)
    else:
        dbutils.fs.unmount(mountpoint)
        dbutils.fs.mount(source = toHash, mount_point = mountpoint, extra_configs = configs)
        print('Data successfully mounted at:', mountpoint)
        print("loading","dbfs:"+mountpoint+toAppend)
    
    df =spark.read.format("sstream").load("dbfs:"+mountpoint+toAppend)

    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    sourcePostfix,dataprop=get_max_properties_starting_with(documentId,"DataReadSourceColumns","DataReadSource",LineageLogger)
    if dataprop is None:
        dataprop = str({"DataReadSource_"+sourcePostfix: file_path,\
                                    "Type":"ADLSGEN1"})
    else:
        dataprop = str(dataprop)+str(",")+str({"DataReadSource_"+sourcePostfix: file_path,\
                                    "Type":"ADLSGEN1"})
    dataprop = dataprop.replace("'",'"')
    LineageLogger.update_vertex(documentId, {"DataReadSource_"+sourcePostfix: str(file_path),\
                                             "FileFormat_"+sourcePostfix:str("sstream"),\
                                             "DataReadSourceColumns_"+sourcePostfix:"["+",".join(df.columns)+"]",\
                                             "DataReadSource":dataprop})

    return df
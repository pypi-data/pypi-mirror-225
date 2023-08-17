from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError

class Freshness:
    def __init__(self, endpoint_url, primary_key):
        self.endpoint_url = endpoint_url
        self.primary_key = primary_key
        self.database_name = "mlopstelemetrydb"
        self.container_name = "datafreshness"
        self.cosmos_client = CosmosClient(self.endpoint_url, self.primary_key)
        self.database = self.cosmos_client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def add_freshness(self, document):
        self.container.create_item(document)
        print('Document Added Successfully!')
        return

    def upsert_freshness(self, document):
            try:
                self.container.upsert_item(document)
                print("Document upserted successfully!")
            except Exception as ex:
                print("Error upserting document:", str(ex))

    def query_freshness(self, QueryString):
        import json
        try:
            returnVals=[]
            for item in self.container.query_items(query=QueryString,enable_cross_partition_query=True):
                returnVals.append(json.dumps(item, indent=True))
            return returnVals
        except CosmosResourceNotFoundError:
            return None
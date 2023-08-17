from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback
import asyncio

"""
When Running this Lineage Package from Jupyter Nootebook - 
The below 3 Lines Help over come JupyterNotebook RuntimeError: Cannot run the event loop while another loop is running
import asyncio
import nest_asyncio
nest_asyncio.apply()
"""

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class LineageGraph:

    def __init__(self, endpoint, key, partition_key):

        try:
            self.client = client.Client(f"wss://{endpoint}:443/", 'g',
                                username=f"/dbs/mlopslineagedb/colls/lineagegraph",
                                password=key,
                                message_serializer=serializer.GraphSONSerializersV2d0()
                                )
            self.partition_key = partition_key
        except GremlinServerError as e:
            print('Code: {0}, Attributes: {1}'.format(e.status_code, e.status_attributes))
            cosmos_status_code = e.status_attributes["x-ms-status-code"]
            if cosmos_status_code == 409:
                print('Conflict error!')
            elif cosmos_status_code == 412:
                print('Precondition error!')
            elif cosmos_status_code == 429:
                print('Throttling error!')
            elif cosmos_status_code == 1009:
                print('Request timeout error!')
            else:
                print("Default error handling")
            traceback.print_exc(file=sys.stdout) 
            raise ValueError("Failed to connect to Cosmos Gremlin graph")

    def print_status_attributes(self,result):
        print("\tResponse status_attributes:\n\t{0}".format(result.status_attributes))

    def add_vertex(self, label, properties,run_id,pipeline_step_name):
        try:
            query = "g.V().hasLabel('amlrun').has('RUN_ID', '"+run_id+"').has('PIPELINE_STEP_NAME', '"+pipeline_step_name+"').values('id')"
            documentIds = self.query_graph(query)
            if documentIds:
                documentId = documentIds[0]
                print("The Vertex Already Exists! Updating it..")
                properties.pop('EXPERIMENT_NAME')
                self.update_vertex(documentId,properties)
            else:
                print("Adding a new Vertex!")
                if self.partition_key in properties.keys():
                    queryStr=""
                    queryStr = queryStr + "g.addV('" + label + "')"
                    for key, value in properties.items():
                        queryStr = queryStr + ".property('" + key + "','" + str(value) + "')"
                    print(queryStr)
                else:
                    print("Unable To Add Vertex. Partition Key '"+ self.partition_key +"' Not Found! Failed to Add VERTEX to Cosmos Gremlin graph!")
                callback = self.client.submitAsync(queryStr)
                if callback.result() is not None:
                    print("\tInserted this vertex:\n\t{0}".format(callback.result().all().result()))
                else:
                    print("Something went wrong with this query: {0}".format(queryStr))
                print("\n")
                self.print_status_attributes(callback.result())
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to add vertex to Cosmos Gremlin graph!")

    def get_vertices(self, label,id):
        try:
            StrQuery = "g.V().hasLabel('" + label + "')"+".has('id','" + id + "')"
            callback = self.client.submitAsync(StrQuery)
            for result in callback.result():
                print("\t{0}".format(str(result)))
                return str(result)
        except Exception as e:
            traceback.print_exc()
            self.print_status_attributes(callback.result())
            raise ValueError("Failed to get vertices from Cosmos Gremlin graph ")

    def is_vertex(self, label,id):
        try:
            StrQuery = "g.V().hasLabel('" + label + "')"+".has('id','" + id + "')"
            callback = self.client.submitAsync(StrQuery)
            for result in callback.result():
                return True
            return False
        except Exception as e:
            traceback.print_exc()
            self.print_status_attributes(callback.result())
            return False

    def update_vertex(self, id, properties):
        try:
            queryStr="g.V().has('id','"+id+"').values('label')"
            callback = self.client.submitAsync(queryStr)
            for result in callback.result():
                label = result[0]
                if self.is_vertex(label,id):
                    queryStr=""
                    queryStr = queryStr + "g.V('" + id + "')"
                    for key, value in properties.items():
                        queryStr = queryStr + ".property('" + key + "','" + str(value) + "')"
                        print(queryStr)
                    callback = self.client.submitAsync(queryStr)
                    if callback.result() is not None:
                        print("\tUpdated this vertex:\n\t{0}".format(callback.result().all().result()))
                    else:
                        print("Something went wrong with this query: {0}".format(queryStr))
            self.print_status_attributes(callback.result())

        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to UPDATE vertex to Cosmos Gremlin graph!")


    def insert_edges(self,source_v_id,target_v_id,edge_label,properties):
        try:
            queryStr=""
            queryStr = queryStr + "g.V('" + source_v_id + "')" + ".addE('" + edge_label + "')" + ".to(g.V('" + target_v_id + "'))"
            if properties is not None:
                for key, value in properties.items():
                    queryStr = queryStr + ".property('" + key + "','" + str(value) + "')"
            print(queryStr)
            callback = self.client.submitAsync(queryStr)
            if callback.result() is not None:
                print("\tConnected the verteices with Edge:\n\t{0}".format(callback.result().all().result()))
            else:
                print("Something went wrong with this query: {0}".format(queryStr))
            print("\n")
            self.print_status_attributes(callback.result())

        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to add EDGE to Cosmos Gremlin graph!")

    def drop_vertex(self,id):
        try:
            queryStr="g.V('id','"+id+"').drop()"
            callback = self.client.submitAsync(queryStr)
            for result in callback.result():
                print(result)
            self.print_status_attributes(callback.result())
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to DROP Vertex to Cosmos Gremlin graph!")

    def drop_edge(self,source_v_id,target_v_id,edge_label):
        try:
            queryStr="g.V('id','"+source_v_id+"').outE('"+edge_label+"').where(inV().has('id', '"+target_v_id+"')).drop()"
            callback = self.client.submitAsync(queryStr)
            for result in callback.result():
                print(result)
            self.print_status_attributes(callback.result())
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to DROP EDGE to Cosmos Gremlin graph!")
    
    def query_graph(self,query):
        try:
            result = None
            callback = self.client.submitAsync(query)
            for result in callback.result():
                print(result)
            self.print_status_attributes(callback.result())
            return result
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to QUERY Cosmos Gremlin graph!")
        
    def update_lineage_graph(self,run_id,pipeline_step_name,properties):
        try:
            query = "g.V().hasLabel('amlrun').has('RUN_ID', '"+run_id+"').has('PIPELINE_STEP_NAME', '"+pipeline_step_name+"').values('id')"
            documentIds = self.query_graph(query)
            if documentIds:
                documentId = documentIds[0]
                print("The Vertex Already Exists! Updating it..")            
                self.update_vertex(documentId,properties)
            else:
                print("Document Not Found!")
            return
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to Update lineage graph!")
        
    def connect_lineage_graph(self,run_id,source_pipeline_step_name,dest_pipeline_step_name):
        try:
            src_query = "g.V().hasLabel('amlrun').has('RUN_ID', '"+run_id+"').has('PIPELINE_STEP_NAME', '"+source_pipeline_step_name+"').values('id')"
            source_doc_id = self.query_graph(src_query)
            if not source_doc_id:
                print("No source document ID found.")
                return
            source_doc_id = source_doc_id[0]
            dest_query = "g.V().hasLabel('amlrun').has('RUN_ID', '"+run_id+"').has('PIPELINE_STEP_NAME', '"+dest_pipeline_step_name+"').values('id')"
            dest_doc_id = self.query_graph(dest_query)
            if not dest_doc_id:
                print("No Target document ID found.")
                return
            dest_doc_id = dest_doc_id[0]
            self.insert_edges(source_doc_id, dest_doc_id,"DependendsOn", None)
            return
        except Exception as e:
            traceback.print_exc()
            raise ValueError("Failed to connect lineage graph!")
        
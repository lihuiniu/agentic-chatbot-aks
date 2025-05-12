import os
from azure.cosmos import CosmosClient

def get_user_context(user_id: str) -> str:
    client = CosmosClient(os.environ["COSMOS_DB_URI"], credential=os.environ["COSMOS_DB_KEY"])
    db = client.get_database_client(os.environ["COSMOS_DB_NAME"])
    container = db.get_container_client("UserRequests")
    query = f"SELECT * FROM c WHERE c.user_id = '{user_id}' ORDER BY c._ts DESC"
    results = list(container.query_items(query=query, enable_cross_partition_query=True))
    if results:
        return results[0].get("context", "No context available")
    return "No context available"
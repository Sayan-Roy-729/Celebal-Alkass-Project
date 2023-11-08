import os
from typing import Dict, Any, List

from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos import DatabaseProxy, ContainerProxy

load_dotenv()


class CosmosDBClient:
    """
    A class for interacting with Azure Cosmos DB.

    Args:
        endpoint (str): The Cosmos DB endpoint URL.
        key (str): The Cosmos DB access key.

    Attributes:
        _cosmos_endpoint (str): The Cosmos DB endpoint URL.
        _cosmos_key (str): The Cosmos DB access key.
        _client (CosmosClient): The Cosmos DB client instance.
    """

    def __init__(self, endpoint: str, key: str) -> None:
        """
        Initialize a CosmosDBClient instance.

        Args:
            endpoint (str): The Cosmos DB endpoint URL.
            key (str): The Cosmos DB access key.
        """
        self._cosmos_endpoint = endpoint
        self._cosmos_key = key
        self._client = CosmosClient(url=self._cosmos_endpoint, credential=self._cosmos_key)

    def create_or_get_database(self, database_name: str) -> DatabaseProxy:
        """
        Create or get a database in Cosmos DB.

        Args:
            database_name (str): The name of the database.

        Returns:
            DatabaseProxy: The database instance.
        """
        database = self._client.create_database_if_not_exists(id=database_name)
        return database

    def create_or_get_container(self, database: DatabaseProxy, container_name: str, partition_key: str) -> ContainerProxy:
        """
        Create or get a container within a database in Cosmos DB.

        Args:
            database (DatabaseProxy): The database instance.
            container_name (str): The name of the container.
            partition_key (str): The partition key path.

        Returns:
            ContainerProxy: The container instance.
        """
        key_path = PartitionKey(path=partition_key)
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=key_path,
            offer_throughput=400
        )
        return container

    def add_new_item(self, container: ContainerProxy, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new item to a container in Cosmos DB.

        Args:
            container (ContainerProxy): The container instance.
            item (dict): The item to be added.

        Returns:
            Dict[str, Any]: The added item.
        """
        return container.create_item(body=item)

    def get_item(self, container: ContainerProxy, item_id: str, partition_key: str) -> Dict[str, Any]:
        """
        Retrieve an item from a container in Cosmos DB.

        Args:
            container (ContainerProxy): The container instance.
            item_id (str): The ID of the item.
            partition_key (str): The partition key value.

        Returns:
            Dict[str, Any]: The retrieved item.
        """
        return container.read_item(item=item_id, partition_key=partition_key)

    def query_items(self, container: ContainerProxy, query: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """
        Query items in a container in Cosmos DB.

        Args:
            container (ContainerProxy): The container instance.
            query (str): The query string.
            params (List[Any]): Optional query parameters.

        Returns:
            List[Dict[str, Any]]: A list of queried items.
        """
        query_iter = container.query_items(query, parameters=params, enable_cross_partition_query=False)
        results = list(query_iter)
        return results

    def delete_item(self, container: ContainerProxy, item_id: str, partition_key: str) -> None:
        """
        Delete an item from a container in Cosmos DB.

        Args:
            container (ContainerProxy): The container instance.
            item_id (str): The ID of the item.
            partition_key (str): The partition key value.
        """
        container.delete_item(item=item_id, partition_key=partition_key)

    def replace_item(self, container: ContainerProxy, item_id: str, partition_key: str, updated_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Replace an item in a container in Cosmos DB with an updated item.

        Args:
            container (ContainerProxy): The container instance.
            item_id (str): The ID of the item.
            partition_key (str): The partition key value.
            updated_item (dict): The updated item.

        Returns:
            Dict[str, Any]: The replaced item.
        """
        existing_item = self.get_item(container, item_id, partition_key)
        if existing_item:
            updated_item['id'] = item_id
            return container.replace_item(item=updated_item)
        return None

    def upsert_item(self, container: ContainerProxy, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upsert (insert or update) an item in a container in Cosmos DB.

        Args:
            container (ContainerProxy): The container instance.
            item (dict): The item to be upserted.

        Returns:
            Dict[str, Any]: The upserted item.
        """
        return container.upsert_item(item)

# Usage example:
if __name__ == "__main__":
    cosmos_endpoint = os.getenv("COSMOS_ENDPOINT")
    cosmos_key = os.getenv("COSMOS_KEY")
    db_name = "ProductCatalog"
    container_name = "Products"
    partition_key = "/category"

    client    = CosmosDBClient(cosmos_endpoint, cosmos_key)
    database  = client.create_or_get_database(db_name)
    container = client.create_or_get_container(database, container_name, partition_key)

    # Sample product items
    product1 = {
        "id": "1001",
        "name": "Product A",
        "category": "Electronics",
        "price": 599.99
    }

    product2 = {
        "id": "1002",
        "name": "Product B",
        "category": "Clothing",
        "price": 49.99
    }

    product3 = {
        "id": "1003",
        "name": "Product C",
        "category": "Home & Garden",
        "price": 149.99
    }
    
    # add items to the Cosmos DB container
    client.add_new_item(container, product1)
    client.add_new_item(container, product2)
    client.add_new_item(container, product3)

    # retrieve an item from the Cosmos DB container
    
